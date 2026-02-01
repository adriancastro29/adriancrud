from django.db import models
from django.contrib.auth.models import User



# -----------------------------
# Pharmacy
# -----------------------------
class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# -----------------------------
# Medicine
# -----------------------------
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)

    # Use DecimalField for money
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_generic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Generic' if self.is_generic else 'Brand'})"


# -----------------------------
# Inventory
# -----------------------------
class Inventory(models.Model):
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    stock_quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('pharmacy', 'medicine')

    def __str__(self):
        return f"{self.pharmacy.name} - {self.medicine.name}"


# -----------------------------
# Order
# -----------------------------
class Order(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order #{self.id}"


# -----------------------------
# Order Item
# -----------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"


# -----------------------------
# Delivery
# -----------------------------
class Delivery(models.Model):

    DELIVERY_PENDING = 'pending'
    DELIVERY_OUT = 'out_for_delivery'
    DELIVERY_DELIVERED = 'delivered'

    DELIVERY_STATUS_CHOICES = [
        (DELIVERY_PENDING, 'Pending'),
        (DELIVERY_OUT, 'Out for Delivery'),
        (DELIVERY_DELIVERED, 'Delivered'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery'
    )
    delivery_address = models.TextField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default=DELIVERY_PENDING
    )

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"

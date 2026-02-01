from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicine, Order, OrderItem, Inventory
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'


class MedicineListView(ListView):
    model = Medicine
    template_name = 'app/medicine_list.html'
    context_object_name = 'medicines'


class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'app/medicine_detail.html'
    context_object_name = 'medicine'


class MedicineCreateView(CreateView):
    model = Medicine
    fields = ['name', 'brand_name', 'generic_name', 'price', 'is_generic']
    template_name = 'app/medicine_form.html'
    success_url = reverse_lazy('medicine_list')


class MedicineUpdateView(UpdateView):
    model = Medicine
    fields = ['name', 'brand_name', 'generic_name', 'price', 'is_generic']
    template_name = 'app/medicine_update.html'
    success_url = reverse_lazy('medicine_list')


class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'app/medicine_confirm_delete.html'
    success_url = reverse_lazy('medicine_list')

class OrderMedicineView(LoginRequiredMixin, View):
    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)

        inventory = Inventory.objects.filter(
            medicine=medicine,
            stock_quantity__gt=0
        ).first()

        if not inventory:
            messages.error(request, "Medicine is out of stock.")
            return redirect('medicine_list')

        order = Order.objects.create(
            user=request.user,
            pharmacy=inventory.pharmacy
        )

        OrderItem.objects.create(
            order=order,
            medicine=medicine,
            quantity=1,
            price=medicine.price
        )

        inventory.stock_quantity -= 1
        inventory.save()

        # ✅ SUCCESS MESSAGE
        messages.success(
            request,
            f"Your order for {medicine.name} has been placed successfully."
        )

        return redirect('medicine_list')
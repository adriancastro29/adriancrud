from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicine, Order, OrderItem, Inventory
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import OrderForm

class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class MedicineListView(ListView):
    model = Medicine
    template_name = 'app/medicine_list.html'
    context_object_name = 'medicines'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(brand_name__icontains=query) |
                Q(generic_name__icontains=query)
            )

        return queryset



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

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class OrderMedicineView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)

        inventory = Inventory.objects.filter(
            medicine=medicine,
            stock_quantity__gt=0
        ).first()

        if not inventory:
            messages.error(request, "Medicine is out of stock.")
            return redirect('medicine_list')

        form = OrderForm()

        return render(
            request,
            'app/order_form.html',
            {
                'medicine': medicine,
                'form': form
            }
        )

    def post(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        form = OrderForm(request.POST)

        inventory = Inventory.objects.filter(
            medicine=medicine,
            stock_quantity__gt=0
        ).first()

        if not inventory:
            messages.error(request, "Medicine is out of stock.")
            return redirect('medicine_list')

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.pharmacy = inventory.pharmacy
            order.total_amount = medicine.price
            order.save()

            OrderItem.objects.create(
                order=order,
                medicine=medicine,
                quantity=1,
                price=medicine.price
            )

            inventory.stock_quantity -= 1
            inventory.save()

            messages.success(
                request,
                "Order submitted successfully! We will contact you shortly."
            )
            return redirect('medicine_list')

        return render(
            request,
            'app/order_form.html',
            {
                'medicine': medicine,
                'form': form
            }
        )

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    HomePageView,
    AboutPageView,
    MedicineListView,
    MedicineDetailView,
    MedicineCreateView,
    MedicineUpdateView,
    MedicineDeleteView,
    OrderMedicineView,
    SignUpView,
)

urlpatterns = [
    # Pages
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),

    # Medicines
    path('medicines/', MedicineListView.as_view(), name='medicine_list'),
    path('medicines/add/', MedicineCreateView.as_view(), name='medicine_add'),
    path('medicines/<int:pk>/', MedicineDetailView.as_view(), name='medicine_detail'),
    path('medicines/<int:pk>/update/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('medicines/<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),
    path('medicines/<int:pk>/order/', OrderMedicineView.as_view(), name='medicine_order'),

    # Authentication (BUYER)
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', SignUpView.as_view(), name='signup'),
]

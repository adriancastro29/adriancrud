from django.urls import path
from .views import (
    HomePageView, AboutPageView,
    MedicineListView, MedicineDetailView,
    MedicineCreateView, MedicineUpdateView,
    MedicineDeleteView, OrderMedicineView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),

    path('medicines/', MedicineListView.as_view(), name='medicine_list'),
    path('medicines/add/', MedicineCreateView.as_view(), name='medicine_add'),
    path('medicines/<int:pk>/', MedicineDetailView.as_view(), name='medicine_detail'),
    path('medicines/<int:pk>/update/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('medicines/<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),
    path('medicines/<int:pk>/order/',OrderMedicineView.as_view(),name='medicine_order'
    ),
]

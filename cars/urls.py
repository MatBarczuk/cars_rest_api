from django.urls import path

from cars import views

app_name = 'cars'

urlpatterns = [
    path('cars/', views.ListCreateCar.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', views.DeleteCar.as_view(), name='car-delete'),
    path('rate/', views.RateCar.as_view(), name='car-rate'),
    path('popular/', views.PopularCar.as_view(), name='car-popular'),
]

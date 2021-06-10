from django.urls import path

from cars import views

urlpatterns = [
    path('cars/', views.CreateCar.as_view(), name='car-create'),
]

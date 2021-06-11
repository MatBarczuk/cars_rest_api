import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from cars.models import CarModel, CarMake, CarRate
from cars.serializers import CarSerializer, RateCarSerializer, PopularCarSerializer


class ListCreateCar(ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            makes_data = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json').json()[
                'Results']
            makes_list = []
            for make_name in makes_data:
                makes_list.append(make_name['Make_Name'].capitalize())

            if request.data['make'].capitalize() in makes_list:
                models_data = requests.get(
                    f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{request.data["make"]}?format=json').json()[
                    'Results']
                models_list = []
                for model_name in models_data:
                    models_list.append(model_name['Model_Name'].capitalize())

                if request.data['model'].capitalize() in models_list:
                    make = CarMake.objects.get_or_create(make=request.data['make'])
                    CarModel.objects.create(make=make[0], model=request.data['model'])
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(f'Model not found in external database ({request.data["model"]})',
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(f'Make not found in external database ({request.data["make"]})',
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCar(DestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer


class RateCar(CreateAPIView):
    queryset = CarRate.objects.all()
    serializer_class = RateCarSerializer

    def create(self, request, *args, **kwargs):
        serializer = RateCarSerializer(data=request.data)

        if serializer.is_valid():
            car = CarModel.objects.filter(id=request.data['car_id']).first()

            if car:
                CarRate.objects.create(car_id=car, rating=request.data['rating'])
                car.rates_number += 1
                all_rates = [rate.rating for rate in car.car_rate.all()]
                car.avg_rating = sum(all_rates) / car.rates_number
                car.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(f'No such car id ({request.data["car_id"]}) in database',
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PopularCar(ListAPIView):
    queryset = CarModel.objects.all().order_by('-rates_number')
    serializer_class = PopularCarSerializer

import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from cars.models import CarModel, CarMake
from cars.serializers import CarSerializer


class CreateCar(CreateAPIView):
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

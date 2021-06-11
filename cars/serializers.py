from rest_framework import serializers

from cars.models import CarModel, CarRate


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.make', required=True)

    class Meta:
        model = CarModel
        fields = ('id', 'make', 'model', 'avg_rating')
        read_only_fields = ['avg_rating']
        depth = 1


class RateCarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car.id', required=True)

    class Meta:
        model = CarRate
        fields = ('id', 'car_id', 'rating')
        depth = 1

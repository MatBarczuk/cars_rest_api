from rest_framework import serializers

from cars.models import CarModel


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.make', required=True)

    class Meta:
        model = CarModel
        fields = ('id', 'make', 'model')
        depth = 1

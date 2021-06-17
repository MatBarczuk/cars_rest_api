from django.test import TestCase

from cars.models import CarMake, CarModel, CarRate
from cars.serializers import CarSerializer, RateCarSerializer, PopularCarSerializer


class CarSerializerTest(TestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )
        self.data = CarSerializer(instance=self.car_model).data

    def test_fields(self):
        self.assertEqual(self.data.keys(), {'id', 'make', 'model', 'avg_rating'})

    def test_expected_values(self):
        self.assertEqual(self.data['id'], self.car_model.id)
        self.assertEqual(self.data['make'], self.car_model.make.make)
        self.assertEqual(self.data['model'], self.car_model.model)
        self.assertEqual(self.data['avg_rating'], self.car_model.avg_rating)


class PopularCarSerializerTest(TestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )
        self.data = PopularCarSerializer(instance=self.car_model).data

    def test_fields(self):
        self.assertEqual(self.data.keys(), {'id', 'make', 'model', 'rates_number'})

    def test_expected_values(self):
        self.assertEqual(self.data['id'], self.car_model.id)
        self.assertEqual(self.data['make'], self.car_model.make.make)
        self.assertEqual(self.data['model'], self.car_model.model)
        self.assertEqual(self.data['rates_number'], self.car_model.rates_number)

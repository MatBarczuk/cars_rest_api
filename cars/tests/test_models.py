from django.db import DataError
from django.test import TestCase

from cars.models import CarMake, CarModel, CarRate


class CarMakeTest(TestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )

    def test_car_make_fields(self):
        self.assertEqual(
            [*self.car_make.__dict__],
            ['_state', 'id', 'make']
        )

    def test_car_make_creation(self):
        self.assertTrue(isinstance(self.car_make, CarMake))
        self.assertEqual(self.car_make.make, 'test make')
        self.assertEqual(self.car_make.__str__(), 'Make: test make')

    def test_car_make_too_long(self):
        with self.assertRaises(DataError):
            CarMake.objects.create(
                make='t' * 51
            )


class CarModelTest(TestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )

    def test_car_model_fields(self):
        self.assertEqual(
            [*self.car_model.__dict__],
            ['_state', 'id', 'make_id', 'model', 'rates_number', 'avg_rating']
        )

    def test_car_model_creation(self):
        self.assertTrue(isinstance(self.car_model, CarModel))
        self.assertEqual(self.car_model.make.make, 'test make')
        self.assertEqual(self.car_model.model, 'test model')
        self.assertEqual(self.car_model.rates_number, 0)
        self.assertEqual(self.car_model.avg_rating, None)
        self.assertEqual(self.car_model.__str__(), 'Make: test make, model: test model')

    def test_car_model_too_long(self):
        with self.assertRaises(DataError):
            CarModel.objects.create(
                model='t' * 101
            )


class CarRateTest(TestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )
        self.car_rate = CarRate.objects.create(
            car_id=self.car_model,
            rating=3
        )

    def test_car_model_fields(self):
        self.assertEqual(
            [*self.car_rate.__dict__],
            ['_state', 'id', 'car_id_id', 'rating']
        )

    def test_car_rate_creation(self):
        self.assertTrue(isinstance(self.car_rate, CarRate))
        self.assertEqual(self.car_rate.car_id.model, 'test model')
        self.assertEqual(self.car_rate.rating, 3)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from cars.models import CarMake, CarModel
from cars.views import ListCreateCar

api_client = APIClient()
factory = APIRequestFactory()


class ListCreateCarTest(APITestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )

    def test_get_car_list(self):
        request = api_client.get(reverse('cars:car-list-create'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_post_car_valid_data(self):
        test_data = {
            "make": "Volkswagen",
            "model": "Golf"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        response = view(request)
        self.assertTrue(CarModel.objects.filter(model='Golf'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_car_invalid_make_key(self):
        test_data = {
            "invalid": "Volkswagen",
            "model": "Golf"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        response = view(request)
        self.assertFalse(CarModel.objects.filter(model='Golf'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_make_value(self):
        test_data = {
            "make": "invalid",
            "model": "Golf"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        response = view(request)
        self.assertFalse(CarModel.objects.filter(model='Golf'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_model_key(self):
        test_data = {
            "make": "Volkswagen",
            "invalid": "Golf"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        response = view(request)
        self.assertFalse(CarModel.objects.filter(model='Golf'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_model_value(self):
        test_data = {
            "make": "Volkswagen",
            "model": "invalid"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        response = view(request)
        self.assertFalse(CarModel.objects.filter(model='Golf'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_duplicate_car(self):
        test_data = {
            "make": "Volkswagen",
            "model": "Golf"
        }
        request = factory.post(reverse('cars:car-list-create'), data=test_data)
        duplicate_request = factory.post(reverse('cars:car-list-create'), data=test_data)
        view = ListCreateCar.as_view()
        view(request)
        duplicate_response = view(duplicate_request)
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteCarTest(APITestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            id=123,
            make=self.car_make,
            model='test model'
        )

    def test_delete_car(self):
        request = api_client.delete(f'/cars/{self.car_model.id}/')
        self.assertFalse(CarModel.objects.filter(model='test model'))
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_existing_car(self):
        request = api_client.delete(f'/cars/456/')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


class RateCarTest(APITestCase):
    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            id=1,
            make=self.car_make,
            model='test model'
        )

    def test_add_single_rate(self):
        test_rate = {
            "car_id": 1,
            "rating": 3
        }
        response = api_client.post(reverse('cars:car-rate'), test_rate)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_rate_twice(self):
        test_rate1 = {
            "car_id": 1,
            "rating": 3
        }
        test_rate2 = {
            "car_id": 1,
            "rating": 5
        }
        response1 = api_client.post(reverse('cars:car-rate'), test_rate1)
        response2 = api_client.post(reverse('cars:car-rate'), test_rate2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_add_invalid_rate(self):
        test_rate = {
            "car_id": 1,
            "rating": 50
        }
        response = api_client.post(reverse('cars:car-rate'), test_rate)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rate_for_not_existing_car(self):
        test_rate = {
            "car_id": 124,
            "rating": 3
        }
        response = api_client.post(reverse('cars:car-rate'), test_rate)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PopularCarTest(APITestCase):

    def setUp(self):
        self.car_make = CarMake.objects.create(
            make='test make'
        )
        self.car_model = CarModel.objects.create(
            make=self.car_make,
            model='test model'
        )

    def test_get_car_list(self):
        request = api_client.get(reverse('cars:car-popular'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

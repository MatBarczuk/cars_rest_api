from django.db import models


class CarMake(models.Model):
    make = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'Make: {self.make}'


class CarModel(models.Model):
    make = models.ForeignKey('CarMake', related_name='car_model', on_delete=models.CASCADE)
    model = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f'Make: {self.make.make}, model: {self.model}'


class CarRate(models.Model):
    car = models.ForeignKey('CarModel', related_name='car_rate', on_delete=models.CASCADE)

    RATE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    rate = models.PositiveIntegerField(choices=RATE_CHOICES)
    rates_number = models.PositiveIntegerField(default=0)
    rates_sum = models.PositiveIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1)

# Cars REST API

Django Rest application for car storage with rating cars functionality.

## How to run

1. You have to have `docker` and `docker-composed` installed on your device.
2. Run command `docker-compose up --build` in terminal.
3. Open browser with url `http://0.0.0.0:8000/cars` or `http://127.0.0.1:8000/cars` if you are using Windows.
4. To run tests, run command `docker-compose exec web python manage.py test`.

## Endpoints

1. `/cars` - returns list of all cars and gives possibility to add new car to the database (methods: GET, POST).
2. `/cars/{id}` - delete car with given `id` from database (method: DELETE).
3. `/rate` - gives possibility to rate car (method: POST).
4. `/popular` - returns list of all cars sorted by the rates amount (method: GET).

## Licence

```text
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
 * ----------------------------------------------------------------------------
```
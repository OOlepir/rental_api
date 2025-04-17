import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_project.settings')
django.setup()

from users.models import User
from bookings.models import Booking
from faker import Faker
from datetime import datetime, timedelta
from random import randint, choice, uniform
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from properties.models import Location, Property, PropertyType

fake = Faker()

# users = []
# hashed_password = make_password("password")
#
#
#
# for _ in range(10):
#     username = fake.user_name()
#     email = fake.unique.email()
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     user_type = 'landlord'
#
#
#
#     user = User(
#         email=email,
#         first_name=first_name,
#         last_name=last_name,
#         username = username,
#         password=hashed_password,
#         user_type=user_type,
#     )
#     users.append(user)
#
#
# for _ in range(90):
#     username = fake.user_name()
#     email = fake.unique.email()
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     user_type = 'tenant'
#
#
#
#     user = User(
#         email=email,
#         first_name=first_name,
#         last_name=last_name,
#         password=hashed_password,
#         username = username,
#         user_type=user_type,
#     )
#     users.append(user)
#
# User.objects.bulk_create(users)


# deutsche_städte = [
#     "Berlin",
#     "München",
#     "Hamburg",
#     "Köln",
#     "Frankfurt am Main",
#     "Stuttgart",
#     "Düsseldorf",
#     "Dresden",
#     "Leipzig",
#     "Nürnberg"
# ]
#
# for i in range(10):
#     location = Location.objects.create(
#         city = choice(deutsche_städte),
#         address=fake.address(),
#     )
#     location.save()


#
# p1 = PropertyType(name='Квартира')
# p2 = PropertyType(name='Дом')
# p3 = PropertyType(name='Отель')
#
# PropertyType.objects.bulk_create([p1, p2, p3])

#
# property_types = PropertyType.objects.all()
# owners = User.objects.filter(user_type='landlord')
# locations = Location.objects.all()
# for owner in owners:
#     property = Property.objects.create(
#         owner=owner,
#         title=fake.text(),
#         description=fake.text(),
#         location=choice(locations),
#         property_type = choice(property_types),
#         price = randint(1, 100),
#         rooms = randint(1, 8),
#         area = randint(15, 300),
#         status = 'active'
#
#     )
#     property.save()


# def generate_random_dates():
#     # Генерируем случайное количество дней в промежутке от -120 до -30
#     days_offset = randint(0, 120)
#     date_from = datetime.now().date() + timedelta(days=days_offset)  # Начальная дата
#     date_to = date_from + timedelta(days=randint(1, 6))  # Срок аренды от 1 до 6 дней
#
#     return date_from, date_to
#
#
# properties = Property.objects.all()
# tenants = User.objects.filter(user_type='tenant')
#
# for _ in range(500):
#     check_in_date, check_out_date = generate_random_dates()
#     try:
#         days_offset = randint(0, 120)
#         booking = Booking.objects.create(
#             property = choice(properties),
#             tenant = choice(tenants),
#             check_in_date = check_in_date,
#             check_out_date = check_out_date,
#             guests_count = randint(1, 10),
#             notes = fake.text(),
#         )
#         booking.save()
#     except Exception as e:
#         print(e)
#     else:
#         print(booking)


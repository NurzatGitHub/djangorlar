from typing import Any, List
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password
from faker import Faker
from decimal import Decimal
from random import choice, randint
from apps.users.models import CustomUser, DEPARTMENT_CHOICES, ROLE_CHOICES

fake = Faker()


class Command(BaseCommand):
    help = "Generate N fake users. Usage: python manage.py generate_users --count 10000 --batch 1000"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10000)
        parser.add_argument('--batch', type=int, default=1000)

    def handle(self, *args: Any, **options: Any) -> None:
        total = options['count']
        batch_size = options['batch']

        # precompute hashed password to avoid hashing inside loop
        hashed_password = make_password("12345")
        created = 0
        users_buffer: List[CustomUser] = []

        departments = [d[0] for d in DEPARTMENT_CHOICES]
        roles = [r[0] for r in ROLE_CHOICES]

        for i in range(total):
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            username = f"{first.lower()}{last.lower()}{i}"
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = choice(departments)
            role = choice(roles)
            # birth_date random between 1975 and 2005
            year = randint(1975, 2005)
            month = randint(1, 12)
            day = randint(1, 28)
            birth_date = timezone.datetime(year, month, day).date()
            salary = Decimal(randint(100000, 1000000))

            user = CustomUser(
                email=email,
                username=username,
                first_name=first,
                last_name=last,
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                salary=salary,
                is_active=True,
                is_staff=(role == 'admin'),
                password=hashed_password,
            )
            users_buffer.append(user)

            if len(users_buffer) >= batch_size:
                CustomUser.objects.bulk_create(users_buffer)
                created += len(users_buffer)
                self.stdout.write(self.style.SUCCESS(f"Inserted {created}/{total} users"))
                users_buffer = []

        # remaining
        if users_buffer:
            CustomUser.objects.bulk_create(users_buffer)
            created += len(users_buffer)
            self.stdout.write(self.style.SUCCESS(f"Inserted {created}/{total} users"))

        self.stdout.write(self.style.SUCCESS("Done."))

from django.core.management.base import BaseCommand
from apps.restaurant.models import (
    User, Restaurant, Address, MenuItem, Category, ItemCategory,
    Option, ItemOption, Order, OrderOption, PromoCode, OrderPromo
)
from django.utils import timezone
import random
from decimal import Decimal

class Command(BaseCommand):
    help = "Generate 20 test data records for each model"

    def handle(self, *args, **options):
        # Очистка таблиц (для повторных запусков)
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        Address.objects.all().delete()
        MenuItem.objects.all().delete()
        Category.objects.all().delete()
        ItemCategory.objects.all().delete()
        Option.objects.all().delete()
        ItemOption.objects.all().delete()
        Order.objects.all().delete()
        OrderOption.objects.all().delete()
        PromoCode.objects.all().delete()
        OrderPromo.objects.all().delete()

        # Users
        users = []
        for i in range(1, 21):
            user = User.objects.create(name=f'User {i}', password='password123')
            users.append(user)

        # Restaurants
        restaurants = []
        for i in range(1, 21):
            r = Restaurant.objects.create(
                name=f'Restaurant {i}',
                description='Delicious food and cozy place',
                address=f'Street {i}, City',
                phone=f'+7700{i:07}'
            )
            restaurants.append(r)

        # Categories
        categories = []
        for i in range(1, 21):
            c = Category.objects.create(name=f'Category {i}')
            categories.append(c)

        # Menu items
        menu_items = []
        for i in range(1, 21):
            mi = MenuItem.objects.create(
                restaurant=random.choice(restaurants),
                name=f'Item {i}',
                base_price=Decimal(random.randint(1000, 5000)) / 100,
                is_available=True
            )
            menu_items.append(mi)

        # ItemCategory (many-to-many)
        for mi in menu_items:
            cats = random.sample(categories, 3)
            for j, c in enumerate(cats):
                ItemCategory.objects.create(menu_item=mi, category=c, position=j)

        # Options
        options = []
        for i in range(1, 21):
            opt = Option.objects.create(
                name=f'Option {i}',
                additional_price=Decimal(random.randint(50, 500)) / 100
            )
            options.append(opt)

        # ItemOption
        for mi in menu_items:
            opt = random.choice(options)
            ItemOption.objects.create(
                option=opt,
                price_delta=opt.additional_price,
                is_default=random.choice([True, False])
            )

        # Orders
        orders = []
        for i in range(1, 21):
            o = Order.objects.create(
                user=random.choice(users),
                menu_item=random.choice(menu_items),
                item_name=f'Order Item {i}',
                item_price=Decimal(random.randint(500, 1500)) / 100,
                quantity=random.randint(1, 5)
            )
            orders.append(o)

        # OrderOptions
        for o in orders:
            OrderOption.objects.create(
                order_item=o,
                option_name='Extra Cheese',
                price_delta=Decimal('0.50')
            )

        # PromoCodes
        promos = []
        for i in range(1, 21):
            p = PromoCode.objects.create(
                code=f'PROMO{i}',
                discount_percent=Decimal(random.randint(5, 30)),
                valid_from=timezone.now(),
                valid_to=timezone.now() + timezone.timedelta(days=30),
                is_active=True
            )
            promos.append(p)

        # OrderPromo
        for o in orders:
            promo = random.choice(promos)
            OrderPromo.objects.create(
                order=o,
                promo_code=promo,
                applied_discount=Decimal(random.randint(10, 100)) / 10
            )

        self.stdout.write(self.style.SUCCESS("Successfully added 20 test data for each model!"))

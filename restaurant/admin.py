from django.contrib import admin

# Register your models here.
from .models import (
    User, Restaurant, Address, MenuItem, Category,
    ItemCategory, Option, ItemOption, Order, PromoCode, OrderPromo
    )

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Address)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(ItemCategory)
admin.site.register(Option)
admin.site.register(ItemOption)
admin.site.register(Order)
admin.site.register(PromoCode)
admin.site.register(OrderPromo)
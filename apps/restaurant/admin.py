from django.contrib import admin
from .models import Restaurant, MenuItem, Option, ItemOption, Order, OrderOption, PromoCode, OrderPromo

# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address', 'phone')
    search_fields = ('name', 'address', 'phone')
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):   
    list_display = ('name', 'restaurant', 'base_price', 'is_available')
    list_filter = ('restaurant', 'is_available')
    search_fields = ('name',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'additional_price')
    search_fields = ('name',)
    
@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'price_delta', 'is_default')
    search_fields = ('option__name',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'quantity')
    list_filter = ('user',)
    search_fields = ('item_name',)
    
@admin.register(OrderOption)
class OrderOptionAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'option_name', 'price_delta')
    list_filter = ('order_item',)
    search_fields = ('option_name',)
    
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to')
    search_fields = ('code',)

@admin.register(OrderPromo)
class OrderPromoAdmin(admin.ModelAdmin):
    list_display = ('order', 'promo_code', 'applied_discount')
    list_filter = ('promo_code',)
    search_fields = ('order__item_name', 'promo_code__code')



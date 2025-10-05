from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    phone = models.TextField()
    
    def __str__(self):
        return self.name
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.TextField()
    
    def __str__(self):
        return f"{self.city}, {self.street}, {self.house_number}"
    

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class ItemCategory(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.IntegerField()
    

class Option(models.Model):
    name = models.CharField(max_length=255)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
class ItemOption(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    item_name = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)


class OrderOption(models.Model):
    order_item = models.ForeignKey(Order, on_delete=models.CASCADE)
    option_name = models.TextField()
    price_delta = models.DecimalField(max_digits=10, decimal_places=2)

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"

class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    applied_discount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order {self.order.id} - Promo {self.promo_code.code}"
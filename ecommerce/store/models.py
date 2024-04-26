from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, max_length=200, null=True, blank=True, on_delete=models.CASCADE)


class Category(models.Model): #EX: (Masc, Fem, Kids)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class CategoryType(models.Model): #EX: (T-shirt, Jacket, Underwear)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category_id = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    categorytype_id = models.ForeignKey(CategoryType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.name} / {self.category_id} / {self.categorytype_id} / {self.price}"


class StockItem(models.Model):
    product_id = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    quant = models.IntegerField(default=0)


class Address(models.Model):
    client_id = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    street = models.CharField(max_length=400, null=True, blank=True)
    number = models.IntegerField(default=0)
    complement = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

class Order(models.Model):
    client_id = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    finished = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(null=True, blank=True)
    transaction_code = models.CharField(max_length=200, null=True, blank=True)

class OrderItems(models.Model):
    order_id =  models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    stockitem_id = models.ForeignKey(StockItem, null=True, blank=True, on_delete=models.SET_NULL)
    quant = models.IntegerField(default=0)

class Banner(models.Model):
    image = models.ImageField(null=True, blank=True)
    link = models.CharField(max_length=400, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.link} - Active: {self.active}"
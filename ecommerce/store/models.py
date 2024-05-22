from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=200, null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, max_length=200, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.email)


class Category(models.Model): #EX: (Masc, Fem, Kids)
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class CategoryType(models.Model): #EX: (T-shirt, Jacket, Underwear)
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    categorytype = models.ForeignKey(CategoryType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.name} / {self.category} / {self.categorytype} / {self.price} / Active:{self.active}"


class Color(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    color_code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class StockItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=20, null=True, blank=True)
    quant = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product.name} / Size: {self.size} / Color: {self.color.name} / Quant: {self.quant}"


class Address(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=400, null=True, blank=True)
    number = models.IntegerField(default=0)
    complement = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.client} / {self.description} / {self.street}, {self.number} - {self.city}-{self.state}"

class Order(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    finished = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(null=True, blank=True)
    transaction_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f"Order_id: {self.id} / {self.client.email} / Finished: {self.finished}"
    
    @property
    def total_price(self):
        all_itens = OrderItems.objects.filter(order__id=self.id)
        total = sum([item.total_price for item in all_itens])
        return total


class OrderItems(models.Model):
    order =  models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    stockitem = models.ForeignKey(StockItem, null=True, blank=True, on_delete=models.SET_NULL)
    quant = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Order Nº: {self.order.id} / {self.stockitem.product.name} - {self.stockitem.size} - {self.stockitem.color.name} - Quant: {self.quant}"

    @property
    def total_price(self):
        return self.quant * self.stockitem.product.price


class Banner(models.Model):
    image = models.ImageField(null=True, blank=True)
    link = models.CharField(max_length=400, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.link} - Active: {self.active}"
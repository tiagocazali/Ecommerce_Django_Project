from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Category)
admin.site.register(CategoryType)
admin.site.register(Product)
admin.site.register(StockItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Banner)


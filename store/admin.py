from django.contrib import admin
from .models import Product, Customer, Category, Order, Contact,Grades, PromoVideo, Picture
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(Grades)
admin.site.register(PromoVideo)
admin.site.register(Picture)
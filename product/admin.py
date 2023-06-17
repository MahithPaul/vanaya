from django.contrib import admin
from .models import *
# Register your models here.

#1:31:09:- Adding images/price/description in the service page. 
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
class TitleImageAdmin(admin.StackedInline):
    model = TitleImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin,TitleImageAdmin]

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
admin.site.register(TitleImage)
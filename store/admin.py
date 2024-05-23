from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductType,
)

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(ProductType)
# Inline giúp quản trị viên quản lý các đối tượng liên quan trực tiếp trong cùng một trang.



class ProductImageInline(admin.TabularInline):
    model = ProductImage



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
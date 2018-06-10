from django.contrib import admin

# Register your models here.
from .models import Product, Store, ProductExtra

admin.site.register(Store)


class ExtraInline(admin.StackedInline):
    model = ProductExtra


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [
        ExtraInline,
    ]

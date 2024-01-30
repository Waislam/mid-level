from django.contrib import admin
from .models import ProductVariantPrice, Variant, ProductVariant

# Register your models here.
admin.site.register(ProductVariantPrice)
admin.site.register(Variant)
admin.site.register(ProductVariant)

from django.contrib import admin
from .models import (
     Supplier, Category, Product,
    Sale, SaleItem, PurchaseOrder, PurchaseOrderItem
)

# الطريقة البسيطة والمباشرة تماماً:

admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
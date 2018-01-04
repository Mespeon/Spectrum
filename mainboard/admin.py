from django.contrib import admin
from django.db import connection
from .models import *

class StoreAdmin(admin.ModelAdmin):
	list_display = ('store_code', 'store_name', 'store_region', 'store_address')
	fields = ['store_code', 'store_name', 'store_region', 'store_address']

class ProductAdmin(admin.ModelAdmin):
	list_display = ('item_SKU', 'item_name', 'item_unit_price', 'item_retail_price')
	
class SalesAdvAdmin(admin.ModelAdmin):
	list_display = ('invoiceNumber', 'invoiceDate', 'store', 'adviceCreator', 'adviceCreateDate', 'adviceEditor', 'adviceEditDate')
	
class SalesAdvItmAdmin(admin.ModelAdmin):
	list_display = ('invoiceNumber', 'item', 'itemQty')
	
class SalesReportAdmin(admin.ModelAdmin):
	pass

admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SalesAdvice, SalesAdvAdmin)
admin.site.register(SalesAdviceItems, SalesAdvItmAdmin)
admin.site.register(SalesReport, SalesReportAdmin)
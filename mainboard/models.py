from django.db import models
from django import forms
from django.forms import ModelForm, inlineformset_factory
import pytz
import datetime

# Create your models here.

class Store(models.Model):
	store_code = models.CharField(max_length=4, unique=True)
	store_name = models.CharField(max_length=100)
	store_region = models.CharField(max_length=70)
	store_address = models.TextField(max_length=255)

	def __str__(self):
		return self.store_code
		return self.store_name
		return self.store_region
		return self.store_address

class Product(models.Model):
	item_SKU = models.IntegerField(unique=True)
	item_name = models.CharField(max_length=70)
	item_unit_price = models.FloatField()
	item_retail_price = models.FloatField()

	def __str__(self):
		return self.item_name

class SalesAdvice(models.Model):
	invoiceNumber = models.CharField(max_length=20, default='', unique=True)
	invoiceDate = models.DateField()
	apBatchNumber = models.CharField(max_length=20, default='')
	paymentDueDate = models.DateField()
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	adviceCreator = models.CharField(max_length=50, null=True)
	adviceCreateDate = models.DateField()
	adviceEditor = models.CharField(max_length=50, null=True)
	adviceEditDate = models.DateField(null=True)
	totalAmtPayable = models.IntegerField(default=0)
	totalItemQty = models.IntegerField(default=0)
	adviceStatus = models.CharField(max_length=50, default='FOR APPROVAL')

	def __str__(self):
		return self.invoiceNumber
		return self.store
		return self.adviceCreator
		return self.adviceEditor
		return self.adviceStatus

class SalesAdviceItems(models.Model):
	invoiceNumber = models.ForeignKey(SalesAdvice, on_delete=models.CASCADE)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	itemQty = models.IntegerField(default=0)
	itemUnitCost = models.FloatField(default=0)
	itemCost = models.FloatField(default=0)

class ReceivingAdvice(models.Model):
	receiptNumber = models.CharField(max_length=20, default='', unique=True)
	receiptDate = models.DateField()
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	adviceCreator = models.CharField(max_length=50, null=True)
	adviceCreateDate = models.DateField()
	adviceEditor = models.CharField(max_length=50, null=True)
	adviceEditDate = models.DateField(null=True)
	adviceStatus = models.CharField(max_length=50, default='FOR APPROVAL')

class ReceivingAdviceItems(models.Model):
	receiptNumber = models.ForeignKey(ReceivingAdvice, on_delete=models.CASCADE)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	itemQty = models.IntegerField(default=0)
	itemUnitCost = models.FloatField(default=0)
	itemCost = models.FloatField(default=0)

"""
class EditAdviceItemQty(ModelForm):
	class Meta:
		model = SalesAdviceItems
		fields = ['itemQty']
"""

class SalesReport(models.Model):
	invoiceNumber = models.ForeignKey(SalesAdvice, on_delete=models.CASCADE)
	reportGeneratedDate = models.DateField()

from django.core import serializers
from django.shortcuts import *
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.utils import timezone
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from decimal import *
from math import *

import datetime
import pytz

from .models import *
from .forms import *

def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/mainboard/dashboard')
	else:
		return HttpResponseRedirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def dashboard(request):
	business_date = timezone.now()
	store_count	= Store.objects.count()
	item_count = Product.objects.count()
	salesadv_count = SalesAdvice.objects.count()
	rcvadv_count = ReceivingAdvice.objects.count()
	store_latest = Store.objects.latest('id')
	item_latest = Product.objects.latest('id')
	salesadv_latest = SalesAdvice.objects.latest('id')
	rcvadv_latest = ReceivingAdvice.objects.latest('id')

	context = {
		'store_count': store_count,
		'store_latest': store_latest,
		'item_latest': item_latest,
		'salesadv_latest': salesadv_latest,
		'rcvadv_latest': rcvadv_latest,
		'item_count': item_count,
		'salesadv_count': salesadv_count,
		'rcvadv_count': rcvadv_count,
		'businessdate': business_date,
	}
	return render(request, 'mainboard/dashboard.html', context)

@login_required(login_url='/accounts/login/')
def data(request):
	section_header = 'Data Management'
	context = {
		'section_header': section_header
	}
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def inventory(request):
	section_header = 'Inventory Management'
	context = {
		'section_header': section_header,
	}
	return render(request, 'mainboard/inventory.html', context)

@login_required(login_url='/accounts/login/')
def addStore(request):
	addStore = '&nbsp;'
	section_header = 'Add New Store'

	if request.method == 'POST':
		form = AddStoreForm(request.POST)
		if form.is_valid():
			newStore = form.save()
			store_success = 'Successfully added Store'
			request.session['store_success_message'] = store_success
			return HttpResponseRedirect(reverse('storeAll'))
		else:
			return HttpResponse(str(form.errors))
	else:
		form = AddStoreForm()

	context = {
		'addStore': addStore,
		'section_header': section_header,
		'form': form,
	}

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def editStore(request, store_code):
	prefix_text = 'Editing Store'
	store_code = store_code
	section_header = ' '.join([prefix_text, str(store_code)])
	editStore = '&nbsp;'

	#Check if page is requested using POST or GET
	if request.method == 'POST':
		#Create a form copy
		form = EditStoreForm(request.POST)

		#Check form if valid then pass new values to table
		if form.is_valid():
			#Get row to update
			thisStore = Store.objects.get(store_code=store_code)
			if thisStore is not None:
				#Pass values from form to model field
				thisStore.store_name = request.POST['store_name']
				thisStore.store_region = request.POST['store_region']
				thisStore.store_address = request.POST['store_address']

				#Push values
				thisStore.save()

				#Generate success message
				editStore_success = 'Store detail successfully updated.'
				request.session['store_success_message'] = editStore_success
				return HttpResponseRedirect(reverse('storeAll'))
		else:
			return HttpResponse(str(form.errors))
	else:
		#Get initial values by fetching store data from table using store_code
		#Pass these values to the form fields
		thisStore = Store.objects.get(store_code=store_code)
		form = EditStoreForm(initial={
			'store_code': thisStore.store_code,
			'store_name': thisStore.store_name,
			'store_region': thisStore.store_region,
			'store_address': thisStore.store_address, })

	context = {
		'section_header': section_header,
		'editStore': editStore,
		'form': form,
	}

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def deleteStore(request, store_code):
	store_code = store_code

	#Get store to delete
	thisStore = Store.objects.get(store_code=store_code)
	try:
		thisStore.delete()

		#Generate success message
		remove_success = "Store successfully removed."
		request.session['store_success_message'] = remove_success
		return HttpResponseRedirect(reverse('storeAll'))
	except:
		return HttpResponse("Store removal failed.")

@login_required(login_url='/accounts/login/')
def store(request, store_code):
	#Get store instance based from store code passed from URL
	thisStore = Store.objects.get(store_code=store_code)
	thisStoreId = thisStore.id
	thisStoreName = thisStore.store_name
	store = store_code
	section_header = ' '.join([str(store), thisStoreName])

	#Get product instance
	thisStoreItems = Product.objects.all()

	#Get sales advice instance
	thisStoreSalesAdvices = SalesAdvice.objects.filter(store_id=thisStoreId)

	#Get receiving advice instance
	thisStoreReceivingAdvices = ReceivingAdvice.objects.filter(store_id=thisStoreId)

	context = {
		'store': store,
		'section_header': section_header,
		'storeDetails': thisStore,
		'allItems': thisStoreItems,
		'allSalesAdvices': thisStoreSalesAdvices,
		'allRcvAdvices': thisStoreReceivingAdvices,
	}
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def storeAll(request):
	section_header = 'Stores'
	try:
		success = request.session.get('store_success_message')
	except KeyError:
		success = 'No new stores added'

	all_stores = Store.objects.filter().order_by('-id')
	context = {
		'section_header': section_header,
		'store_view_all': all_stores,
		'success': success
	}

	try:
		del request.session['store_success_message']
	except KeyError:
		pass
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def addItem(request):
	addItem = '&nbsp;'
	section_header = 'Add New Item'
	form = AddItemForm()

	context = {
		'addItem': addItem,
		'section_header': section_header,
		'form': form,
	}

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def editItem(request, item_SKU):
	editItem = '&nbsp;'
	itemSKU = item_SKU
	header_prefix = 'Editing Item'
	section_header = ' '.join([header_prefix, str(itemSKU)])

	#Determine if page is requested using GET or POST
	if request.method == 'POST':
		pass
	else:
		#Get product instance
		thisItem = Product.objects.get(item_SKU=itemSKU)
		form = EditItem(initial={'item_name':thisItem.item_name, 'item_unit_price':thisItem.item_unit_price, 'item_retail_price':thisItem.item_retail_price})

	context = {
		'editItem': editItem,
		'section_header': section_header,
		'form': form,
	}

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def removeItem(request, item_SKU):
	pass

@login_required(login_url='/accounts/login/')
def item(request, item_SKU):
	viewItem = '&nbsp;'
	itemSKU = item_SKU

	thisItem = Product.objects.get(item_SKU=itemSKU)
	item_sku = thisItem.item_SKU
	item_name = thisItem.item_name
	item_longname = ' '.join([str(item_sku), item_name])

	context = {
		'viewItem': viewItem,
		'section_header': item_longname,
		'item': thisItem,
	}
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def itemAll(request):
	section_header = 'Items'
	all_items = Product.objects.all()
	context = {
		'section_header': section_header,
		'item_view_all': all_items
	}
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def salesadvAll(request):
	section_header = 'Sales Advices'
	try:
		success = request.session.get('advice_success_message')
	except KeyError:
		success = 'No new advices added'

	all_advices = SalesAdvice.objects.filter().order_by('-invoiceDate')

	context = {
		'section_header': section_header,
		'salesadv_view_all': all_advices,
		'success': success
	}

	try:
		del request.session['advice_success_message']
	except KeyError:
		pass
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def addAdv(request):
	addAdv = '&nbsp;'
	business_date = datetime.datetime.now().date
	section_header = 'Create Sales Advice'

	#CHECK IF PAGE IS REQUESTED USING A POST METHOD OR NOT
	if request.method == 'POST':
		form = AddAdviceForm(request.POST)
		if form.is_valid():
			#newAdvice = form.save(commit=False)
			#newAdvice.adviceCreator = request.POST['adviceCreator']
			#newAdvice.adviceCreateDate = request.POST['adviceCreateDate']

			#Save new advice form into database
			newAdvice = form.save()

			#AUTO GENERATE ROWS IN SALES ADVICE ITEMS TABLE WITH ID DATA FROM SALES ADVICE TABLE
			#Get primary key of latest entry created
			thisAdviceId = SalesAdvice.objects.filter().order_by('-id')[0]
			adviceId = thisAdviceId.id

			#Get item count
			productInstance = Product.objects.all()	#instance declaration for Product model
			thisCount = productInstance.count()	#count all items in Product model

			#INSERT NEW ROWS USING DATA FETCHED FROM BOTH SALES ADVICE AND PRODUCT TABLES
			#LOOP THIS CODE ACCORDING TO PRODUCT COUNT
			for x in range(0, thisCount):
				#Get Item Detail
				item = Product.objects.get(id=x+1)	#range 0 + 1 i.e. 0+1(1), 1+1(2) ....

				#INSERT ROWS
				row = SalesAdviceItems(invoiceNumber_id=adviceId, item_id=item.id, itemQty=0, itemCost=0, itemUnitCost=item.item_unit_price)
				row.save()

			#Generate Success Message
			advice_success = "Successfully created Sales Advice."
			request.session['advice_success_message'] = advice_success

			return HttpResponseRedirect(reverse('salesAdvAll'))
		else:
			error = form.errors
			form = AddAdviceForm(initial={'adviceCreateDate':datetime.date.today, 'adviceCreator':' '.join([request.user.first_name, request.user.last_name])})

			context = {
				'section_header': section_header,
				'businessdate': business_date,
				'addAdv': addAdv,
				'error': error,
				'form': form,
			}
			return render(request, 'mainboard/data.html', context)
	else:
		form = AddAdviceForm(initial={'adviceCreateDate':datetime.date.today, 'adviceCreator':' '.join([request.user.first_name, request.user.last_name])})

	context = {
		'section_header': section_header,
		'addAdv': addAdv,
		'businessdate': business_date,
		'form': form,
	}
	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def salesAdv(request, invoiceNumber):
	request_invoice = invoiceNumber
	try:
		success = request.session.get('editAdvice_success_message')
	except KeyError:
		success = "No changes made."

	#GET ALL INVOICE DATA
	for sacode in SalesAdvice.objects.raw('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_store ON mainboard_salesadvice.store_id = mainboard_store.id WHERE mainboard_salesadvice.invoiceNumber="'+request_invoice+'"'):
		invoiceNumber = str(sacode.invoiceNumber)
		invoiceDate = str(sacode.invoiceDate)
		paymentDueDate = str(sacode.paymentDueDate)
		storeCode = str(sacode.store_code)
		storeName = str(sacode.store_name)
		apBatchNumber = str(sacode.apBatchNumber)
		adviceCreateDate = str(sacode.adviceCreateDate)
		adviceCreator = str(sacode.adviceCreator)
		adviceEditDate = str(sacode.adviceEditDate)
		adviceEditor = str(sacode.adviceEditor)
		adviceStatus = str(sacode.adviceStatus)

	salesAdv_detail = ''
	advice_created = ', '.join([adviceCreator, adviceCreateDate])
	advice_edited = ', '.join([adviceEditor, adviceEditDate])

	#Determine if advice is approved or not.
	if adviceStatus == 'APPROVED':
		approved = "Advice is marked APPROVED."
	else:
		approved = ''

	#GET ALL ITEMS RELATIVE TO THE INVOICE NUMBER
	item_list = SalesAdvice.objects.raw('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_salesadviceitems ON mainboard_salesadvice.id = mainboard_salesadviceitems.invoiceNumber_id LEFT JOIN mainboard_product ON mainboard_salesadviceitems.item_id = mainboard_product.id WHERE mainboard_salesadvice.invoiceNumber="'+request_invoice+'"')

	#COUNT ALL ITEMS
	for count in SalesAdvice.objects.raw('SELECT *, SUM(itemQty) AS itemCount, SUM(itemCost) AS itemCost FROM mainboard_salesadvice LEFT JOIN mainboard_salesadviceitems ON mainboard_salesadvice.id = mainboard_salesadviceitems.invoiceNumber_id LEFT JOIN mainboard_product ON mainboard_salesadviceitems.item_id = mainboard_product.id WHERE mainboard_salesadvice.invoiceNumber="'+request_invoice+'"'):
		item_count = count.itemCount
		item_cost = '{:.4f}'.format(count.itemCost)

	context = {
		'section_header': ' : '.join([invoiceNumber, storeName]),
		'salesAdv_detail': invoiceNumber,
		'invoiceNumber': invoiceNumber,
		'invoiceDate': invoiceDate,
		'paymentDueDate': paymentDueDate,
		'storeCode': storeCode,
		'apBatchNumber': apBatchNumber,
		'storeName': storeName,
		'adviceCreated': advice_created,
		'adviceEdited': advice_edited,
		'adviceStatus': adviceStatus,
		'item_list': item_list,
		'itemQty': item_count,
		'amtPayable': item_cost,
		'success': success,
		'approved': approved,
	}

	try:
		del request.session['editAdvice_success_message']
	except KeyError:
		pass

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def editAdv(request, invoiceNumber):
	section_header = ' '.join(['Editing Advice', invoiceNumber])
	editAdv = '&nbsp;'
	invNum = invoiceNumber

	#Check if page is requested using POST or GET
	if request.method == 'POST':
		#Get row count from Product model
		getCount = Product.objects.all()
		count = getCount.count()

		#Get invoiceNumber_id of current advice
		thisAdvice = SalesAdvice.objects.get(invoiceNumber=invNum)
		thisAdviceId = thisAdvice.id

		#BEGIN PASSING VALUES FOR SALES ADVICE ITEMS
		#Pass values from POST fields to the specific target rows based on item_id AND invoiceNumber_id.
		#This should always be sequentially numbered since items are arranged by id ascending and invoiceNumber is passed through context.
		#Loop the value assignment and table update using the count from Product table.
		#This should be also correct every time since the rows were created using the count from Product table.
		for y in range(0, count):
			#Get row to update
			item_row = SalesAdviceItems.objects.get(invoiceNumber_id=thisAdviceId, item_id=y+1)

			#Determine on which field is to be assigned to the table field.
			prefix_name = 'qty-for-item-'
			row_num = y+1
			field_id = ''.join([prefix_name, str(row_num)])
			item_qty = request.POST.get(field_id)
			item_row.itemQty = item_qty	#Assign value to item quantity.

			#Calculate updated itemCost based from itemUnitCost * itemQty
			unit_cost = item_row.itemUnitCost
			item_cost = unit_cost * float(item_qty)
			format_cost = '{:.2f}'.format(item_cost)	#This will format the cost to X.YY with ceiling/flooring.
			item_row.itemCost = format_cost				#Assign value to item cost.

			#Push all changes
			item_row.save()

		#PASS VALUES FOR SALES ADVICE EDITOR / EDIT DATE
		editor = str(' '.join([request.user.first_name, request.user.last_name]))
		print(editor)
		thisAdvice.adviceEditor = editor
		dateToday = timezone.now().date()
		print(dateToday)
		thisAdvice.adviceEditDate = dateToday
		thisAdvice.save()	#Push changes

		#Generate Success Message
		advice_edit_success = "Successfully edited Sales Advice."
		request.session['editAdvice_success_message'] = advice_edit_success

		reverse_link = '/mainboard/data/salesadvice/'
		reverse_link_invNum = invNum
		reverse_full = ''.join([reverse_link, str(reverse_link_invNum), '/'])
		return HttpResponseRedirect(reverse_full)
		#return HttpResponse('Successfully updated rows.')
	else:
		#Get all items in the advice
		item_list = SalesAdvice.objects.raw('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_salesadviceitems ON mainboard_salesadvice.id = mainboard_salesadviceitems.invoiceNumber_id LEFT JOIN mainboard_product ON mainboard_salesadviceitems.item_id = mainboard_product.id WHERE mainboard_salesadvice.invoiceNumber="'+invNum+'"')

	context = {
		'invoiceNumber': invNum,
		'section_header': section_header,
		'editAdv': editAdv,
		'items': item_list,
	}

	return render(request, 'mainboard/data.html', context)

@login_required(login_url='/accounts/login/')
def cancelSalesAdv(request, invoiceNumber):
	invoiceNumber = invoiceNumber

	#Determine which advice is to be deleted.
	thisAdvice = SalesAdvice.objects.get(invoiceNumber=invoiceNumber)
	try:
		thisAdvice.delete()
		delete_success = "Sales Advice is successfully deleted."
		request.session['advice_success_message'] = delete_success
		return HttpResponseRedirect(reverse('salesAdvAll'))
	except:
		return HttpResponse("Record deletion failed.")

@login_required(login_url='/accounts/login/')
def approveSalesAdv(request, invoiceNumber):
	invoiceNumber = invoiceNumber

	#Determine which advice is to be approved.
	thisAdvice = SalesAdvice.objects.get(invoiceNumber=invoiceNumber)
	thisAdviceId = thisAdvice.id
	print(thisAdviceId)
	try:
		thisAdvice.adviceStatus = "APPROVED"
		thisAdvice.save()

		#TABLE CLEANUP
		#Remove related items to advice that have a quantity of 0
		thisItem = SalesAdviceItems.objects.filter(invoiceNumber_id=thisAdviceId, itemQty='0').delete()

		#Generate success message
		approve_success = "Sales Advice is successfully approved."
		request.session['editAdvice_success_message'] = approve_success

		#Generate reverse link and redirect
		reverse_link = '/mainboard/data/salesadvice/'
		reverse_invoiceNumber = invoiceNumber
		reverse_full = ''.join([reverse_link, str(reverse_invoiceNumber), '/'])
		return HttpResponseRedirect(reverse_full)
	except:
		return HttpResponse("Advice approval failed.")

@login_required(login_url='/accounts/login/')
def rcvAdvAll(request):
	section_header = 'Receiving Advices'
	all_advices = ReceivingAdvice.objects.filter().order_by('-receiptDate')
	try:
		success = request.session.get('advice_success_message')
	except KeyError:
		pass

	context = {
		'rcvAdv_view_all': all_advices,
		'section_header': section_header,
		'success': success,
	}

	try:
		del request.session['advice_success_message']
	except KeyError:
		pass
	return render(request, 'mainboard/inventory.html', context)

@login_required(login_url='/accounts/login/')
def rcvAdv(request, receiptNumber):
	rcvAdv = '&nbsp;'
	header_prefix = 'R.A.'
	receiptNumber = receiptNumber
	section_header = ' '.join([header_prefix, receiptNumber])

	#Check if a success message is passed to a session variable
	try:
		success = request.session.get('editAdvice_success_message')
	except KeyError:
		pass

	#GET ALL ADVICE DETAILS
	thisAdvice = ReceivingAdvice.objects.get(receiptNumber=receiptNumber)	#PERFORMS ROW LOCK FOR DETAILS
	#Assign Values
	receiptDate = str(thisAdvice.receiptDate)
	adviceCreator = str(thisAdvice.adviceCreator)
	adviceCreated = str(thisAdvice.adviceCreateDate)
	adviceEditor = str(thisAdvice.adviceEditor)
	adviceEdited = str(thisAdvice.adviceEditDate)
	adviceStatus = str(thisAdvice.adviceStatus)

	#Merge Create/Edit Details
	creator = ', '.join([adviceCreator, adviceCreated])
	editor = ', '.join([adviceEditor, adviceEdited])

	#Get store related to this advice
	store = thisAdvice.store_id
	thisAdviceStore = Store.objects.get(id=store)
	#Assign Values
	storeCode = str(thisAdviceStore.store_code)
	storeName = str(thisAdviceStore.store_name)

	#Determine if advice is approved or not
	if adviceStatus == 'APPROVED':
		approved = "Advice is marked APPROVED."
	else:
		approved = ''

	#Get all items related to the advice
	item_list = SalesAdvice.objects.raw('SELECT * FROM mainboard_receivingadvice LEFT JOIN mainboard_receivingadviceitems ON mainboard_receivingadvice.id = mainboard_receivingadviceitems.receiptNumber_id LEFT JOIN mainboard_product ON mainboard_receivingadviceitems.item_id = mainboard_product.id WHERE mainboard_receivingadvice.receiptNumber="'+receiptNumber+'"')

	#Count items
	for n in SalesAdvice.objects.raw('SELECT *, SUM(itemQty) AS itemCount, SUM(itemCost) AS itemCost FROM mainboard_receivingadvice LEFT JOIN mainboard_receivingadviceitems ON mainboard_receivingadvice.id = mainboard_receivingadviceitems.receiptNumber_id LEFT JOIN mainboard_product ON mainboard_receivingadviceitems.item_id = mainboard_product.id WHERE mainboard_receivingadvice.receiptNumber="'+receiptNumber+'"'):
		item_count = n.itemCount
		item_total = '{:.2f}'.format(n.itemCost)

	context = {
		'rcvAdv': rcvAdv,
		'section_header': section_header,
		'receiptNumber': receiptNumber,
		'receiptDate': receiptDate,
		'adviceCreated': creator,
		'adviceEdited': editor,
		'adviceStatus': adviceStatus,
		'storeName': storeName,
		'storeCode': storeCode,
		'item_list': item_list,
		'itemCount': item_count,
		'itemTotal': item_total,
		'success': success,
		'approved': approved,
	}

	try:
		del request.session['editAdvice_success_message']
	except KeyError:
		pass

	return render(request, 'mainboard/inventory.html', context)

@login_required(login_url='/accounts/login/')
def addRcvAdv(request):
	addRcvAdv = '&nbsp;'
	section_header = "Create Receiving Advice"

	#Check if page is requested using POST or GET
	if request.method == 'POST':
		form = AddReceivingAdviceForm(request.POST)
		if form.is_valid():
			#Save Advice
			newAdvice = form.save()

			#Generate rows in rcvAdviceItems using advice ID and item IDs
			#Perform row lock
			thisAdvice = ReceivingAdvice.objects.filter().order_by('-id')[0]
			thisAdviceId = thisAdvice.id

			#Get item count
			productInstance = Product.objects.all()	#Get all items in Product table
			count = productInstance.count()	#Count all items in Product table

			#Insert rows in rcvAdviceItems with item and advice data
			for x in range(0, count):
				#Get item detail
				thisItem = Product.objects.get(id=x+1)

				#Insert row
				row = ReceivingAdviceItems(receiptNumber_id=thisAdviceId, item_id=thisItem.id, itemQty=0, itemUnitCost=thisItem.item_unit_price, itemCost=0)
				row.save()

			#Generate success message
			advice_success = "Successfully created Receiving Advice."
			request.session['advice_success_message'] = advice_success

			return HttpResponseRedirect(reverse('rcvAdvAll'))
		else:
			error = form.errors
			form = AddReceivingAdviceForm(initial={'adviceCreateDate':datetime.date.today, 'adviceCreator':' '.join([request.user.first_name, request.user.last_name])})

			context = {
				'section_header': section_header,
				'addRcvAdv': addRcvAdv,
				'form': form,
				'error': error,
			}
			return render(request, 'mainboard/inventory.html', context)
	else:
		form = AddReceivingAdviceForm(initial={'adviceCreateDate':datetime.date.today, 'adviceCreator':' '.join([request.user.first_name, request.user.last_name])})

	context = {
		'addRcvAdv': addRcvAdv,
		'section_header': section_header,
		'form': form,
	}

	return render(request, 'mainboard/inventory.html', context)

@login_required(login_url='/accounts/login/')
def editRcvAdv(request, receiptNumber):
	editRcvAdv = '&nbsp;'
	header_prefix = 'Editing Advice'
	receiptNumber = receiptNumber
	section_header = ' '.join([header_prefix, receiptNumber])

	#Check if page is requested using POST or GET
	if request.method == 'POST':
		#Get row count from product model
		productInstance = Product.objects.all()
		count = productInstance.count()

		#Get receipt number id of current advice
		thisAdvice = ReceivingAdvice.objects.get(receiptNumber=receiptNumber)
		thisAdviceId = thisAdvice.id

		#BEGIN PASSING VALUES TO ITEM ROWS
		for y in range(0, count):
			#Get row to update
			thisRow = ReceivingAdviceItems.objects.get(receiptNumber_id=thisAdviceId, item_id=y+1)

			#Assign form field to table field
			field_prefix = 'qty-for-item-'
			row_num = y+1
			field_id = ''.join([field_prefix, str(row_num)])
			item_qty = request.POST.get(field_id)
			thisRow.itemQty = item_qty	#Assign value to item quantity

			#Calculate updated costs
			unit_cost = thisRow.itemUnitCost
			item_cost = unit_cost * float(item_qty)
			format_cost = '{:.2f}'.format(item_cost)	#Format cost to X.YY with ceiling/flooring
			thisRow.itemCost = format_cost				#Assign value to item cost

			#Push changes
			thisRow.save()

		#PASS VALUES FOR ADVICE EDITOR/EDIT DATE
		editor = str(' '.join([request.user.first_name, request.user.last_name]))
		thisAdvice.adviceEditor = editor
		dateToday = timezone.now().date()
		thisAdvice.adviceEditDate = dateToday
		thisAdvice.save()

		#Generate success message
		advice_edit_success = "Successfully edited Sales Advice."
		request.session['editAdvice_success_message'] = advice_edit_success

		#Generate reverse link and redirect
		reverse_link = '/mainboard/inventory/receivingadvice/'
		reverse_receiptNumber = receiptNumber
		reverse_full = ''.join([reverse_link, str(reverse_receiptNumber), '/'])
		return HttpResponseRedirect(reverse_full)
	else:
		item_list = SalesAdvice.objects.raw('SELECT * FROM mainboard_receivingadvice LEFT JOIN mainboard_receivingadviceitems ON mainboard_receivingadvice.id = mainboard_receivingadviceitems.receiptNumber_id LEFT JOIN mainboard_product ON mainboard_receivingadviceitems.item_id = mainboard_product.id WHERE mainboard_receivingadvice.receiptNumber="'+receiptNumber+'"')

	context = {
		'editRcvAdv': editRcvAdv,
		'section_header': section_header,
		'items': item_list,
	}

	return render(request, 'mainboard/inventory.html', context)

@login_required(login_url='/accounts/login/')
def cancelRcvAdv(request, receiptNumber):
	receiptNumber = receiptNumber

	#Determine which advice is to be deleted.
	thisAdvice = ReceivingAdvice.objects.get(receiptNumber=receiptNumber)
	try:
		thisAdvice.delete()
		delete_success = 'Receiving Advice is successfully deleted.'
		request.session['advice_success_message'] = delete_success
		return HttpResponseRedirect(reverse('rcvAdvAll'))
	except:
		return HttpResponse('Record deletion failed.')

@login_required(login_url='accounts/login/')
def approveRcvAdv(request, receiptNumber):
	receiptNumber = receiptNumber

	#Determine which advice is to be approved.
	thisAdvice = ReceivingAdvice.objects.get(receiptNumber=receiptNumber)
	try:
		thisAdvice.adviceStatus = "APPROVED"
		thisAdvice.save()
		approve_success = "Receiving Advice is successfully approved."
		request.session['editAdvice_success_message'] = approve_success

		#Generate reverse link and redirect
		reverse_link = '/mainboard/inventory/receivingadvice/'
		reverse_receiptNumber = receiptNumber
		reverse_full = ''.join([reverse_link, str(reverse_receiptNumber), '/'])
		return HttpResponseRedirect(reverse_full)
	except:
		return HttpResponse('Record update failed.')

@login_required(login_url='/accounts/login/')
def reports(request):
	return render(request, 'mainboard/reports.html')

@login_required(login_url='/accounts/login/')
def admin(request):
	pass

"""
def store(request):
	store_list = Store.objects.all()
	view_header = "Stores currently listed:"
	context = {
		'store_list': store_list,
		'view_header': view_header,
	}
	return render(request, 'mainboard/stores.html', context)
"""

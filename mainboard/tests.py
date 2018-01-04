from django.test import TestCase
from .models import *
from django.db import connection

# Create your tests here.

#cursor = connection.cursor()
#cursor.execute('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_store ON mainboard_salesadvice.store_id = mainboard_store.id')
#for p in SalesAdvice.objects.raw('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_store ON mainboard_salesadvice.store_id = mainboard_store.id'):
#	print(p.invoiceNumber, p.store_name)

#invoiceNumber = 'CON00228147'
#salesAdv_details = SalesAdvice.objects.raw('SELECT * FROM mainboard_salesadvice WHERE mainboard_salesadvice.invoiceNumber=' + str(invoiceNumber) + ' LEFT JOIN mainboard_store ON mainboard_salesadvice.store_id = mainboard_store.id')

#cursor = connection.cursor()
#cursor.execute('SELECT * FROM mainboard_salesadvice LEFT JOIN mainboard_store ON mainboard_salesadvice.store_id = mainboard_store.id WHERE mainboard_salesadvice.invoiceNumber = ')
#myValue = cursor.fetchall()
#print(myValue)

"""
thisAdviceId = SalesAdvice.objects.filter().order_by('-id')[0]
print (thisAdviceId.id)
"""
"""
getCount = Product.objects.all()
print (getCount.count())

for x in range(0, getCount.count()):
    print (x+1)

item = Product.objects.get(id=0+1)
print (item.item_unit_price)

thisCount = 12
adviceId = 6
for x in range(0, thisCount):
    #Get Item Detail
    item = Product.objects.get(id=x+1)	#range 0 + 1 i.e. 0+1(1), 1+1(2) ....
    row = SalesAdviceItems(invoiceNumber_id=adviceId, item_id=item.id, itemQty=0, itemCost=0, itemUnitCost=item.item_unit_price)
    row.save()
    print ('Row entry created.')

print('Successfully exited loop.')
"""

"""
invNum = 'CON00228341'
item_id = 1
thisAdvice = SalesAdvice.objects.get(invoiceNumber=invNum)
thisAdviceId = str(thisAdvice.id)
thisAdviceInvNum = thisAdvice.invoiceNumber
print ('Getting advice details...')
print (', '.join([thisAdviceId, thisAdviceInvNum]))
"""

"""
adviceRow = SalesAdviceItems.objects.get(invoiceNumber=thisAdvice.id, item_id=item_id)
row_id = adviceRow.id
row_invoice = adviceRow.invoiceNumber_id
row_item = adviceRow.item_id
row_qty = adviceRow.itemQty + 99
row_unit = adviceRow.itemUnitCost
row_cost = row_qty * row_unit
print ('')
print ('Getting row details...')
print (', '.join([str(row_id), str(row_invoice), str(row_item), str(row_qty), str(row_cost), str(row_unit)]))
#print (', '.join[(adviceRow.id, adviceRow.invoiceNumber_id, adviceRow.item_id, adviceRow.itemQty, adviceRow.itemCost, adviceRow.itemUnitCost)])
"""

"""
for y in range(0, 12):
    prefix_name = 'qty-for-item-'
    row_num = y+1
    field_id = ''.join([prefix_name, str(row_num)])
    print (field_id)
"""

"""
itemUnitCost = 24
item_qty = 99
unit_cost = itemUnitCost
item_cost = unit_cost * item_qty
print (item_cost)
"""

"""
store_code = 309
thisStore = Store.objects.get(store_code=store_code)
print(thisStore.id)
print(thisStore.store_code)
print(thisStore.store_name)
print(thisStore.store_region)
print(thisStore.store_address)
"""
"""
invNum = 'CON00228341'
item_qty = 2
#Get row count from Product model
getCount = Product.objects.all()
count = getCount.count()
print(count)

#Get invoiceNumber_id of current advice
thisAdvice = SalesAdvice.objects.get(invoiceNumber=invNum)
thisAdviceId = thisAdvice.id
print(thisAdviceId)

for y in range(0, count):
    #Get row to update
    item_row = SalesAdviceItems.objects.get(invoiceNumber_id=thisAdviceId, item_id=y+1)
    print('Editing Row for Item:')
    print(item_row.item_id)

    #Determine on which field is to be assigned to the table field.
    prefix_name = 'qty-for-item-'
    row_num = y+1
    field_id = ''.join([prefix_name, str(row_num)])
    print('Using Field ID:')
    print(field_id)
    #item_qty = request.get.[field_id]
    #item_row.itemQty = item_qty	#Assign value to item quantity.
    print('Quantity:')
    print(item_qty)

    #Calculate updated itemCost based from itemUnitCost * itemQty
    unit_cost = item_row.itemUnitCost
    item_cost = unit_cost * item_qty
    print('Unit Cost:')
    print(unit_cost)
    print('Adjusted Item Cost:')
    print(item_cost)
    #item_row.itemCost = item_cost	#Assign value to item cost.

    #Push all changes
    item_row.save()
    print('Row successfully updated')
    print('------------------------')
    print('')
"""
invoiceNumber = 'CON00228346'

#Determine which advice is to be approved.
thisAdvice = SalesAdvice.objects.get(invoiceNumber=invoiceNumber)
thisAdviceId = thisAdvice.id
print(thisAdviceId)

thisAdvice.adviceStatus = "APPROVED"
thisAdvice.save()
thisItem = SalesAdviceItems.objects.filter(invoiceNumber_id=thisAdviceId, itemQty='0').delete()

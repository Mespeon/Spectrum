from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import salesadvicePDF
from .views import receivingadvicePDF
from .views import storesPDF
from .views import itemsPDF

urlpatterns = [
	#GENERAL URLS
	path(r'', views.index, name='index'),
	#path(r'store/', views.store, name='store'),
	#path(r'accounts/login/', views.login, name='login'),
	#path(r'/accounts/logout', views.logout, name='logout'),
	path(r'logout/', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
	path(r'dashboard/', views.dashboard, name='dashboard'),
	path(r'data/', views.data, name='data'),
	path(r'inventory/', views.inventory, name='inventory'),
	#path(r'reports/', views.reports, name='reports'),
	path(r'admin/', views.admin, name='admin'),
	#SALES DATA
	path(r'data/stores', views.storeAll, name='storeAll'),
	path(r'data/stores/add', views.addStore, name='addStore'),
	path(r'data/stores/<int:store_code>/edit', views.editStore, name='editStore'),
	path(r'data/stores/<int:store_code>/delete', views.deleteStore, name='deleteStore'),
	path(r'data/stores/<int:store_code>/', views.store, name='viewStore'),
	path(r'data/items', views.itemAll, name='itemAll'),
	path(r'data/items/add', views.addItem, name='addItem'),
	path(r'data/items/<int:item_SKU>/edit', views.editItem, name='editItem'),
	path(r'data/items/<int:item_SKU>/', views.item, name='viewItem'),
	path(r'data/salesadvice', views.salesadvAll, name='salesAdvAll'),
	path(r'data/salesadvice/add', views.addAdv, name='addAdvice'),
	path(r'data/salesadvice/<invoiceNumber>/', views.salesAdv, name='viewAdvice'),
	path(r'data/salesadvice/<invoiceNumber>/edit', views.editAdv, name='editAdvice'),
	path(r'data/salesadvice/<invoiceNumber>/approve', views.approveSalesAdv, name='approveSalesAdvice'),
	path(r'data/salesadvice/<invoiceNumber>/cancel', views.cancelSalesAdv, name='cancelSalesAdvice'),
	#INVENTORY MANAGEMENT
	path(r'inventory/receivingadvice', views.rcvAdvAll, name='rcvAdvAll'),
	path(r'inventory/receivingadvice/add', views.addRcvAdv, name='addRcvAdvice'),
	path(r'inventory/receivingadvice/<receiptNumber>/', views.rcvAdv, name='viewRcvAdvice'),
	path(r'inventory/receivingadvice/<receiptNumber>/edit', views.editRcvAdv, name='editRcvAdvice'),
	path(r'inventory/receivingadvice/<receiptNumber>/approve', views.approveRcvAdv, name='approveAdvice'),
	path(r'inventory/receivingadvice/<receiptNumber>/cancel', views.cancelRcvAdv, name='cancelAdvice'),
	#PDF GENERATOR
	path(r'salesadvice/pdf/', views.salesadvicePDF, name='salesAdvPDF'),
	path(r'receivingadvice/pdf/', views.receivingadvicePDF, name='receivingAdvPDF'),
	path(r'stores/pdf/', views.storesPDF, name='storeListPDF'),
	path(r'items/pdf/', views.itemsPDF, name='itemListPDF'),
]

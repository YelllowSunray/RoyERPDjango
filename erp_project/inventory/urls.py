from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Master Data - Items
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<path:item_id>/', views.item_detail, name='item_detail'),
    path('items/<path:item_id>/edit/', views.item_edit, name='item_edit'),
    
    # Master Data - Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/<path:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    
    # Master Data - Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<path:customer_code>/', views.customer_detail, name='customer_detail'),
    
    # Inventory Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/<path:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    
    # QA Reviews
    path('qa-reviews/', views.qa_review_list, name='qa_review_list'),
    path('qa-reviews/create/', views.create_qa_review, name='create_qa_review'),
    path('qa-reviews/<path:qa_review_id>/', views.qa_review_detail, name='qa_review_detail'),
    
    # Batch Management
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/<path:batch_id>/', views.batch_detail, name='batch_detail'),
    
    # API Endpoints for AJAX
    path('api/items/<path:item_id>/details/', views.get_item_details, name='get_item_details'),
    path('api/items/<path:item_id>/supplier-products/', views.get_supplier_products, name='get_supplier_products'),
    path('api/storage-zones/<path:zone_id>/locations/', views.get_storage_locations, name='get_storage_locations'),
    
    # Reports
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/expiry/', views.expiry_report, name='expiry_report'),
    
    # Debug
    path('debug/links/', views.debug_links, name='debug_links'),
    path('api/subtype-choices/', views.get_subtype_choices, name='get_subtype_choices'),
] 
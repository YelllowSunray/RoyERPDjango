from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    Supplier, ItemRecord, Product, ProductVersion, SupplierProduct, Batch,
    StorageZone, StorageLocation, Customer, QAReview, QAReviewUnit, InventoryTransaction,
    calculate_qa_required, calculate_traceability_level, calculate_document_requirements,
    CategoryChoices, GradeChoices, QAStatusChoices, TransactionTypeChoices,
    UOMChoices, ReviewOutcomeChoices, DocumentMatchChoices
)
from .forms import ItemRecordForm

# Authentication Views
def login_view(request):
    """Simple login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventory:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'inventory/login.html')

def logout_view(request):
    """Simple logout view"""
    logout(request)
    return redirect('inventory:dashboard')

# Dashboard Views

def dashboard(request):
    """Main ERP Dashboard"""
    # Get summary statistics
    total_items = ItemRecord.objects.count()
    total_suppliers = Supplier.objects.count()
    total_customers = Customer.objects.count()
    total_batches = Batch.objects.count()
    
    # Recent transactions
    recent_transactions = InventoryTransaction.objects.select_related(
        'item_code', 'batch_id', 'supplier_code'
    ).order_by('-transaction_datetime')[:10]
    
    # Pending QA reviews
    pending_qa = QAReview.objects.filter(review_outcome='Pending').count()
    
    # Expiring batches (within 30 days)
    thirty_days_from_now = timezone.now().date() + timedelta(days=30)
    expiring_batches = Batch.objects.filter(
        expiry_date__lte=thirty_days_from_now,
        qa_status='Approved'
    ).count()
    
    # Low stock items (quantity < 10)
    low_stock_items = ItemRecord.objects.filter(
        batch__qa_status='Approved'
    ).annotate(
        total_quantity=Sum('batch__quantity_received')
    ).filter(total_quantity__lt=10).count()
    
    context = {
        'total_items': total_items,
        'total_suppliers': total_suppliers,
        'total_customers': total_customers,
        'total_batches': total_batches,
        'pending_qa': pending_qa,
        'expiring_batches': expiring_batches,
        'low_stock_items': low_stock_items,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'inventory/dashboard.html', context)

# Master Data Views

def customer_list(request):
    """List all customers with search and filter functionality"""
    customers = Customer.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(customer_code__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(contact_person__icontains=search_query)
        )
    
    # Filter functionality
    customer_type_filter = request.GET.get('customer_type', '')
    if customer_type_filter:
        customers = customers.filter(customer_type=customer_type_filter)
    
    approved_filter = request.GET.get('approved', '')
    if approved_filter:
        customers = customers.filter(approved=approved_filter == 'True')
    
    country_filter = request.GET.get('country', '')
    if country_filter:
        customers = customers.filter(country__icontains=country_filter)
    
    qa_required_filter = request.GET.get('qa_required', '')
    if qa_required_filter:
        customers = customers.filter(qa_required_before_ship=qa_required_filter == 'True')
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'search_query': search_query,
        'customer_type_filter': customer_type_filter,
        'approved_filter': approved_filter,
        'country_filter': country_filter,
        'qa_required_filter': qa_required_filter,
    }
    
    return render(request, 'inventory/customer_list.html', context)


def customer_detail(request, customer_code):
    """Show detailed customer information"""
    customer = get_object_or_404(Customer, customer_code=customer_code)
    
    # Get related transactions
    related_transactions = InventoryTransaction.objects.filter(
        recipient_code=customer
    ).select_related('item_code', 'batch_id').order_by('-transaction_datetime')[:10]
    
    context = {
        'customer': customer,
        'related_transactions': related_transactions,
    }
    
    return render(request, 'inventory/customer_detail.html', context)


def item_list(request):
    """List all items with search and filter functionality"""
    items = ItemRecord.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(item_record_id__icontains=search_query) |
            Q(item_name__icontains=search_query) |
            Q(chemical_family__icontains=search_query)
        )
    
    # Filter functionality
    category_filter = request.GET.get('category', '')
    if category_filter:
        items = items.filter(category=category_filter)
    
    grade_filter = request.GET.get('grade', '')
    if grade_filter:
        items = items.filter(grade=grade_filter)
    
    qa_required_filter = request.GET.get('qa_required', '')
    if qa_required_filter:
        items = items.filter(qa_required=qa_required_filter == 'true')
    
    # Pagination
    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'grade_filter': grade_filter,
        'qa_required_filter': qa_required_filter,
        'categories': CategoryChoices.choices,
        'grades': GradeChoices.choices,
    }
    
    return render(request, 'inventory/item_list.html', context)


def item_create(request):
    """Create a new item"""
    if request.method == 'POST':
        form = ItemRecordForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Item "{item.item_name}" created successfully.')
            return redirect('inventory:item_detail', item_id=item.item_record_id)
    else:
        form = ItemRecordForm()
    
    context = {
        'form': form,
        'title': 'Create New Item'
    }
    return render(request, 'inventory/item_form.html', context)

def item_edit(request, item_id):
    """Edit an existing item"""
    item = get_object_or_404(ItemRecord, item_record_id=item_id)
    if request.method == 'POST':
        form = ItemRecordForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Item "{item.item_name}" updated successfully.')
            return redirect('inventory:item_detail', item_id=item.item_record_id)
    else:
        form = ItemRecordForm(instance=item)
    
    context = {
        'form': form,
        'title': f'Edit Item: {item.item_name}'
    }
    return render(request, 'inventory/item_form.html', context)

def item_detail(request, item_id):
    """Detailed view of an item with related batches and transactions"""
    item = get_object_or_404(ItemRecord, item_record_id=item_id)
    
    # Get related data counts
    batches_count = Batch.objects.filter(item_record_id=item).count()
    suppliers_count = SupplierProduct.objects.filter(item_code=item).count()
    transactions_count = InventoryTransaction.objects.filter(item_code=item).count()
    qa_reviews_count = QAReview.objects.filter(item_code=item).count()
    
    # Get recent batches
    recent_batches = Batch.objects.filter(item_record_id=item).order_by('-received_date')[:5]
    
    # Get recent transactions
    recent_transactions = InventoryTransaction.objects.filter(item_code=item).order_by('-transaction_datetime')[:5]
    
    # Calculate dates for expiry warnings
    from datetime import date, timedelta
    today = date.today()
    today_plus_30 = today + timedelta(days=30)
    
    context = {
        'item': item,
        'batches_count': batches_count,
        'suppliers_count': suppliers_count,
        'transactions_count': transactions_count,
        'qa_reviews_count': qa_reviews_count,
        'recent_batches': recent_batches,
        'recent_transactions': recent_transactions,
        'today': today,
        'today_plus_30': today_plus_30,
    }
    
    return render(request, 'inventory/item_detail.html', context)


def supplier_list(request):
    """List all suppliers with search and filter functionality"""
    suppliers = Supplier.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        suppliers = suppliers.filter(
            Q(supplier_id__icontains=search_query) |
            Q(supplier_name__icontains=search_query) |
            Q(business_unit__icontains=search_query)
        )
    
    # Filter functionality
    approved_filter = request.GET.get('approved', '')
    if approved_filter:
        suppliers = suppliers.filter(approved=approved_filter == 'true')
    
    country_filter = request.GET.get('country', '')
    if country_filter:
        suppliers = suppliers.filter(country_of_origin=country_filter)
    
    # Pagination
    paginator = Paginator(suppliers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'approved_filter': approved_filter,
        'country_filter': country_filter,
    }
    
    return render(request, 'inventory/supplier_list.html', context)


def supplier_detail(request, supplier_id):
    """Detailed view of a supplier with related products and transactions"""
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    
    # Get related data counts
    supplier_products_count = SupplierProduct.objects.filter(supplier_name=supplier).count()
    transactions_count = InventoryTransaction.objects.filter(supplier_code=supplier).count()
    batches_count = Batch.objects.filter(supplier_code=supplier).count()
    qa_reviews_count = QAReview.objects.filter(supplier_code=supplier).count()
    
    # Get supplier products
    supplier_products = SupplierProduct.objects.filter(
        supplier_name=supplier
    ).select_related('item_code')
    
    # Get recent transactions
    transactions = InventoryTransaction.objects.filter(
        supplier_code=supplier
    ).select_related('item_code', 'batch_id').order_by('-transaction_datetime')[:10]
    
    # Calculate dates for review warnings
    from datetime import date, timedelta
    today = date.today()
    today_plus_30 = today + timedelta(days=30)
    
    context = {
        'supplier': supplier,
        'supplier_products_count': supplier_products_count,
        'transactions_count': transactions_count,
        'batches_count': batches_count,
        'qa_reviews_count': qa_reviews_count,
        'supplier_products': supplier_products,
        'transactions': transactions,
        'today': today,
        'today_plus_30': today_plus_30,
    }
    
    return render(request, 'inventory/supplier_detail.html', context)

# Inventory Transaction Views

def transaction_list(request):
    """List all inventory transactions with search and filter functionality"""
    transactions = InventoryTransaction.objects.select_related(
        'item_code', 'batch_id', 'supplier_code', 'recipient_code'
    ).order_by('-transaction_datetime')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        transactions = transactions.filter(
            Q(transaction_id__icontains=search_query) |
            Q(item_code__item_name__icontains=search_query) |
            Q(batch_id__batch_id__icontains=search_query) |
            Q(invoice_no__icontains=search_query)
        )
    
    # Filter functionality
    transaction_type_filter = request.GET.get('transaction_type', '')
    if transaction_type_filter:
        transactions = transactions.filter(transaction_type=transaction_type_filter)
    
    qa_status_filter = request.GET.get('qa_status', '')
    if qa_status_filter:
        transactions = transactions.filter(qa_status=qa_status_filter)
    
    date_from = request.GET.get('date_from', '')
    if date_from:
        transactions = transactions.filter(transaction_datetime__date__gte=date_from)
    
    date_to = request.GET.get('date_to', '')
    if date_to:
        transactions = transactions.filter(transaction_datetime__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(transactions, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'transaction_type_filter': transaction_type_filter,
        'qa_status_filter': qa_status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'transaction_types': TransactionTypeChoices.choices,
        'qa_statuses': QAStatusChoices.choices,
    }
    
    return render(request, 'inventory/transaction_list.html', context)


def transaction_detail(request, transaction_id):
    """Detailed view of an inventory transaction"""
    transaction = get_object_or_404(
        InventoryTransaction.objects.select_related(
            'item_code', 'batch_id', 'supplier_code', 'recipient_code',
            'storage_zone', 'storage_location', 'qa_review_id'
        ),
        transaction_id=transaction_id
    )
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'inventory/transaction_detail.html', context)


def create_transaction(request):
    """Create a new inventory transaction"""
    if request.method == 'POST':
        # Handle form submission
        try:
            # Extract data from POST request
            transaction_type = request.POST.get('transaction_type')
            item_code_id = request.POST.get('item_code')
            quantity = request.POST.get('quantity')
            unit = request.POST.get('unit')
            
            # Create transaction
            transaction = InventoryTransaction.objects.create(
                transaction_id=f"TXN-{datetime.now().strftime('%Y%m%d')}-{InventoryTransaction.objects.count() + 1:03d}",
                transaction_datetime=timezone.now(),
                transaction_user=request.user.username,
                transaction_type=transaction_type,
                item_code_id=item_code_id,
                quantity=quantity,
                unit=unit,
                # Add other fields as needed
            )
            
            messages.success(request, f'Transaction {transaction.transaction_id} created successfully.')
            return redirect('transaction_detail', transaction_id=transaction.transaction_id)
            
        except Exception as e:
            messages.error(request, f'Error creating transaction: {str(e)}')
    
    # Get data for form
    items = ItemRecord.objects.all()
    suppliers = Supplier.objects.filter(approved=True)
    customers = Customer.objects.filter(approved=True)
    storage_zones = StorageZone.objects.all()
    
    context = {
        'items': items,
        'suppliers': suppliers,
        'customers': customers,
        'storage_zones': storage_zones,
        'transaction_types': TransactionTypeChoices.choices,
        'units': UOMChoices.choices,
    }
    
    return render(request, 'inventory/create_transaction.html', context)

# QA Review Views

def qa_review_list(request):
    """List all QA reviews with search and filter functionality"""
    qa_reviews = QAReview.objects.select_related(
        'batch_number', 'item_code', 'supplier_code'
    ).order_by('-review_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        qa_reviews = qa_reviews.filter(
            Q(qa_review_id__icontains=search_query) |
            Q(batch_number__batch_id__icontains=search_query) |
            Q(item_code__item_name__icontains=search_query)
        )
    
    # Filter functionality
    outcome_filter = request.GET.get('outcome', '')
    if outcome_filter:
        qa_reviews = qa_reviews.filter(review_outcome=outcome_filter)
    
    date_from = request.GET.get('date_from', '')
    if date_from:
        qa_reviews = qa_reviews.filter(review_date__gte=date_from)
    
    date_to = request.GET.get('date_to', '')
    if date_to:
        qa_reviews = qa_reviews.filter(review_date__lte=date_to)
    
    # Pagination
    paginator = Paginator(qa_reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'outcome_filter': outcome_filter,
        'date_from': date_from,
        'date_to': date_to,
        'outcomes': ReviewOutcomeChoices.choices,
    }
    
    return render(request, 'inventory/qa_review_list.html', context)


def qa_review_detail(request, qa_review_id):
    """Detailed view of a QA review"""
    qa_review = get_object_or_404(
        QAReview.objects.select_related(
            'batch_number', 'item_code', 'supplier_code'
        ),
        qa_review_id=qa_review_id
    )
    
    # Get unit-level reviews if any
    unit_reviews = QAReviewUnit.objects.filter(qa_review_id=qa_review)
    
    context = {
        'qa_review': qa_review,
        'unit_reviews': unit_reviews,
    }
    
    return render(request, 'inventory/qa_review_detail.html', context)


def create_qa_review(request):
    """Create a new QA review"""
    if request.method == 'POST':
        try:
            # Extract data from POST request
            batch_number_id = request.POST.get('batch_number')
            item_code_id = request.POST.get('item_code')
            supplier_code_id = request.POST.get('supplier_code')
            coa_match = request.POST.get('coa_match') == 'true'
            sds_match = request.POST.get('sds_match') == 'true'
            spec_match = request.POST.get('spec_match') == 'true'
            review_outcome = request.POST.get('review_outcome')
            
            # Create QA review
            qa_review = QAReview.objects.create(
                qa_review_id=f"QA-{datetime.now().strftime('%Y%m%d')}-{QAReview.objects.count() + 1:03d}",
                batch_number_id=batch_number_id,
                item_code_id=item_code_id,
                supplier_code_id=supplier_code_id,
                coa_match=coa_match,
                sds_match=sds_match,
                spec_match=spec_match,
                review_outcome=review_outcome,
                qa_reviewer=request.user.username,
                review_date=timezone.now().date(),
                # Add other fields as needed
            )
            
            messages.success(request, f'QA Review {qa_review.qa_review_id} created successfully.')
            return redirect('qa_review_detail', qa_review_id=qa_review.qa_review_id)
            
        except Exception as e:
            messages.error(request, f'Error creating QA review: {str(e)}')
    
    # Get data for form
    batches = Batch.objects.filter(qa_status='Pending')
    items = ItemRecord.objects.all()
    suppliers = Supplier.objects.filter(approved=True)
    
    context = {
        'batches': batches,
        'items': items,
        'suppliers': suppliers,
        'outcomes': ReviewOutcomeChoices.choices,
        'document_matches': DocumentMatchChoices.choices,
    }
    
    return render(request, 'inventory/create_qa_review.html', context)

# Batch Management Views

def batch_list(request):
    """List all batches with search and filter functionality"""
    batches = Batch.objects.select_related('item_record_id', 'supplier_product_id').order_by('-received_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        batches = batches.filter(
            Q(batch_id__icontains=search_query) |
            Q(item_record_id__item_name__icontains=search_query)
        )
    
    # Filter functionality
    qa_status_filter = request.GET.get('qa_status', '')
    if qa_status_filter:
        batches = batches.filter(qa_status=qa_status_filter)
    
    # Expiring batches filter
    expiring_filter = request.GET.get('expiring', '')
    if expiring_filter:
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        batches = batches.filter(expiry_date__lte=thirty_days_from_now)
    
    # Pagination
    paginator = Paginator(batches, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'qa_status_filter': qa_status_filter,
        'expiring_filter': expiring_filter,
        'qa_statuses': QAStatusChoices.choices,
    }
    
    return render(request, 'inventory/batch_list.html', context)


def batch_detail(request, batch_id):
    """Detailed view of a batch"""
    batch = get_object_or_404(
        Batch.objects.select_related('item_record_id', 'supplier_product_id'),
        batch_id=batch_id
    )
    
    # Get related transactions
    transactions = InventoryTransaction.objects.filter(
        batch_id=batch
    ).select_related('item_code', 'supplier_code').order_by('-transaction_datetime')
    
    # Get QA reviews
    qa_reviews = QAReview.objects.filter(batch_number=batch)
    
    context = {
        'batch': batch,
        'transactions': transactions,
        'qa_reviews': qa_reviews,
    }
    
    return render(request, 'inventory/batch_detail.html', context)

# API Views for AJAX functionality

def get_item_details(request, item_id):
    """Get item details for AJAX requests"""
    try:
        item = ItemRecord.objects.get(item_record_id=item_id)
        data = {
            'item_name': item.item_name,
            'unit_of_measure': item.unit_of_measure,
            'category': item.category,
            'subtype': item.subtype,
            'grade': item.grade,
            'hazard_class': item.hazard_class,
            'qa_required': item.qa_required,
            'traceability_level': item.traceability_level,
            'sds_mandatory': item.sds_mandatory,
            'coa_mandatory': item.coa_mandatory,
            'spec_required': item.spec_required,
        }
        return JsonResponse(data)
    except ItemRecord.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


def get_supplier_products(request, item_id):
    """Get supplier products for an item"""
    try:
        supplier_products = SupplierProduct.objects.filter(
            item_code_id=item_id,
            approved=True
        ).select_related('supplier_name')
        
        data = []
        for sp in supplier_products:
            data.append({
                'id': sp.id,
                'supplier_name': sp.supplier_name.supplier_name,
                'product_code': sp.product_code,
                'grade': sp.grade,
                'is_default': sp.is_default,
            })
        
        return JsonResponse({'supplier_products': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_storage_locations(request, zone_id):
    """Get storage locations for a zone"""
    try:
        locations = StorageLocation.objects.filter(
            zone_id=zone_id,
            active=True
        )
        
        data = []
        for location in locations:
            data.append({
                'id': location.location_id,
                'name': f"{location.location_id} - {location.rack_shelf}",
                'max_capacity': location.max_capacity,
            })
        
        return JsonResponse({'locations': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Report Views

def inventory_report(request):
    """Generate inventory report"""
    from django.db.models import F, Value, CharField, DecimalField
    from django.db.models.functions import Coalesce
    
    # Get all items with their batch information
    items = ItemRecord.objects.annotate(
        batch_count=Count('batch'),
        approved_batches=Count('batch', filter=Q(batch__qa_status='Approved')),
        total_stock=Coalesce(Sum('batch__quantity_received', filter=Q(batch__qa_status='Approved')), Value(0.0, output_field=DecimalField())),
        expiring_batches=Count('batch', filter=Q(batch__expiry_date__lte=F('batch__expiry_date') + timedelta(days=30))),
        expired_batches=Count('batch', filter=Q(batch__expiry_date__lt=timezone.now().date())),
    ).prefetch_related('batch_set', 'batch_set__storage_location', 'batch_set__storage_location__zone_id')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(item_record_id__icontains=search_query) |
            Q(item_name__icontains=search_query) |
            Q(chemical_family__icontains=search_query)
        )
    
    # Filter functionality
    category_filter = request.GET.get('category', '')
    if category_filter:
        items = items.filter(category=category_filter)
    
    qa_status_filter = request.GET.get('qa_status', '')
    if qa_status_filter:
        items = items.filter(batch__qa_status=qa_status_filter)
    
    storage_zone_filter = request.GET.get('storage_zone', '')
    if storage_zone_filter:
        items = items.filter(batch__storage_location__zone_id=storage_zone_filter)
    
    stock_level_filter = request.GET.get('stock_level', '')
    if stock_level_filter:
        if stock_level_filter == 'low':
            items = items.filter(total_stock__lt=Value(10.0, output_field=DecimalField()))
        elif stock_level_filter == 'high':
            items = items.filter(total_stock__gt=Value(100.0, output_field=DecimalField()))
    
    # Get storage zones for filter dropdown
    storage_zones = StorageZone.objects.all()
    
    # Calculate summary statistics
    total_items = items.count()
    active_batches = Batch.objects.filter(qa_status='Approved').count()
    low_stock_items = items.filter(total_stock__lt=Value(10.0, output_field=DecimalField())).count()
    expiring_soon = Batch.objects.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        qa_status='Approved'
    ).count()
    
    # Pagination
    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inventory_items': page_obj,
        'storage_zones': storage_zones,
        'total_items': total_items,
        'active_batches': active_batches,
        'low_stock_items': low_stock_items,
        'expiring_soon': expiring_soon,
    }
    
    return render(request, 'inventory/inventory_report.html', context)


def expiry_report(request):
    """Generate expiry report"""
    from django.db.models import F, ExpressionWrapper, fields
    from django.db.models.functions import ExtractDay
    
    # Get all batches with expiry information
    batches = Batch.objects.select_related(
        'item_record_id', 'storage_location', 'storage_location__zone_id'
    ).annotate(
        days_remaining=ExpressionWrapper(
            F('expiry_date') - timezone.now().date(),
            output_field=fields.IntegerField()
        )
    ).order_by('expiry_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        batches = batches.filter(
            Q(batch_id__icontains=search_query) |
            Q(item_record_id__item_name__icontains=search_query) |
            Q(item_record_id__item_record_id__icontains=search_query)
        )
    
    # Filter functionality
    expiry_status_filter = request.GET.get('expiry_status', '')
    if expiry_status_filter:
        if expiry_status_filter == 'expired':
            batches = batches.filter(expiry_date__lt=timezone.now().date())
        elif expiry_status_filter == 'expiring_week':
            batches = batches.filter(
                expiry_date__lte=timezone.now().date() + timedelta(days=7),
                expiry_date__gte=timezone.now().date()
            )
        elif expiry_status_filter == 'expiring_month':
            batches = batches.filter(
                expiry_date__lte=timezone.now().date() + timedelta(days=30),
                expiry_date__gt=timezone.now().date() + timedelta(days=7)
            )
        elif expiry_status_filter == 'valid':
            batches = batches.filter(expiry_date__gt=timezone.now().date() + timedelta(days=30))
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        batches = batches.filter(item_record_id__category=category_filter)
    
    qa_status_filter = request.GET.get('qa_status', '')
    if qa_status_filter:
        batches = batches.filter(qa_status=qa_status_filter)
    
    storage_zone_filter = request.GET.get('storage_zone', '')
    if storage_zone_filter:
        batches = batches.filter(storage_location__zone_id=storage_zone_filter)
    
    # Get storage zones for filter dropdown
    storage_zones = StorageZone.objects.all()
    
    # Calculate summary statistics
    expired_count = batches.filter(expiry_date__lt=timezone.now().date()).count()
    expiring_week = batches.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=7),
        expiry_date__gte=timezone.now().date()
    ).count()
    expiring_month = batches.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date() + timedelta(days=7)
    ).count()
    valid_count = batches.filter(expiry_date__gt=timezone.now().date() + timedelta(days=30)).count()
    
    # Get batches for alerts
    expired_batches = batches.filter(expiry_date__lt=timezone.now().date())[:10]
    expiring_soon_batches = batches.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=7),
        expiry_date__gte=timezone.now().date()
    )[:10]
    
    # Pagination
    paginator = Paginator(batches, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'expiry_items': page_obj,
        'storage_zones': storage_zones,
        'expired_count': expired_count,
        'expiring_week': expiring_week,
        'expiring_month': expiring_month,
        'valid_count': valid_count,
        'expired_batches': expired_batches,
        'expiring_soon_batches': expiring_soon_batches,
    }
    
    return render(request, 'inventory/expiry_report.html', context)

def debug_links(request):
    """Debug view to test if links are working"""
    return render(request, 'inventory/debug_links.html', {})

def get_subtype_choices(request):
    """AJAX endpoint to get subtype choices based on category"""
    category = request.GET.get('category')
    if category:
        choices = ItemRecord.get_subtype_choices(category)
        return JsonResponse({'choices': choices})
    return JsonResponse({'choices': []})

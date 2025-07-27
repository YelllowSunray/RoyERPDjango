#!/usr/bin/env python
"""
Comprehensive Test Script for Pluviago ERP System
Tests every page and functionality systematically
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from inventory.models import (
    ItemRecord, Supplier, Customer, Batch, InventoryTransaction, QAReview,
    StorageZone, StorageLocation, Product, ProductVersion, SupplierProduct
)

def test_url(client, url_name, expected_status=200, **kwargs):
    """Test a URL and return the result"""
    try:
        if kwargs:
            url = reverse(url_name, kwargs=kwargs)
        else:
            url = reverse(url_name)
        
        response = client.get(url)
        status = response.status_code
        
        if status == expected_status:
            return f"✅ {url_name}: {status}"
        else:
            return f"❌ {url_name}: Expected {expected_status}, got {status}"
            
    except Exception as e:
        return f"💥 {url_name}: ERROR - {str(e)}"

def test_all_pages():
    """Test all pages in the ERP system"""
    print("🔍 COMPREHENSIVE ERP SYSTEM TEST")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Create a test user for authentication
    try:
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')
        print("✅ Authentication setup complete")
    except:
        print("⚠️  Using existing user for authentication")
    
    # Test Results
    results = []
    
    print("\n📋 TESTING ALL PAGES:")
    print("-" * 30)
    
    # 1. Authentication Pages
    print("\n🔐 AUTHENTICATION PAGES:")
    results.append(test_url(client, 'inventory:login'))
    results.append(test_url(client, 'inventory:logout'))
    
    # 2. Dashboard
    print("\n🏠 DASHBOARD:")
    results.append(test_url(client, 'inventory:dashboard'))
    
    # 3. Master Data - Items
    print("\n📦 ITEM MANAGEMENT:")
    results.append(test_url(client, 'inventory:item_list'))
    results.append(test_url(client, 'inventory:item_create'))
    
    # Test item detail with a sample item
    try:
        sample_item = ItemRecord.objects.first()
        if sample_item:
            results.append(test_url(client, 'inventory:item_detail', item_id=sample_item.item_record_id))
            results.append(test_url(client, 'inventory:item_edit', item_id=sample_item.item_record_id))
        else:
            results.append("⚠️  No items found for detail testing")
    except Exception as e:
        results.append(f"💥 Item detail test failed: {str(e)}")
    
    # 4. Master Data - Suppliers
    print("\n🏢 SUPPLIER MANAGEMENT:")
    results.append(test_url(client, 'inventory:supplier_list'))
    
    try:
        sample_supplier = Supplier.objects.first()
        if sample_supplier:
            results.append(test_url(client, 'inventory:supplier_detail', supplier_id=sample_supplier.supplier_id))
        else:
            results.append("⚠️  No suppliers found for detail testing")
    except Exception as e:
        results.append(f"💥 Supplier detail test failed: {str(e)}")
    
    # 5. Master Data - Customers
    print("\n👥 CUSTOMER MANAGEMENT:")
    results.append(test_url(client, 'inventory:customer_list'))
    
    try:
        sample_customer = Customer.objects.first()
        if sample_customer:
            results.append(test_url(client, 'inventory:customer_detail', customer_code=sample_customer.customer_code))
        else:
            results.append("⚠️  No customers found for detail testing")
    except Exception as e:
        results.append(f"💥 Customer detail test failed: {str(e)}")
    
    # 6. Inventory Transactions
    print("\n📊 TRANSACTION MANAGEMENT:")
    results.append(test_url(client, 'inventory:transaction_list'))
    results.append(test_url(client, 'inventory:create_transaction'))
    
    try:
        sample_transaction = InventoryTransaction.objects.first()
        if sample_transaction:
            results.append(test_url(client, 'inventory:transaction_detail', transaction_id=sample_transaction.transaction_id))
        else:
            results.append("⚠️  No transactions found for detail testing")
    except Exception as e:
        results.append(f"💥 Transaction detail test failed: {str(e)}")
    
    # 7. QA Reviews
    print("\n🔍 QA REVIEW MANAGEMENT:")
    results.append(test_url(client, 'inventory:qa_review_list'))
    results.append(test_url(client, 'inventory:create_qa_review'))
    
    try:
        sample_qa = QAReview.objects.first()
        if sample_qa:
            results.append(test_url(client, 'inventory:qa_review_detail', qa_review_id=sample_qa.qa_review_id))
        else:
            results.append("⚠️  No QA reviews found for detail testing")
    except Exception as e:
        results.append(f"💥 QA review detail test failed: {str(e)}")
    
    # 8. Batch Management
    print("\n📦 BATCH MANAGEMENT:")
    results.append(test_url(client, 'inventory:batch_list'))
    
    try:
        sample_batch = Batch.objects.first()
        if sample_batch:
            results.append(test_url(client, 'inventory:batch_detail', batch_id=sample_batch.batch_id))
        else:
            results.append("⚠️  No batches found for detail testing")
    except Exception as e:
        results.append(f"💥 Batch detail test failed: {str(e)}")
    
    # 9. API Endpoints
    print("\n🔌 API ENDPOINTS:")
    results.append(test_url(client, 'inventory:get_subtype_choices'))
    
    try:
        sample_item = ItemRecord.objects.first()
        if sample_item:
            results.append(test_url(client, 'inventory:get_item_details', item_id=sample_item.item_record_id))
            results.append(test_url(client, 'inventory:get_supplier_products', item_id=sample_item.item_record_id))
        else:
            results.append("⚠️  No items found for API testing")
    except Exception as e:
        results.append(f"💥 API endpoint test failed: {str(e)}")
    
    try:
        sample_zone = StorageZone.objects.first()
        if sample_zone:
            results.append(test_url(client, 'inventory:get_storage_locations', zone_id=sample_zone.zone_id))
        else:
            results.append("⚠️  No storage zones found for API testing")
    except Exception as e:
        results.append(f"💥 Storage API test failed: {str(e)}")
    
    # 10. Reports
    print("\n📈 REPORTS:")
    results.append(test_url(client, 'inventory:inventory_report'))
    results.append(test_url(client, 'inventory:expiry_report'))
    
    # 11. Debug
    print("\n🐛 DEBUG:")
    results.append(test_url(client, 'inventory:debug_links'))
    
    # Print Results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    passed = 0
    failed = 0
    errors = 0
    warnings = 0
    
    for result in results:
        print(result)
        if "✅" in result:
            passed += 1
        elif "❌" in result:
            failed += 1
        elif "💥" in result:
            errors += 1
        elif "⚠️" in result:
            warnings += 1
    
    print("\n" + "=" * 50)
    print("📈 FINAL STATISTICS:")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"💥 Errors: {errors}")
    print(f"⚠️  Warnings: {warnings}")
    print(f"📊 Total Tests: {len(results)}")
    
    if failed == 0 and errors == 0:
        print("\n🎉 ALL TESTS PASSED! ERP SYSTEM IS FULLY FUNCTIONAL!")
    else:
        print(f"\n🔧 {failed + errors} ISSUES FOUND - NEEDS ATTENTION")
    
    return passed, failed, errors, warnings

def test_model_creation():
    """Test creating sample data for all models"""
    print("\n🔧 TESTING MODEL CREATION:")
    print("-" * 30)
    
    try:
        # Create sample storage zone
        zone, created = StorageZone.objects.get_or_create(
            zone_id='ZONE-001',
            defaults={
                'zone_name': 'Test Zone',
                'temperature_range': '20-25°C',
                'humidity_controlled': True,
                'hazard_compatibility': 'None',
                'default_for_category': 'Chemical'
            }
        )
        if created:
            print("✅ Created test storage zone")
        
        # Create sample storage location
        location, created = StorageLocation.objects.get_or_create(
            location_id='LOC-001',
            defaults={
                'zone_id': zone,
                'rack_shelf': 'Rack A, Shelf 1',
                'max_capacity': '100 units',
                'active': True
            }
        )
        if created:
            print("✅ Created test storage location")
        
        # Create sample supplier
        supplier, created = Supplier.objects.get_or_create(
            supplier_id='SUP-001',
            defaults={
                'supplier_name': 'Test Supplier Inc.',
                'business_unit': 'Test Unit',
                'address': '123 Test Street, Test City',
                'country_of_origin': 'USA',
                'certifications': 'ISO 9001',
                'approved': True,
                'review_frequency': '1 year'
            }
        )
        if created:
            print("✅ Created test supplier")
        
        # Create sample item
        item, created = ItemRecord.objects.get_or_create(
            item_record_id='CHEM-ACID-001',
            defaults={
                'item_name': 'Test Hydrochloric Acid',
                'unit_of_measure': 'L',
                'category': 'Chemical',
                'subtype': 'Acid',
                'grade': 'ACS',
                'hazard_class': 'Corrosive',
                'chemical_family': 'Hydrochloric Acid (HCl)',
                'contamination_risk': 'Medium',
                'critical_to_product': True
            }
        )
        if created:
            print("✅ Created test item")
        
        # Create sample batch
        from datetime import date, timedelta
        batch, created = Batch.objects.get_or_create(
            batch_id='BATCH-001',
            defaults={
                'item_record_id': item,
                'subtype': 'Acid',
                'supplier_code': supplier,
                'batch_source': 'External',
                'batch_type': 'Production',
                'quantity_received': 10.0,
                'received_date': date.today(),
                'expiry_date': date.today() + timedelta(days=365),
                'qa_status': 'Pending',
                'storage_location': location
            }
        )
        if created:
            print("✅ Created test batch")
        
        print("✅ All test data created successfully")
        return True
        
    except Exception as e:
        print(f"💥 Error creating test data: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Comprehensive ERP System Test...")
    
    # Test model creation first
    test_model_creation()
    
    # Test all pages
    passed, failed, errors, warnings = test_all_pages()
    
    print("\n🎯 TEST COMPLETE!")
    print("=" * 50) 
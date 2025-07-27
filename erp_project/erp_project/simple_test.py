import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

def test_url(client, url_name, expected_status=200, **kwargs):
    try:
        if kwargs:
            url = reverse(url_name, kwargs=kwargs)
        else:
            url = reverse(url_name)
        
        response = client.get(url)
        status = response.status_code
        
        if status == expected_status:
            return f"PASS: {url_name}"
        else:
            return f"FAIL: {url_name} - Expected {expected_status}, got {status}"
            
    except Exception as e:
        return f"ERROR: {url_name} - {str(e)}"

def main():
    print("Testing all ERP pages...")
    
    client = Client()
    
    # Create test user
    try:
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')
    except:
        pass
    
    # Test all URLs
    urls_to_test = [
        ('inventory:login',),
        ('inventory:logout',),
        ('inventory:dashboard',),
        ('inventory:item_list',),
        ('inventory:item_create',),
        ('inventory:supplier_list',),
        ('inventory:customer_list',),
        ('inventory:transaction_list',),
        ('inventory:create_transaction',),
        ('inventory:qa_review_list',),
        ('inventory:create_qa_review',),
        ('inventory:batch_list',),
        ('inventory:inventory_report',),
        ('inventory:expiry_report',),
        ('inventory:debug_links',),
        ('inventory:get_subtype_choices',),
    ]
    
    results = []
    for url_test in urls_to_test:
        result = test_url(client, *url_test)
        results.append(result)
        print(result)
    
    # Summary
    passed = sum(1 for r in results if 'PASS' in r)
    failed = sum(1 for r in results if 'FAIL' in r)
    errors = sum(1 for r in results if 'ERROR' in r)
    
    print(f"\nSummary: {passed} passed, {failed} failed, {errors} errors")
    
    if failed == 0 and errors == 0:
        print("All tests passed!")
    else:
        print("Some issues found.")

if __name__ == "__main__":
    main() 
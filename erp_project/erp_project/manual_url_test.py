#!/usr/bin/env python
"""
Manual URL Test for Problematic URLs
"""

import requests
import time

def test_url(url, expected_status=200):
    """Test a single URL"""
    try:
        print(f"Testing: {url}")
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code != expected_status:
            print(f"❌ Expected {expected_status}, got {response.status_code}")
            if response.status_code == 500:
                print("Error content:")
                print(response.text[:500])
        else:
            print("✅ Success")
        print("-" * 50)
        return response.status_code == expected_status
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        print("-" * 50)
        return False

def main():
    base_url = "http://localhost:8000"
    
    print("🔍 MANUAL URL TEST")
    print("=" * 50)
    
    # Test the problematic URLs
    urls_to_test = [
        (f"{base_url}/inventory/logout/", 302),
        (f"{base_url}/inventory/transactions/create/", 200),
        (f"{base_url}/inventory/qa-reviews/create/", 200),
        (f"{base_url}/inventory/reports/inventory/", 200),
    ]
    
    results = []
    for url, expected_status in urls_to_test:
        success = test_url(url, expected_status)
        results.append(success)
        time.sleep(1)  # Small delay between requests
    
    print("\n📊 RESULTS:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 All URLs working!")
    else:
        print("🔧 Some URLs need attention")

if __name__ == "__main__":
    main() 
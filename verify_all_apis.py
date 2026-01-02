import os
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartclass.settings')
django.setup()

def run_tests():
    client = Client()
    User = get_user_model()
    
    print("\n" + "="*50)
    print("   SMART CLASS COMPANION - COMPREHENSIVE API TEST")
    print("="*50 + "\n")

    def test_url(name, url, method="GET", data=None, expected_status=[200, 302]):
        print(f"Testing {name} ({url}) ...", end=" ", flush=True)
        try:
            if method == "GET":
                response = client.get(url)
            else:
                response = client.post(url, data)
            
            if response.status_code in expected_status:
                print("PASSED")
                return response
            else:
                print(f"FAILED (Status: {response.status_code})")
                return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None

    # 1. Public Pages
    test_url("Home Page", "/")
    test_url("Login Page", "/login/")
    test_url("Register Page", "/register/")

    # 2. Registration and Login Flow
    print("\n--- Testing Registration ---")
    reg_data = {
        'username': 'testuser_api',
        'email': 'api_test@example.com',
        'password': 'password123',
        'password_confirm': 'password123',
        'first_name': 'API',
        'last_name': 'Test',
        'role': 'TEACHER'
    }
    # Check if user already exists
    if User.objects.filter(username='testuser_api').exists():
        User.objects.filter(username='testuser_api').delete()
        print("Cleared existing test user.")

    reg_resp = test_url("Register POST", "/register/", method="POST", data=reg_data)
    
    print("\n--- Testing Login ---")
    login_data = {'username': 'testuser_api', 'password': 'password123'}
    login_resp = test_url("Login POST", "/login/", method="POST", data=login_data)

    if login_resp:
        # 3. Authenticated Pages
        print("\n--- Testing Authenticated Pages ---")
        test_url("Dashboard", "/dashboard/")
        test_url("Create Class Page", "/class/create/")
        test_url("Join Class Page", "/class/join/")

        # 4. Content Creation
        print("\n--- Testing Content Creation ---")
        class_data = {
            'name': 'API Test Class',
            'subject': 'Testing',
            'description': 'Description for API test class',
            'room': '101'
        }
        test_url("Create Class POST", "/class/create/", method="POST", data=class_data)
        
        test_class = None
        try:
            from core.models import Class
            test_class = Class.objects.get(name='API Test Class')
            print(f"Found created class: ID {test_class.id}")
        except Exception:
            print("Could not find created class.")

        if test_class:
            cid = test_class.id
            test_url("Class Detail", f"/class/{cid}/")
            test_url("Edit Class Page", f"/class/{cid}/edit/")
            
            lesson_data = {'title': 'API Lesson', 'description': 'Lesson content'}
            test_url("Create Lesson POST", f"/class/{cid}/lesson/create/", method="POST", data=lesson_data)
            
            assign_data = {
                'title': 'API Assignment', 
                'description': 'Assignment content',
                'due_date': '2030-01-01 12:00:00',
                'max_points': 100
            }
            test_url("Create Assignment POST", f"/class/{cid}/assignment/create/", method="POST", data=assign_data)

    print("\n" + "="*50)
    print("   TESTING COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Ensure apply_schema has been run
    from database.apply_schema import apply_schema
    try:
        apply_schema()
    except Exception as e:
        print(f"Pre-test schema application failed: {e}")
        # Continue anyway as tables might already exist
    
    run_tests()

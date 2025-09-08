#!/usr/bin/env python
"""
Comprehensive test runner for AI-Powered Expense Tracker API
Ensures all endpoints and AI models are thoroughly tested
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.chdir(backend_dir)

def run_tests():
    """Run all test suites"""
    print("Running AI-Powered Expense Tracker API Tests")
    print("=" * 50)
    
    test_commands = [
        # Unit tests by app
        ("Authentication Tests", "python manage.py test users.tests --verbosity=2"),
        ("Expense CRUD Tests", "python manage.py test expenses.tests --verbosity=2"),
        ("AI Functionality Tests", "python manage.py test ai.tests --verbosity=2"),
        
        # Integration tests
        ("Integration Tests", "python -m pytest ../tests/test_endpoints.py -v"),
        
        # Coverage report (if coverage is installed)
        ("Test Coverage", "python manage.py test --verbosity=2 --debug-mode"),
    ]
    
    results = []
    
    for test_name, command in test_commands:
        print(f"\nRunning {test_name}...")
        print("-" * 30)
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"{test_name}: PASSED")
                results.append((test_name, "PASSED"))
            else:
                print(f"{test_name}: FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                results.append((test_name, "FAILED"))
                
        except subprocess.TimeoutExpired:
            print(f"{test_name}: TIMEOUT")
            results.append((test_name, "TIMEOUT"))
        except Exception as e:
            print(f"{test_name}: ERROR - {e}")
            results.append((test_name, "ERROR"))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, status in results if status == "PASSED")
    total = len(results)
    
    for test_name, status in results:
        status_emoji = "PASS" if status == "PASSED" else "FAIL"
        print(f"{status_emoji} {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("All tests passed! Ready for production.")
        return 0
    else:
        print("Some tests failed. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
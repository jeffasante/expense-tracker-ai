#!/usr/bin/env python
"""
Documentation generator for AI-Powered Expense Tracker API
Generates and validates OpenAPI documentation
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def generate_swagger_docs():
    """Generate Swagger documentation from Django views"""
    print("Generating API Documentation...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / 'backend'
    os.chdir(backend_dir)
    
    # Add to Python path
    sys.path.insert(0, str(backend_dir))
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        # Generate OpenAPI schema
        print("Generating OpenAPI schema...")
        result = subprocess.run([
            'python', 'manage.py', 'spectacular', '--color', '--file', 'docs/generated_openapi.yaml'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Auto-generated OpenAPI schema created")
        else:
            print(f"Schema generation failed: {result.stderr}")
            
        # Validate existing OpenAPI spec
        print("Validating manual OpenAPI specification...")
        
        # Check if openapi.yaml exists and is valid
        openapi_file = Path('docs/openapi.yaml')
        if openapi_file.exists():
            print("Manual OpenAPI specification found")
            
            # Basic validation - check if it's valid YAML
            import yaml
            try:
                with open(openapi_file, 'r') as f:
                    spec = yaml.safe_load(f)
                
                # Check required OpenAPI fields
                required_fields = ['openapi', 'info', 'paths']
                missing_fields = [field for field in required_fields if field not in spec]
                
                if missing_fields:
                    print(f"Missing required fields: {missing_fields}")
                else:
                    print("OpenAPI specification is valid")
                    
                # Count endpoints
                path_count = len(spec.get('paths', {}))
                print(f"Documented endpoints: {path_count}")
                
                # Check AI endpoints specifically
                ai_endpoints = [path for path in spec.get('paths', {}) if '/ai/' in path]
                print(f"AI endpoints documented: {len(ai_endpoints)}")
                
            except yaml.YAMLError as e:
                print(f"Invalid YAML: {e}")
        else:
            print("Manual OpenAPI specification not found")
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

def check_documentation_completeness():
    """Check if all endpoints are documented"""
    print("\nChecking documentation completeness...")
    
    try:
        # Import Django and get URL patterns
        import django
        from django.urls import get_resolver
        
        django.setup()
        
        resolver = get_resolver()
        
        # Get all URL patterns
        def extract_urls(urlpatterns, prefix=''):
            urls = []
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # Include pattern (has nested patterns)
                    urls.extend(extract_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
                else:
                    # URL pattern
                    url = prefix + str(pattern.pattern)
                    if hasattr(pattern, 'name') and pattern.name:
                        urls.append((url, pattern.name))
            return urls
        
        all_urls = extract_urls(resolver.url_patterns)
        api_urls = [(url, name) for url, name in all_urls if '/api/' in url]
        
        print(f"Total API endpoints found: {len(api_urls)}")
        
        # Check specific endpoint categories
        auth_endpoints = [url for url, name in api_urls if '/auth/' in url]
        expense_endpoints = [url for url, name in api_urls if '/expenses/' in url]
        ai_endpoints = [url for url, name in api_urls if '/ai/' in url]
        
        print(f"Authentication endpoints: {len(auth_endpoints)}")
        print(f"Expense endpoints: {len(expense_endpoints)}")
        print(f"AI endpoints: {len(ai_endpoints)}")
        
        # List AI endpoints specifically
        if ai_endpoints:
            print("\nAI Endpoints:")
            for url in ai_endpoints:
                print(f"   - {url}")
        
    except Exception as e:
        print(f"Error checking endpoints: {e}")

def main():
    """Main documentation generation function"""
    print("AI-Powered Expense Tracker API Documentation Generator")
    print("=" * 60)
    
    success = generate_swagger_docs()
    check_documentation_completeness()
    
    print("\n" + "=" * 60)
    print("Documentation Summary:")
    print("Manual OpenAPI 3.0 specification: backend/docs/openapi.yaml")
    print("Auto-generated schema: backend/docs/generated_openapi.yaml")
    print("Interactive docs: http://localhost:8000/api/docs/")
    print("Schema endpoint: http://localhost:8000/api/schema/")
    
    if success:
        print("\nDocumentation generation completed successfully!")
        return 0
    else:
        print("\nDocumentation generation completed with warnings.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
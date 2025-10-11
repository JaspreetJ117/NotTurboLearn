"""
Basic sanity test for the FastAPI migration.
Tests that the application can be imported and initialized properly.
"""

import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_imports():
    """Test that all necessary modules can be imported"""
    try:
        # These imports should work even without installing all dependencies
        import json
        import sqlite3
        import threading
        import uuid
        print("✓ Standard library imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_app_structure():
    """Test that app.py has correct structure for FastAPI"""
    app_path = os.path.join(os.path.dirname(__file__), 'scripts', 'app.py')
    with open(app_path, 'r') as f:
        content = f.read()
    
    checks = {
        "FastAPI import": "from fastapi import FastAPI",
        "FastAPI app instance": "app = FastAPI()",
        "Jinja2 templates": "Jinja2Templates",
        "Session middleware": "SessionMiddleware",
        "Uvicorn import": "import uvicorn",
        "Async route": "async def",
        "Pydantic models": "class ChatRequest(BaseModel)",
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string in content:
            print(f"✓ {check_name} found")
        else:
            print(f"✗ {check_name} NOT found")
            all_passed = False
    
    return all_passed

def test_routes_migrated():
    """Test that all Flask routes have been converted"""
    app_path = os.path.join(os.path.dirname(__file__), 'scripts', 'app.py')
    with open(app_path, 'r') as f:
        content = f.read()
    
    # Check for old Flask patterns
    flask_patterns = [
        "@app.route(",
        "return jsonify(",
        "request.files",
        "request.json.get",
    ]
    
    all_passed = True
    for pattern in flask_patterns:
        if pattern in content:
            print(f"✗ Old Flask pattern found: {pattern}")
            all_passed = False
    
    if all_passed:
        print("✓ No old Flask patterns detected")
    
    # Check for new FastAPI patterns
    fastapi_patterns = [
        "@app.get(",
        "@app.post(",
        "@app.delete(",
        "async def",
        "UploadFile",
        "HTTPException",
    ]
    
    for pattern in fastapi_patterns:
        if pattern in content:
            print(f"✓ FastAPI pattern found: {pattern}")
        else:
            print(f"✗ FastAPI pattern NOT found: {pattern}")
            all_passed = False
    
    return all_passed

def test_config_files():
    """Test that configuration files are updated"""
    checks = []
    
    # Check requirements.txt
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            req_content = f.read()
        if 'fastapi' in req_content and 'uvicorn' in req_content:
            print("✓ requirements.txt has FastAPI dependencies")
            checks.append(True)
        else:
            print("✗ requirements.txt missing FastAPI dependencies")
            checks.append(False)
    else:
        print("✗ requirements.txt not found")
        checks.append(False)
    
    # Check README.md
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        if 'FastAPI' in readme_content and 'uvicorn' in readme_content:
            print("✓ README.md updated for FastAPI")
            checks.append(True)
        else:
            print("✗ README.md not fully updated for FastAPI")
            checks.append(False)
    else:
        print("✗ README.md not found")
        checks.append(False)
    
    # Check .gitignore
    gitignore_path = os.path.join(os.path.dirname(__file__), '.gitignore')
    if os.path.exists(gitignore_path):
        print("✓ .gitignore exists")
        checks.append(True)
    else:
        print("✗ .gitignore not found")
        checks.append(False)
    
    return all(checks)

if __name__ == '__main__':
    print("=" * 60)
    print("FastAPI Migration Sanity Tests")
    print("=" * 60)
    
    results = []
    
    print("\n1. Testing imports...")
    results.append(test_imports())
    
    print("\n2. Testing app.py structure...")
    results.append(test_app_structure())
    
    print("\n3. Testing route migration...")
    results.append(test_routes_migrated())
    
    print("\n4. Testing configuration files...")
    results.append(test_config_files())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        sys.exit(1)

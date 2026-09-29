# check_imports.py
import os
import re

def check_typos_in_files():
    """Check all Python files for common import typos"""
    typos_found = False
    
    # Common typos to check for
    common_typos = [
        'modeels', 'modelss', 'advaanced', 'advancced',
        'emotioon', 'ragaa', 'swarra', 'middi'
    ]
    
    # Check all Python files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for typos
                    for typo in common_typos:
                        if typo in content:
                            print(f"❌ TYPO FOUND: {typo} in {filepath}")
                            typos_found = True
                            
                except Exception as e:
                    print(f"⚠️ Could not read {filepath}: {e}")
    
    if not typos_found:
        print("✅ No typos found in Python files!")
    
    return typos_found

def check_imports_in_file(filepath):
    """Check imports in a specific file"""
    print(f"\n🔍 Checking imports in {filepath}:")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if 'import' in line and 'models' in line:
                print(f"  Line {i}: {line.strip()}")
                
    except Exception as e:
        print(f"  ⚠️ Could not read file: {e}")

if __name__ == '__main__':
    print("🔎 Checking for import typos...")
    check_typos_in_files()
    
    # Check specific files
    files_to_check = [
        'routes/emotion_routes.py',
        'routes/swara_routes.py', 
        'routes/midi_routes.py',
        'routes/raga_routes.py',
        'models/model_manager.py',
        'app.py'
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            check_imports_in_file(file)
        else:
            print(f"❌ File not found: {file}")
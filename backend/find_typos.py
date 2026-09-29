import os
import re

def find_typos():
    typos = ['modells', 'eemotion', 'mmodels', 'models\\.\\.']
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for typo in typos:
                        if re.search(typo, content):
                            print(f"❌ TYPO FOUND: '{typo}' in {filepath}")
                            
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")

if __name__ == '__main__':
    find_typos()
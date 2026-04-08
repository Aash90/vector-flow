#!/usr/bin/env python3
"""
Quick test script to verify the portal works correctly.
Run this before launching to ensure dependencies are installed.
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed."""
    required = ['fastapi', 'uvicorn', 'pydantic', 'chromadb', 'sentence_transformers']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing


def install_dependencies():
    """Install missing dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', '../requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def test_imports():
    """Test Python imports."""
    print("\n🧪 Testing imports...")
    try:
        from webapp import app
        from core.pipeline import RAGPipeline
        from debugger.retrieval_debugger import RetrievalDebugger
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("Vector-Flow Portal - Dependency Check")
    print("="*60)
    
    print("\n📋 Checking dependencies...")
    ok, missing = check_dependencies()
    
    if not ok:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        if not install_dependencies():
            print("\n⚠️  Installation failed. Install manually:")
            print("   pip install -r ../requirements.txt")
            return False
        
        print("\n📋 Re-checking dependencies...")
        ok, missing = check_dependencies()
    
    if not test_imports():
        return False
    
    print("\n" + "="*60)
    print("✅ All checks passed!")
    print("="*60)
    print("\n🚀 Ready to launch the portal!")
    print("\nStart the server with:")
    print("   python app.py")
    print("\nThen open: http://localhost:8000")
    print("\n" + "="*60)
    
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

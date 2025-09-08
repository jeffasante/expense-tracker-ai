#!/usr/bin/env python
"""
Optional setup for ML pipeline dependencies
Run this if you want full SmolVLM support
"""

import subprocess
import sys

def install_optional_deps():
    """Install optional dependencies for enhanced AI features"""
    optional_packages = [
        "accelerate>=0.26.0",
        "torch>=2.0.0", 
        "transformers>=4.35.0"
    ]
    
    print("Installing optional ML dependencies...")
    
    for package in optional_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")
            print("Continuing with basic functionality...")
    
    print("Setup complete. Enhanced AI features may be available.")

if __name__ == "__main__":
    install_optional_deps()
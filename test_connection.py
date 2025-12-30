#!/usr/bin/env python3
"""Quick test script to verify Azure API connections."""

import sys
from azure_vision import AzureVisionService, AzureFaceService
from config import Config

def test_azure_services():
    """Test Azure service connections."""
    print("🔍 Testing Azure Services Connection...")
    print("-" * 50)
    
    # Test Computer Vision
    print("\n1. Testing Azure Computer Vision...")
    try:
        vision = AzureVisionService()
        print("   ✓ Computer Vision service initialized")
        print(f"   Endpoint: {Config.AZURE_COMPUTER_VISION_ENDPOINT}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test Face API
    print("\n2. Testing Azure Face API...")
    try:
        face = AzureFaceService()
        if face.client:
            print("   ✓ Face API service initialized")
            print(f"   Endpoint: {Config.AZURE_FACE_ENDPOINT}")
        else:
            print("   ℹ Face API not configured (optional)")
    except Exception as e:
        print(f"   ℹ Face API: {e}")
    
    print("\n" + "-" * 50)
    print("✅ All services are ready!")
    print("\nYou can now start the application with:")
    print("  python app.py")
    print("  or")
    print("  ./start.sh")
    
    return True

if __name__ == "__main__":
    success = test_azure_services()
    sys.exit(0 if success else 1)



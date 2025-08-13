#!/usr/bin/env python3
"""
Test script for the AI-powered Menu Intelligence Widget Backend
"""

import requests
import json
import time

def test_backend():
    """Test the backend API endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing AI-Powered Menu Intelligence Widget Backend")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5000")
        return False
    
    # Test 2: Generate Menu Content (GPT-3.5)
    print("\n2. Testing Menu Content Generation (GPT-3.5)...")
    test_items = ["Margherita Pizza", "Chicken Burger", "Paneer Tikka"]
    
    for item in test_items:
        try:
            response = requests.post(
                f"{base_url}/generate-item-details",
                json={
                    "item_name": item,
                    "model": "gpt-3.5-turbo"
                },
                timeout=10
            )
            
            # Add delay between requests to avoid rate limiting
            time.sleep(1.5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Generated content for '{item}':")
                print(f"   Description: {data['description']}")
                print(f"   Upsell: {data['upsell_suggestion']}")
                print(f"   Model: {data['model_used']}")
            else:
                print(f"❌ Failed to generate content for '{item}': {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout generating content for '{item}'")
        except Exception as e:
            print(f"❌ Error generating content for '{item}': {str(e)}")
    
    # Test 3: Generate Menu Content (GPT-4)
    print("\n3. Testing Menu Content Generation (GPT-4)...")
    try:
        response = requests.post(
            f"{base_url}/generate-item-details",
            json={
                "item_name": "Paneer Tikka Pizza",
                "model": "gpt-4"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated GPT-4 content for 'Paneer Tikka Pizza':")
            print(f"   Description: {data['description']}")
            print(f"   Upsell: {data['upsell_suggestion']}")
            print(f"   Model: {data['model_used']}")
        else:
            print(f"❌ Failed to generate GPT-4 content: {response.status_code}")
            
        # Add delay before next test
        time.sleep(1.5)
            
    except Exception as e:
        print(f"❌ Error testing GPT-4: {str(e)}")
    
    # Test 4: Input Validation
    print("\n4. Testing Input Validation...")
    
    # Test empty input
    try:
        response = requests.post(
            f"{base_url}/generate-item-details",
            json={"item_name": ""}
        )
        if response.status_code == 400:
            print("✅ Empty input validation working")
        else:
            print(f"❌ Empty input validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing empty input: {str(e)}")
    
    # Add delay before next test
    time.sleep(1.5)
    
    # Test invalid input
    try:
        response = requests.post(
            f"{base_url}/generate-item-details",
            json={"item_name": "1234567890" * 20}  # Very long input
        )
        if response.status_code == 400:
            print("✅ Long input validation working")
        else:
            print(f"❌ Long input validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing long input: {str(e)}")
    
    # Test 5: Rate Limiting (simulated)
    print("\n5. Testing Rate Limiting...")
    try:
        # Make multiple rapid requests to trigger rate limiting
        for i in range(5):
            response = requests.post(
                f"{base_url}/generate-item-details",
                json={"item_name": f"Test Item {i}"}
            )
            if response.status_code == 429:
                print("✅ Rate limiting working")
                break
            time.sleep(0.2)  # Very small delay between rapid requests
        else:
            print("⚠️  Rate limiting not triggered (this is normal for small number of requests)")
            
    except Exception as e:
        print(f"❌ Error testing rate limiting: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Backend testing completed!")
    print("\nTo test the full application:")
    print("1. Start the backend: cd backend && python app.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Or use the startup script: ./start.sh")
    
    return True

if __name__ == "__main__":
    test_backend()

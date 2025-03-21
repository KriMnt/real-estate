import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_create_property():
    """Test creating a property"""
    
    url = f"{BASE_URL}/properties/"
    
    # Test data for creating a property
    data = {
        "external_id": "test123",
        "source": "test-source",
        "title": "Test Property",
        "description": "A beautiful apartment for testing",
        "price": 250000,
        "currency": "EUR",
        "location": "Test City, Downtown",
        "area": 120,
        "rooms": 3,
        "features": {"parking": True, "balcony": True}
    }
    
    # Make POST request
    response = requests.post(url, json=data)
    
    # Print full response for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        # Get the created property's ID
        property_id = response.json()["id"]
        print(f"Successfully created property with ID: {property_id}")
        return property_id
    else:
        print(f"Failed to create property: {response.text}")
        return None

def main():
    # Make sure server is running before executing this
    
    # Test creating a property
    property_id = test_create_property()
    
    if property_id:
        print("Tests passed!")
    else:
        print("Tests failed!")

if __name__ == "__main__":
    main()
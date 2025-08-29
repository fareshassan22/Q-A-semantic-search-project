#!/usr/bin/env python3
"""
Demo script for the Q&A Semantic Search system.
"""

import requests
import json
import time


def test_health(base_url="http://127.0.0.1:8000"):
    """Test the health endpoint."""
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_index(base_url="http://127.0.0.1:8000"):
    """Test indexing some sample Q&A pairs."""
    sample_data = {
        "pairs": [
            {
                "question": "What is your refund policy?",
                "answer": "We offer a 30-day money-back guarantee on all purchases."
            },
            {
                "question": "How do I contact customer support?",
                "answer": "You can reach us at support@example.com or call 1-800-123-4567."
            },
            {
                "question": "What payment methods do you accept?",
                "answer": "We accept credit cards, PayPal, and Apple Pay."
            },
            {
                "question": "How long does shipping take?",
                "answer": "Standard shipping takes 3-5 business days, express shipping takes 1-2 business days."
            },
            {
                "question": "Do you ship internationally?",
                "answer": "Yes, we ship to most countries worldwide. International shipping takes 7-14 business days."
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/index",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Indexed {result['indexed_count']} Q&A pairs successfully")
            print(f"Message: {result['message']}")
            return True
        else:
            print(f"❌ Indexing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Indexing error: {e}")
        return False


def test_query(base_url="http://127.0.0.1:8000"):
    """Test querying the system."""
    test_queries = [
        "How can I get my money back?",
        "What's your phone number?",
        "Do you take credit cards?",
        "How fast is delivery?",
        "Can you ship to Europe?"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/query",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Query: '{query}'")
                print(f"   Result: {result.get('result', 'N/A')}")
            else:
                print(f"❌ Query failed: '{query}' - {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"Query error for '{query}': {e}")
        
        print("-" * 50)


def test_stats(base_url="http://127.0.0.1:8000"):
    """Test the stats endpoint."""
    try:
        response = requests.get(f"{base_url}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 System Stats: {stats}")
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"Stats error: {e}")


def main():
    """Run the demo."""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Q&A Semantic Search System Demo")
    print("=" * 50)
    
    # Test health
    if not test_health(base_url):
        print("❌ System is not healthy. Make sure the API is running.")
        return
    
    print("\n" + "=" * 50)
    
    # Test indexing
    print("📝 Testing indexing...")
    if test_index(base_url):
        print("✅ Indexing completed successfully")
    else:
        print("❌ Indexing failed")
        return
    
    print("\n" + "=" * 50)
    
    # Test stats
    print("📊 Testing stats...")
    test_stats(base_url)
    
    print("\n" + "=" * 50)
    
    # Test querying
    print("🔍 Testing queries...")
    test_query(base_url)
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")


if __name__ == "__main__":
    main()

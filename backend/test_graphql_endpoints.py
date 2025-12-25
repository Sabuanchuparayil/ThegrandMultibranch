#!/usr/bin/env python3
"""
Test GraphQL endpoints to verify which queries work and which don't.
"""
import requests
import json

BACKEND_URL = "https://backend-production-fb5f.up.railway.app/graphql/"

queries = {
    "branches": {
        "query": "{ branches { id name code } }"
    },
    "branchInventory": {
        "query": "{ branchInventory(branchId: \"1\") { id quantity } }"
    },
    "products": {
        "query": "{ products(first: 5) { edges { node { id name } } } }"
    },
    "orders": {
        "query": "{ orders(first: 5) { edges { node { id number } } } }"
    },
    "users": {
        "query": "{ users(first: 5) { edges { node { id email } } } }"
    },
}

def test_query(name, query_data):
    """Test a GraphQL query"""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"{'='*80}")
    
    try:
        response = requests.post(
            BACKEND_URL,
            json=query_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        result = response.json()
        
        if "errors" in result:
            print(f"❌ ERROR:")
            for error in result["errors"]:
                print(f"   {error.get('message', 'Unknown error')}")
            if "data" in result:
                print(f"   Data: {result.get('data')}")
        else:
            print(f"✅ SUCCESS")
            data = result.get("data", {})
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                    elif isinstance(value, dict) and "edges" in value:
                        print(f"   {key}: {len(value['edges'])} items")
                    else:
                        print(f"   {key}: {value}")
            else:
                print(f"   Data: {data}")
        
        return "errors" not in result
        
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def main():
    print("=" * 80)
    print("GRAPHQL ENDPOINT TEST")
    print("=" * 80)
    print(f"\nBackend URL: {BACKEND_URL}")
    
    results = {}
    for name, query_data in queries.items():
        results[name] = test_query(name, query_data)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    working = [name for name, success in results.items() if success]
    failing = [name for name, success in results.items() if not success]
    
    if working:
        print(f"\n✅ Working queries ({len(working)}):")
        for name in working:
            print(f"   - {name}")
    
    if failing:
        print(f"\n❌ Failing queries ({len(failing)}):")
        for name in failing:
            print(f"   - {name}")
    
    print("\n" + "=" * 80)
    return 0 if len(working) > 0 else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())


#!/usr/bin/env python3
"""
Simple API test for Singapore Rainfall Data
Run this first to verify API connectivity
"""

import requests
import json
from datetime import datetime

def test_singapore_api():
    """Test basic API connectivity"""
    print("🌧️ Testing Singapore Rainfall API...")
    print("=" * 50)
    
    url = "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
    
    try:
        print("📡 Connecting to API...")
        response = requests.get(url, timeout=30)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Basic info
            print(f"✅ Response Code: {data.get('code', 'N/A')}")
            print(f"📍 Number of Stations: {len(data['data']['stations'])}")
            print(f"📊 Number of Readings: {len(data['data']['readings'])}")
            
            # Sample station
            if data['data']['stations']:
                sample_station = data['data']['stations'][0]
                print(f"📍 Sample Station: {sample_station['name']} (ID: {sample_station['id']})")
            
            # Sample reading
            if data['data']['readings']:
                sample_reading = data['data']['readings'][0]
                print(f"⏰ Latest Reading Time: {sample_reading['timestamp']}")
                print(f"📈 Data Points in Latest Reading: {len(sample_reading['data'])}")
            
            print("\n✅ API Test SUCCESSFUL!")
            return True
            
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except KeyError as e:
        print(f"❌ Data Structure Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_singapore_api()
    
    if success:
        print("\n🎯 Ready to proceed with dashboard development!")
    else:
        print("\n❌ Please fix API connectivity before proceeding.")
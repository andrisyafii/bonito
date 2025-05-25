import requests
import pandas as pd
from datetime import datetime
import time
import json

class RainfallDataProcessor:
    """Handle Singapore rainfall data extraction and processing"""
    
    def __init__(self):
        self.base_url = "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
        self.stations_info = {}
        
    def fetch_data(self, date=None):
        """Fetch rainfall data from Singapore API"""
        params = {}
        if date:
            params['date'] = date
            
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def debug_api_structure(self, api_response):
        """Debug helper to understand API structure"""
        if api_response:
            print("🔍 API Response Structure:")
            print(json.dumps(api_response, indent=2)[:1000] + "..." if len(str(api_response)) > 1000 else json.dumps(api_response, indent=2))
    
    def process_stations(self, api_response):
        """Extract and store station information with flexible structure handling"""
        if not api_response or 'data' not in api_response:
            print("❌ No data found in API response")
            return pd.DataFrame()
            
        stations = api_response['data'].get('stations', [])
        print(f"📍 Found {len(stations)} stations")
        
        if not stations:
            print("⚠️ No stations data available")
            return pd.DataFrame()
        
        # Debug: Check structure of first station
        if stations:
            print(f"🔍 First station structure: {stations[0]}")
        
        # Store for reference with flexible field handling
        for station in stations:
            station_id = station.get('id', station.get('stationId', 'unknown'))
            
            # Try different possible location field names
            location_info = {}
            if 'labelLocation' in station:
                location_info = station['labelLocation']
            elif 'location' in station:
                location_info = station['location']
            elif 'coordinates' in station:
                location_info = station['coordinates']
            
            self.stations_info[station_id] = {
                'name': station.get('name', f'Station_{station_id}'),
                'latitude': location_info.get('latitude', location_info.get('lat', 0)),
                'longitude': location_info.get('longitude', location_info.get('lng', location_info.get('lon', 0)))
            }
        
        return pd.DataFrame(stations)
    
    def process_readings(self, api_response):
        """Process readings into structured DataFrame"""
        if not api_response or 'data' not in api_response:
            print("❌ No data found in API response")
            return pd.DataFrame()
            
        readings = api_response['data'].get('readings', [])
        print(f"📊 Found {len(readings)} reading timestamps")
        
        if not readings:
            print("⚠️ No readings data available")
            return pd.DataFrame()
        
        processed_data = []
        
        for reading in readings:
            timestamp = reading.get('timestamp', reading.get('time', ''))
            data_points = reading.get('data', [])
            
            print(f"📅 Processing timestamp: {timestamp} with {len(data_points)} data points")
            
            for data_point in data_points:
                station_id = data_point.get('stationId', data_point.get('station_id', data_point.get('id', 'unknown')))
                rainfall_value = data_point.get('value', data_point.get('rainfall', 0))
                
                # Get station info
                station_info = self.stations_info.get(station_id, {})
                
                processed_data.append({
                    'timestamp': pd.to_datetime(timestamp),
                    'station_id': station_id,
                    'station_name': station_info.get('name', f'Station_{station_id}'),
                    'latitude': station_info.get('latitude', 0),
                    'longitude': station_info.get('longitude', 0),
                    'rainfall_mm': rainfall_value
                })
        
        df = pd.DataFrame(processed_data)
        if not df.empty:
            df['hour'] = df['timestamp'].dt.hour
            df['date'] = df['timestamp'].dt.date
            print(f"✅ Created DataFrame with {len(df)} rows")
        else:
            print("❌ No data could be processed into DataFrame")
        
        return df
    
    def get_all_data(self, date=None, debug=False):
        """Get comprehensive rainfall data"""
        print("📡 Fetching rainfall data...")
        
        # Fetch API response
        api_response = self.fetch_data(date)
        if not api_response:
            print("❌ Failed to fetch data from API")
            return pd.DataFrame()
        
        # Debug API structure if requested
        if debug:
            self.debug_api_structure(api_response)
        
        # Process stations
        stations_df = self.process_stations(api_response)
        if stations_df.empty:
            print("❌ No stations could be processed")
            return pd.DataFrame()
        
        # Process readings
        df = self.process_readings(api_response)
        
        if not df.empty:
            print(f"✅ Successfully processed {len(df)} rainfall readings from {len(self.stations_info)} stations")
        else:
            print("❌ No readings could be processed")
        
        return df

# Enhanced test with better error handling
if __name__ == "__main__":
    processor = RainfallDataProcessor()
    
    # Try to get data with debug mode first
    print("🚀 Starting data processing with debug mode...")
    data = processor.get_all_data(debug=True)
    
    if not data.empty:
        print(f"\n📊 Data Summary:")
        print(f"Total readings: {len(data)}")
        print(f"Unique stations: {data['station_id'].nunique()}")
        print(f"Time range: {data['timestamp'].min()} to {data['timestamp'].max()}")
        print(f"Rainfall statistics:")
        print(f"  - Average: {data['rainfall_mm'].mean():.2f} mm")
        print(f"  - Max: {data['rainfall_mm'].max():.2f} mm")
        print(f"  - Min: {data['rainfall_mm'].min():.2f} mm")
        
        # Show sample data
        print(f"\n📋 Sample data (first 5 rows):")
        print(data.head().to_string())
        
        # Save sample
        try:
            data.to_csv('sample_rainfall_data.csv', index=False)
            print("\n✅ Data saved to sample_rainfall_data.csv")
        except Exception as e:
            print(f"\n❌ Error saving data: {e}")
    else:
        print("\n❌ No data retrieved. Please check:")
        print("1. Internet connection")
        print("2. API endpoint availability")
        print("3. API response structure (check debug output above)")
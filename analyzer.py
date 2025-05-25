import pandas as pd
import numpy as np
from datetime import datetime

class RainfallAnalyzer:
    """Analyze rainfall data for dashboard requirements"""
    
    def __init__(self, data):
        self.data = data.copy() if not data.empty else pd.DataFrame()
        
    def get_top_rainfall_areas(self, n=10, group_nearby=False):
        """Requirement 1a: Top 10 areas of highest rainfall"""
        if self.data.empty:
            return pd.DataFrame()
        
        if group_nearby:
            # Simple grouping by rounding coordinates
            self.data['lat_group'] = self.data['latitude'].round(2)
            self.data['lon_group'] = self.data['longitude'].round(2)
            grouped = self.data.groupby(['lat_group', 'lon_group']).agg({
                'rainfall_mm': ['sum', 'mean', 'count'],
                'station_name': 'first',
                'latitude': 'mean',
                'longitude': 'mean'
            }).reset_index()
            grouped.columns = ['lat_group', 'lon_group', 'total_rainfall', 'avg_rainfall', 
                             'reading_count', 'station_name', 'latitude', 'longitude']
        else:
            grouped = self.data.groupby(['station_id', 'station_name']).agg({
                'rainfall_mm': ['sum', 'mean', 'count'],
                'latitude': 'mean',
                'longitude': 'mean'
            }).reset_index()
            grouped.columns = ['station_id', 'station_name', 'total_rainfall', 
                             'avg_rainfall', 'reading_count', 'latitude', 'longitude']
        
        return grouped.nlargest(n, 'total_rainfall')
    
    def get_lowest_rainfall_areas(self, n=10):
        """Requirement 1b: Top 10 areas of lowest rainfall population"""
        if self.data.empty:
            return pd.DataFrame()
            
        grouped = self.data.groupby(['station_id', 'station_name']).agg({
            'rainfall_mm': ['sum', 'mean', 'count'],
            'latitude': 'mean',
            'longitude': 'mean'
        }).reset_index()
        grouped.columns = ['station_id', 'station_name', 'total_rainfall', 
                         'avg_rainfall', 'reading_count', 'latitude', 'longitude']
        
        return grouped.nsmallest(n, 'total_rainfall')
    
    def get_hourly_distribution(self):
        """Requirement 1c: Hourly rainfall distribution across Singapore"""
        if self.data.empty:
            return pd.DataFrame()
            
        hourly = self.data.groupby('hour').agg({
            'rainfall_mm': ['sum', 'mean', 'count', 'std']
        }).reset_index()
        hourly.columns = ['hour', 'total_rainfall', 'avg_rainfall', 'reading_count', 'std_rainfall']
        
        return hourly.sort_values('hour')
    
    def get_monthly_average(self):
        """Calculate current monthly average for alert threshold"""
        if self.data.empty:
            return 0
            
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_data = self.data[
            (self.data['timestamp'].dt.month == current_month) & 
            (self.data['timestamp'].dt.year == current_year)
        ]
        
        if monthly_data.empty:
            return self.data['rainfall_mm'].mean()
        
        return monthly_data['rainfall_mm'].mean()
    
    def get_alert_areas(self, threshold_multiplier=1.5):
        """Requirement 2: Alert mechanism for areas exceeding average rainfall"""
        if self.data.empty:
            return pd.DataFrame(), 0
            
        monthly_avg = self.get_monthly_average()
        threshold = monthly_avg * threshold_multiplier
        
        # Group by station and calculate current averages
        station_averages = self.data.groupby(['station_id', 'station_name']).agg({
            'rainfall_mm': 'mean',
            'latitude': 'mean',
            'longitude': 'mean'
        }).reset_index()
        
        # Find stations exceeding threshold
        alert_areas = station_averages[station_averages['rainfall_mm'] > threshold].copy()
        
        if not alert_areas.empty:
            alert_areas['threshold'] = threshold
            alert_areas['excess_rainfall'] = alert_areas['rainfall_mm'] - threshold
            alert_areas = alert_areas.sort_values('excess_rainfall', ascending=False)
        
        return alert_areas, threshold
    
    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        if self.data.empty:
            return {}
            
        return {
            'total_stations': self.data['station_id'].nunique(),
            'total_readings': len(self.data),
            'avg_rainfall': self.data['rainfall_mm'].mean(),
            'max_rainfall': self.data['rainfall_mm'].max(),
            'min_rainfall': self.data['rainfall_mm'].min(),
            'std_rainfall': self.data['rainfall_mm'].std(),
            'zero_rainfall_readings': len(self.data[self.data['rainfall_mm'] == 0]),
            'time_range_start': self.data['timestamp'].min(),
            'time_range_end': self.data['timestamp'].max()
        }

# Test the analyzer
if __name__ == "__main__":
    # Test with sample data
    try:
        data = pd.read_csv('sample_rainfall_data.csv')
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['hour'] = data['timestamp'].dt.hour
        
        analyzer = RainfallAnalyzer(data)
        
        print("🔍 Testing Analyzer Functions:")
        print("=" * 40)
        
        # Test 1: Top rainfall areas
        top_areas = analyzer.get_top_rainfall_areas(5)
        print(f"\n✅ Top 5 Rainfall Areas:")
        for i, row in top_areas.iterrows():
            print(f"{len(top_areas) - i}. {row['station_name']}: {row['total_rainfall']:.2f} mm")
        
        # Test 2: Hourly distribution
        hourly = analyzer.get_hourly_distribution()
        print(f"\n✅ Hourly Distribution (sample):")
        for i, row in hourly.head(3).iterrows():
            print(f"Hour {row['hour']:02d}:00 - {row['total_rainfall']:.2f} mm total")
        
        # Test 3: Alert system
        alerts, threshold = analyzer.get_alert_areas()
        print(f"\n✅ Alert System:")
        print(f"Threshold: {threshold:.2f} mm")
        print(f"Stations exceeding threshold: {len(alerts)}")
        
        # Test 4: Summary stats
        stats = analyzer.generate_summary_stats()
        print(f"\n✅ Summary Statistics:")
        print(f"Total stations: {stats['total_stations']}")
        print(f"Average rainfall: {stats['avg_rainfall']:.2f} mm")
        
        print("\n🎯 All analyzer functions working correctly!")
        
    except FileNotFoundError:
        print("❌ Please run data_processor.py first to generate sample data")
    except Exception as e:
        print(f"❌ Error testing analyzer: {e}")
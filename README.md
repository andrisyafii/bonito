# 🌧️ Singapore Rainfall Dashboard

A real-time rainfall monitoring dashboard for Singapore using data from the Singapore Government API.

## 📋 Technical Assessment Requirements

This project fulfills all technical assessment requirements:

✅ **Dashboard Implementation**
- Top 10 areas of highest rainfall (with optional grouping)
- Top 10 areas of lowest rainfall population  
- Hourly rainfall distribution across Singapore
- Alert mechanism for areas exceeding average rainfall

✅ **Technical Implementation**
- Python-based solution
- Real-time API integration
- Interactive web dashboard
- Data processing and analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection for API access

### Installation & Setup
```bash
# 1. Navigate to project directory
cd singapore-rainfall-dashboard

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test API connection
python test_api.py

# 6. Run the dashboard
streamlit run app.py
```

### Alternative: Quick Test
```bash
# Test individual components
python data_processor.py    # Test data processing
python analyzer.py          # Test analysis functions
```

## 🏗️ Project Structure

```
singapore-rainfall-dashboard/
├── app.py                  # Main Streamlit dashboard
├── data_processor.py       # API data extraction & processing
├── analyzer.py            # Data analysis functions
├── test_api.py            # API connectivity test
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── data/                  # Generated data files
└── docs/                  # Documentation
```

## 📊 Dashboard Features

### 1. Real-time Data Loading
- Fetches current rainfall data from Singapore API
- 5-minute interval updates from NEA (National Environment Agency)
- Caching mechanism for performance

### 2. Top Rainfall Areas Analysis
- **Highest Rainfall**: Interactive bar charts and maps
- **Lowest Rainfall**: Complementary analysis
- **Grouping Option**: Combine nearby stations for regional analysis

### 3. Temporal Analysis
- **Hourly Distribution**: Rainfall patterns throughout the day
- **Peak Hours**: Identification of high/low rainfall periods
- **Time Series**: Interactive line charts

### 4. Alert System
- **Automatic Thresholds**: 1.5x monthly average rainfall
- **Real-time Monitoring**: Immediate alerts for exceeding areas
- **Visual Indicators**: Color-coded warning system

### 5. Interactive Visualizations
- **Maps**: Geographic distribution using Plotly
- **Charts**: Bar charts, line graphs, time series
- **Hover Details**: Station-specific information
- **Zoom & Pan**: Interactive map controls

## 🛠️ Technical Architecture

### Data Flow
```
Singapore Gov API → Data Processor → Analyzer → Dashboard Components
```

### Key Components

#### RainfallDataProcessor (`data_processor.py`)
```python
# Handles API communication and data processing
processor = RainfallDataProcessor()
data = processor.get_all_data()  # Returns processed DataFrame
```

#### RainfallAnalyzer (`analyzer.py`)
```python
# Performs analysis for dashboard requirements
analyzer = RainfallAnalyzer(data)
top_areas = analyzer.get_top_rainfall_areas(10)
hourly_dist = analyzer.get_hourly_distribution()
alerts = analyzer.get_alert_areas()
```

### API Integration
- **Endpoint**: `https://api-open.data.gov.sg/v2/real-time/api/rainfall`
- **Format**: JSON with nested structure
- **Update Frequency**: Every 5 minutes
- **Error Handling**: Robust retry mechanisms

## 📈 Analysis Methods

### 1. Ranking Analysis
```python
# Top 10 highest rainfall areas
top_rainfall = data.groupby(['station_id', 'station_name']).agg({
    'rainfall_mm': ['sum', 'mean', 'count']
}).nlargest(10, 'total_rainfall')
```

### 2. Temporal Analysis
```python
# Hourly distribution across Singapore
hourly_stats = data.groupby('hour').agg({
    'rainfall_mm': ['sum', 'mean', 'count', 'std']
})
```

### 3. Alert System
```python
# Areas exceeding threshold
monthly_avg = data['rainfall_mm'].mean()
threshold = monthly_avg * 1.5
alert_areas = stations[stations['rainfall_mm'] > threshold]
```

## 🎨 Visualization Strategy

### Chart Types
- **Bar Charts**: Station comparisons
- **Line Charts**: Temporal trends  
- **Scatter Maps**: Geographic distribution
- **Metrics**: Key performance indicators

### Design Principles
- **Clean Interface**: Minimal, focused design
- **Interactive Elements**: Hover, zoom, filter capabilities
- **Responsive Layout**: Works on desktop and mobile
- **Color Coding**: Intuitive visual indicators

## 📱 Dashboard Usage

### Navigation
1. **Sidebar Controls**: Data loading and filter options
2. **Main Dashboard**: Visual analytics and charts
3. **Alert Panel**: Real-time threshold monitoring
4. **Data Tables**: Detailed numerical information

### Key Interactions
- **Refresh Data**: Load latest API data
- **Date Selection**: View historical data
- **Station Grouping**: Combine nearby locations
- **Raw Data View**: Access underlying dataset
- **CSV Export**: Download processed data

## 🚨 Alert System Details

### Threshold Calculation
- **Base**: Monthly average rainfall
- **Multiplier**: 1.5x (configurable)
- **Updates**: Real-time with new data

### Alert Levels
- **🟡 Moderate**: 25-50% above average
- **🟠 High**: 50-100% above average  
- **🔴 Severe**: 100%+ above average

### Notification Methods
- Visual dashboard alerts
- Color-coded indicators
- Detailed excess calculations

## 🧪 Testing & Validation

### Test Scripts
```bash
# API connectivity
python test_api.py

# Data processing
python data_processor.py

# Analysis functions  
python analyzer.py
```

### Expected Outputs
- ✅ API connection successful
- ✅ Data processing complete
- ✅ Analysis functions working
- ✅ Dashboard renders correctly

## 📊 Sample Output

### API Test Results
```
🌧️ Testing Singapore Rainfall API...
==================================================
✅ Status Code: 200
✅ Response Code: 0
📍 Number of Stations: 69
📊 Number of Readings: 1
📍 Sample Station: Admiralty (ID: S43)
⏰ Latest Reading Time: 2024-01-15T14:00:00.000Z
📈 Data Points in Latest Reading: 69
✅ API Test SUCCESSFUL!
```

### Data Processing Results
```
📡 Fetching rainfall data...
✅ Processed 69 rainfall readings from 69 stations
📊 Data Summary:
Total readings: 69
Stations: 69
Time range: 2024-01-15 14:00:00 to 2024-01-15 14:00:00
Average rainfall: 0.45 mm
```

## ⚙️ Configuration

### Environment Variables
```bash
# Optional configuration
STREAMLIT_PORT=8501
CACHE_TTL=300
ALERT_THRESHOLD_MULTIPLIER=1.5
DEBUG_MODE=false
```

### Customization Options
- Alert threshold multipliers
- Grouping distance for nearby stations
- Chart color schemes
- Update frequencies

## 🔧 Troubleshooting

### Common Issues

#### API Connection Failed
```bash
# Check internet connection
ping api-open.data.gov.sg

# Verify API endpoint
python test_api.py
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Dashboard Not Loading
```bash
# Check if Streamlit is installed
streamlit --version

# Try different port
streamlit run app.py --server.port 8502
```

### Error Messages
- **"No data available"**: API might be temporarily unavailable
- **"Module not found"**: Install missing dependencies
- **"Port already in use"**: Change port or stop other services

## 📈 Performance Optimization

### Caching Strategy
- **API Responses**: 5-minute TTL
- **Processed Data**: Session-based caching
- **Chart Rendering**: Streamlit native caching

### Efficiency Features
- Lazy loading of large datasets
- Optimized DataFrame operations
- Minimal API calls with pagination

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Container-based deployment
- **AWS/GCP**: Scalable cloud hosting

### Docker Deployment
```bash
# Build image
docker build -t rainfall-dashboard .

# Run container
docker run -p 8501:8501 rainfall-dashboard
```

## 📋 Requirements Compliance

### Assessment Checklist
- ✅ **Data Extraction**: Real-time API integration
- ✅ **Top 10 Highest**: Interactive charts and maps
- ✅ **Top 10 Lowest**: Complementary analysis
- ✅ **Hourly Distribution**: Time-based analytics
- ✅ **Alert Mechanism**: Threshold-based monitoring
- ✅ **Tool Choice**: Python ecosystem
- ✅ **Presentation**: Web-based dashboard
- ✅ **Documentation**: Comprehensive README

### Technical Stack
- **Language**: Python 3.8+
- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **API Integration**: Requests
- **Deployment**: Multiple options available

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd singapore-rainfall-dashboard

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings for functions
- Maintain consistent formatting

## 📄 License

This project is developed for technical assessment purposes. Please ensure compliance with Singapore Government API terms of use.

## 📞 Support

For technical questions or issues:
1. Check troubleshooting section
2. Review error messages carefully
3. Test individual components
4. Verify API connectivity

## 🔗 References

- [Singapore Government API Documentation](https://api-open.data.gov.sg)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python Documentation](https://plotly.com/python)
- [Pandas Documentation](https://pandas.pydata.org/docs)

---

**Built with ❤️ for Singapore's weather monitoring needs**
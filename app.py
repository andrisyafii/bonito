import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import time

# Import our custom modules
from data_processor import RainfallDataProcessor
from analyzer import RainfallAnalyzer

# Page configuration
st.set_page_config(
    page_title="Singapore Rainfall Dashboard",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-container {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-container {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_rainfall_data(date=None):
    """Load and process rainfall data with caching"""
    processor = RainfallDataProcessor()
    return processor.get_all_data(date)

def create_bar_chart(data, x_col, y_col, title, color_col=None):
    """Create styled bar chart"""
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        title=title,
        color=color_col or y_col,
        color_continuous_scale='Blues',
        labels={y_col: 'Rainfall (mm)', x_col: 'Station'}
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=500)
    return fig

def create_map_chart(data, title):
    """Create map visualization"""
    fig = px.scatter_mapbox(
        data,
        lat='latitude',
        lon='longitude',
        size='total_rainfall',
        color='total_rainfall',
        hover_name='station_name',
        hover_data={'total_rainfall': ':.2f'},
        color_continuous_scale='Viridis',
        size_max=20,
        zoom=10,
        title=title
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=1.3521, lon=103.8198)),  # Singapore center
        height=500,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

def create_hourly_chart(hourly_data):
    """Create hourly distribution chart"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total Rainfall by Hour', 'Average Rainfall by Hour'),
        vertical_spacing=0.1
    )
    
    # Total rainfall
    fig.add_trace(
        go.Scatter(
            x=hourly_data['hour'], 
            y=hourly_data['total_rainfall'],
            mode='lines+markers',
            name='Total',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    # Average rainfall
    fig.add_trace(
        go.Scatter(
            x=hourly_data['hour'], 
            y=hourly_data['avg_rainfall'],
            mode='lines+markers',
            name='Average',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Hour of Day", row=2, col=1)
    fig.update_yaxes(title_text="Total Rainfall (mm)", row=1, col=1)
    fig.update_yaxes(title_text="Average Rainfall (mm)", row=2, col=1)
    fig.update_layout(height=600, showlegend=False)
    
    return fig

def display_alert_panel(alert_data, threshold):
    """Display alert panel"""
    if alert_data.empty:
        st.markdown("""
        <div class="success-container">
            <h4>✅ All Clear</h4>
            <p>No areas currently exceeding rainfall thresholds</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-container">
            <h4>⚠️ Rainfall Alert</h4>
            <p><strong>{len(alert_data)} areas</strong> are exceeding the rainfall threshold of <strong>{threshold:.2f} mm</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each alert
        for _, area in alert_data.head(5).iterrows():  # Show top 5 alerts
            st.error(
                f"🚨 **{area['station_name']}**: {area['rainfall_mm']:.2f} mm "
                f"(+{area['excess_rainfall']:.2f} mm above threshold)"
            )

def main():
    # Title and header
    st.title("🌧️ Singapore Rainfall Dashboard")
    st.markdown("**Real-time rainfall monitoring and analysis across Singapore**")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Dashboard Controls")
        
        # Data loading options
        st.subheader("Data Options")
        date_option = st.selectbox(
            "Select Data Range",
            ["Current (Real-time)", "Specific Date"]
        )
        
        selected_date = None
        if date_option == "Specific Date":
            selected_date = st.date_input(
                "Select Date",
                value=datetime.now().date() - timedelta(days=1)
            ).strftime("%Y-%m-%d")
            st.info(f"Selected: {selected_date}")
        
        # Analysis options
        st.subheader("Analysis Options")
        group_nearby = st.checkbox("Group nearby stations", value=False)
        show_raw_data = st.checkbox("Show raw data table", value=False)
        
        # Refresh button
        st.markdown("---")
        refresh_data = st.button("🔄 Load/Refresh Data", type="primary")
    
    # Initialize session state
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        st.session_state.data = pd.DataFrame()
    
    # Load data
    if refresh_data or st.session_state.data.empty:
        with st.spinner("📡 Fetching rainfall data from Singapore API..."):
            try:
                data = load_rainfall_data(selected_date)
                if not data.empty:
                    st.session_state.data = data
                    st.session_state.data_loaded = True
                    st.success(f"✅ Loaded {len(data)} rainfall readings from {data['station_id'].nunique()} stations")
                else:
                    st.error("❌ No data available for the selected criteria")
                    return
            except Exception as e:
                st.error(f"❌ Error loading data: {e}")
                return
    
    # Use cached data
    data = st.session_state.data
    
    if data.empty:
        st.info("👆 Please load data using the sidebar controls")
        return
    
    # Initialize analyzer
    analyzer = RainfallAnalyzer(data)
    
    # Key metrics
    stats = analyzer.generate_summary_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Total Stations", stats['total_stations'])
    with col2:
        st.metric("📊 Total Readings", f"{stats['total_readings']:,}")
    with col3:
        st.metric("🌧️ Average Rainfall", f"{stats['avg_rainfall']:.2f} mm")
    with col4:
        st.metric("📈 Max Rainfall", f"{stats['max_rainfall']:.2f} mm")
    
    st.markdown("---")
    
    # Alert System (Requirement 2)
    st.header("🚨 Rainfall Alert System")
    alert_areas, threshold = analyzer.get_alert_areas()
    display_alert_panel(alert_areas, threshold)
    
    st.markdown("---")
    
    # Requirement 1a: Top 10 Highest Rainfall Areas
    st.header("📊 Top 10 Highest Rainfall Areas")
    top_rainfall = analyzer.get_top_rainfall_areas(10, group_nearby)
    
    if not top_rainfall.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_bar_chart(
                top_rainfall, 
                'station_name', 
                'total_rainfall', 
                "Top 10 Highest Rainfall Areas"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig_map1 = create_map_chart(top_rainfall, "Highest Rainfall Areas")
            st.plotly_chart(fig_map1, use_container_width=True)
        
        # Data table
        st.subheader("📋 Top Rainfall Areas Data")
        display_cols = ['station_name', 'total_rainfall', 'avg_rainfall', 'reading_count']
        st.dataframe(
            top_rainfall[display_cols].round(2),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Requirement 1b: Top 10 Lowest Rainfall Areas
    st.header("📉 Top 10 Lowest Rainfall Areas")
    lowest_rainfall = analyzer.get_lowest_rainfall_areas(10)
    
    if not lowest_rainfall.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = create_bar_chart(
                lowest_rainfall, 
                'station_name', 
                'total_rainfall', 
                "Top 10 Lowest Rainfall Areas"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            fig_map2 = create_map_chart(lowest_rainfall, "Lowest Rainfall Areas")
            st.plotly_chart(fig_map2, use_container_width=True)
        
        # Data table
        st.subheader("📋 Lowest Rainfall Areas Data")
        display_cols = ['station_name', 'total_rainfall', 'avg_rainfall', 'reading_count']
        st.dataframe(
            lowest_rainfall[display_cols].round(2),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Requirement 1c: Hourly Distribution
    st.header("⏰ Hourly Rainfall Distribution Across Singapore")
    hourly_data = analyzer.get_hourly_distribution()
    
    if not hourly_data.empty:
        fig3 = create_hourly_chart(hourly_data)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Peak hours analysis
        peak_hour = hourly_data.loc[hourly_data['total_rainfall'].idxmax()]
        low_hour = hourly_data.loc[hourly_data['total_rainfall'].idxmin()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🔝 **Peak Hour**: {peak_hour['hour']:02d}:00 with {peak_hour['total_rainfall']:.2f} mm")
        with col2:
            st.info(f"📉 **Lowest Hour**: {low_hour['hour']:02d}:00 with {low_hour['total_rainfall']:.2f} mm")
    
    # Raw data section
    if show_raw_data:
        st.markdown("---")
        st.header("📋 Raw Data")
        st.dataframe(data, use_container_width=True)
        
        # Download button
        csv = data.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"singapore_rainfall_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌧️ Singapore Rainfall Dashboard | Data from data.gov.sg | Updated every 5 minutes</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
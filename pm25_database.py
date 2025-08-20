import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import io
import base64
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="PM2.5 Database Portal",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .health-effect {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .seasonal-info {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data for demonstration
@st.cache_data
def generate_sample_data():
    """Generate sample PM2.5 data for demonstration"""
    np.random.seed(42)
    
    # Temporal data (hourly)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    
    temporal_data = []
    for date in date_range:
        # Simulate seasonal and daily patterns
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365.25)
        daily_factor = 1 + 0.2 * np.sin(2 * np.pi * date.hour / 24)
        
        pm25_value = np.random.normal(25, 8) * seasonal_factor * daily_factor
        pm25_value = max(0, pm25_value)  # Ensure non-negative values
        
        temporal_data.append({
            'datetime': date,
            'pm25_concentration': pm25_value,
            'station_id': np.random.choice(['ST001', 'ST002', 'ST003', 'ST004', 'ST005']),
            'location': np.random.choice(['Urban', 'Suburban', 'Rural', 'Industrial']),
            'data_source': 'Ground Station'
        })
    
    temporal_df = pd.DataFrame(temporal_data)
    
    # Spatial data (satellite-derived)
    spatial_data = []
    for i in range(1000):
        lat = np.random.uniform(6.0, 10.0)  # Sri Lanka region
        lon = np.random.uniform(79.5, 82.0)
        
        spatial_data.append({
            'latitude': lat,
            'longitude': lon,
            'pm25_concentration': np.random.normal(20, 10),
            'date': np.random.choice(pd.date_range('2023-01-01', '2023-12-31', freq='D')),
            'satellite_source': np.random.choice(['MODIS', 'VIIRS', 'Sentinel-5P']),
            'cloud_cover': np.random.uniform(0, 100),
            'data_quality': np.random.choice(['High', 'Medium', 'Low'])
        })
    
    spatial_df = pd.DataFrame(spatial_data)
    spatial_df['pm25_concentration'] = spatial_df['pm25_concentration'].clip(lower=0)
    
    return temporal_df, spatial_df

# Load or generate data
temporal_df, spatial_df = generate_sample_data()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌍 PM2.5 Environmental Database Portal</h1>
    <p style="text-align: center; color: white; margin: 0;">
        Comprehensive PM2.5 air quality data from ground stations and satellite observations
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header("🔍 Data Filters")

# Dataset selection
district = st.sidebar.selectbox(
    "Select District",
    ["Ampara", "Anuradhapura", "Batticaloa", "Battaramulla", "Galle", "Fort", "Hambanthota", 
     "Jaffna", "Kandy", "Kanthale", "Kilinochchi", 
     "Katubedda", "Mannar", "Matale", "Matara", "Monaragala", 
     "Mullaitivu", "Polonnaruwa", "PointPedro"]
)

selected_date = st.sidebar.date_input(
    "Select Date",
    value=datetime.today(),
    min_value=datetime(2023, 1, 1),
    max_value=datetime.today()  # allows selecting up to current date
)

# Load CSV for selected district
csv_path = os.path.join("new processed", f"Cleaned_{district}.xls")  # keep .xls extension, but treat as CSV
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["timestamp_index"])
else:
    st.error(f"CSV file for {district} not found!")
    st.stop()

# Filter data for selected date
filtered_temporal = df[df["timestamp_index"].dt.date == selected_date]

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🕒 Temporal Data", "🗺️ Spatial Data", "📥 Download"])

with tab1:
    st.header("📊 PM2.5 Information Dashboard")
    
    # Two main columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗺️ Sri Lanka PM2.5 Annual Mean Distribution")
        
        # Display the PM2.5 heat map image
        # Note: Replace 'your_image_path.jpg' with the actual path to your image file
        try:
            # If you have uploaded the image, use this format:
            # st.image("path_to_your_image.jpg", caption="PM2.5 Annual Mean Distribution in Sri Lanka", use_column_width=True)
            
            # For now, show a placeholder message
            
            st.image("PM2.5_heatmap.jpg", use_container_width=True)
            # Uncomment the line below and add your image path when ready:
            # st.image("sri_lanka_pm25_heatmap.jpg", use_column_width=True)
            
        except Exception as e:
            st.error(f"Could not load the heat map image: {str(e)}")
            st.info("Please ensure the image file is in the correct directory and the path is specified correctly.")
    
    with col2:
        st.subheader("📋 What is PM2.5?")
        st.markdown("""
        <div class="info-card">
        <h4>🔬 Definition</h4>
        <p><strong>PM2.5</strong> refers to particulate matter with a diameter of 2.5 micrometers or smaller. 
        These particles are so small that they can penetrate deep into the lungs and even enter the bloodstream.</p>
        
        <h4>📏 Size Comparison</h4>
        <p>• PM2.5 particles are about <strong>30 times smaller</strong> than the width of human hair</p>
        <p>• They are invisible to the naked eye</p>
        <p>• Can remain suspended in air for hours or days</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🏥 Health Effects")
        st.markdown("""
        <div class="health-effect">
        <h4>⚠️ Short-term Effects</h4>
        <p>• Eye, nose, and throat irritation</p>
        <p>• Coughing and sneezing</p>
        <p>• Shortness of breath</p>
        <p>• Asthma attacks</p>
        </div>
        
        <div class="health-effect">
        <h4>🚨 Long-term Effects</h4>
        <p>• Cardiovascular disease</p>
        <p>• Lung cancer</p>
        <p>• Chronic respiratory diseases</p>
        <p>• Premature death</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seasonal Variation Section
    st.subheader("🌡️ Seasonal Variation of PM2.5 in Sri Lanka")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create seasonal variation chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        pm25_levels = [32, 28, 25, 22, 20, 18, 19, 21, 24, 28, 35, 38]  # Sample data
        
        fig_seasonal = go.Figure()
        fig_seasonal.add_trace(go.Scatter(
            x=months,
            y=pm25_levels,
            mode='lines+markers',
            name='PM2.5 Levels',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig_seasonal.update_layout(
            title='Average PM2.5 Levels Throughout the Year in Sri Lanka',
            xaxis_title='Month',
            yaxis_title='PM2.5 Concentration (μg/m³)',
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="seasonal-info">
        <h4>🌊 Monsoon Seasons</h4>
        <p><strong>Southwest Monsoon</strong><br>
        May - September<br>
        Lower PM2.5 levels due to rain</p>
        
        <p><strong>Northeast Monsoon</strong><br>
        October - January<br>
        Higher PM2.5 in some regions</p>
        
        <p><strong>Inter-monsoon</strong><br>
        March - April<br>
        Variable levels</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Information
    st.subheader("🌍 Key Factors Affecting PM2.5 in Sri Lanka")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
        <h4>🏭 Sources</h4>
        <p>• Vehicle emissions</p>
        <p>• Industrial activities</p>
        <p>• Biomass burning</p>
        <p>• Construction dust</p>
        <p>• Transboundary pollution</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
        <h4>🌤️ Weather Factors</h4>
        <p>• Wind patterns</p>
        <p>• Rainfall</p>
        <p>• Temperature inversions</p>
        <p>• Humidity levels</p>
        <p>• Atmospheric pressure</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
        <h4>📊 WHO Guidelines</h4>
        <p><strong>Annual Mean:</strong> 5 μg/m³</p>
        <p><strong>24-hour Mean:</strong> 15 μg/m³</p>
        <p><br></p>
        <p><strong>Sri Lanka Standard:</strong></p>
        <p>Annual: 25 μg/m³</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("🕒 Temporal PM2.5 Data")
    # Check if a district and date are selected
    if district is None or selected_date is None or len(filtered_temporal) == 0:
        st.info("No district and date selected yet or no data available for the selection.")
    else:
        st.write(f"**Filtered Records for {district} on {selected_date}:** {len(filtered_temporal):,}")
        st.dataframe(
            filtered_temporal[
                ["timestamp_index", "PM2.5 (ug/m3)", "Temperature (Celsius)", "Relative Humidity (%)", "hour", "day", "dayofweek", "month"]
            ],
            use_container_width=True,
            height=400
        )
        fig = px.line(
            filtered_temporal,
            x="timestamp_index",
            y="PM2.5 (ug/m3)",
            title=f"PM2.5 Concentration on {selected_date} ({district})",
            labels={"PM2.5 (ug/m3)": "PM2.5 (μg/m³)", "timestamp_index": "Time"}
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🗺️ Spatial PM2.5 Data")
    
     # Additional filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_satellites = st.multiselect(
            "Select Satellite Sources",
            options=spatial_df['satellite_source'].unique(),
            default=spatial_df['satellite_source'].unique()
        )
    
    with col2:
        cloud_cover_max = st.slider(
            "Maximum Cloud Cover (%)",
            min_value=0,
            max_value=100,
            value=80
        )

# Before tab4 (Download Data), add this:
filtered_spatial_download = spatial_df.copy()

with tab4:
    st.header("📥 Download Data")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🕒 Temporal Data")
        # Excel download only if data is available
        if len(filtered_temporal) > 0:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                filtered_temporal.to_excel(writer, sheet_name='PM25_Temporal', index=False)
            st.download_button(
                label="📊 Download as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"pm25_temporal_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="temporal_excel"
            )
        else:
            st.info("No temporal data available for download.")
    
    with col2:
        st.subheader("🗺️ Spatial Data")
        
        st.write(f"Records available: {len(filtered_spatial_download):,}")
        
        # CSV download
        csv_spatial = filtered_spatial_download.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv_spatial,
            file_name=f"pm25_spatial_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="spatial_csv"
        )
        
        # Excel download
        excel_buffer_spatial = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_spatial, engine='openpyxl') as writer:
            filtered_spatial_download.to_excel(writer, sheet_name='PM25_Spatial', index=False)
        
        st.download_button(
            label="📊 Download as Excel",
            data=excel_buffer_spatial.getvalue(),
            file_name=f"pm25_spatial_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="spatial_excel"
        )
    
    # Combined download
    st.subheader("📦 Combined Dataset")
    
    if st.button("🔄 Prepare Combined Dataset"):
        # Merge temporal and spatial data
        temporal_for_merge = temporal_df.copy()
        temporal_for_merge['data_type'] = 'Temporal'
        temporal_for_merge['latitude'] = np.nan
        temporal_for_merge['longitude'] = np.nan
        
        spatial_for_merge = filtered_spatial_download.copy()
        spatial_for_merge['data_type'] = 'Spatial'
        spatial_for_merge['datetime'] = spatial_for_merge['date']
        spatial_for_merge['station_id'] = 'Satellite'
        spatial_for_merge['location'] = 'Satellite'
        spatial_for_merge['data_source'] = spatial_for_merge['satellite_source']
        
        # Align columns
        common_columns = ['datetime', 'pm25_concentration', 'latitude', 'longitude', 'data_type', 'station_id', 'location', 'data_source']
        
        temporal_aligned = temporal_for_merge[common_columns]
        spatial_aligned = spatial_for_merge[common_columns]
        
        combined_data = pd.concat([temporal_aligned, spatial_aligned], ignore_index=True)
        
        combined_csv = combined_data.to_csv(index=False)
        st.download_button(
            label="📄 Download Combined Dataset (CSV)",
            data=combined_csv,
            file_name=f"pm25_combined_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="combined_csv"
        )
        
        st.success(f"Combined dataset prepared with {len(combined_data):,} records!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🌍 PM2.5 Environmental Database Portal | Built with Streamlit</p>
    <p>For research and educational purposes. Data quality and availability may vary.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📖 About This Database
This portal provides access to PM2.5 air quality data from:
- **Temporal Data**: Hourly measurements from ground stations
- **Spatial Data**: Satellite-derived observations

### 🔧 Features
- Interactive data visualization
- Advanced filtering options
- Multiple download formats
- Real-time data exploration

### 📊 Data Sources
- Ground monitoring stations
- MODIS satellite data
- VIIRS satellite data
- Sentinel-5P satellite data
""")
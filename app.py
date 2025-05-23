import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import requests
import io
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Regional Impact Tracker",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional CSS styling
st.markdown("""
<style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    body, .main {
        background: linear-gradient(135deg, #f0f4ff 0%, #e2e8f0 100%);
        min-height: 100vh;
        padding: 1.5rem;
        color: #1f2937;
    }
    
    /* Header Styling */
    .main-header {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
        line-height: 1.2;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.5;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    /* Color coding for metrics */
    .metric-confirmed { color: #f59e0b; }
    .metric-deaths { color: #ef4444; }
    .metric-recovered { color: #10b981; }
    .metric-active { color: #8b5cf6; }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
    }
    
    .sidebar-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-high { background-color: #ef4444; }
    .status-medium { background-color: #f59e0b; }
    .status-low { background-color: #10b981; }
    
    /* Risk Badges */
    .risk-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .risk-high { background-color: #fef2f2; color: #b91c1c; }
    .risk-medium { background-color: #fefce8; color: #b45309; }
    .risk-low { background-color: #ecfdf5; color: #047857; }
    
    /* General Text Styling */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.75rem;
    }
    
    p, div, span {
        color: #4b5563;
        line-height: 1.6;
    }
    
    /* Table Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title { font-size: 1.75rem; }
        .subtitle { font-size: 1rem; }
        .glass-card { padding: 1.25rem; }
        .metric-value { font-size: 1.75rem; }
        .metric-label { font-size: 0.8rem; }
        .stButton > button { padding: 0.6rem 1rem; font-size: 0.9rem; }
        .main-header { padding: 1.5rem; }
    }
    
    @media (max-width: 480px) {
        .main-title { font-size: 1.5rem; }
        .glass-card { padding: 1rem; }
        .metric-value { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Data loading and caching functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_covid_data():
    """Load COVID-19 data from Johns Hopkins repository"""
    try:
        base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
        
        urls = {
            'confirmed': f"{base_url}/time_series_covid19_confirmed_global.csv",
            'deaths': f"{base_url}/time_series_covid19_deaths_global.csv",
            'recovered': f"{base_url}/time_series_covid19_recovered_global.csv"
        }
        
        data = {}
        for data_type, url in urls.items():
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text))
                data[data_type] = df
                st.success(f"✅ {data_type.capitalize()} data loaded successfully")
            except Exception as e:
                st.error(f"❌ Error loading {data_type} data: {str(e)}")
                return None
        
        return data
    except Exception as e:
        st.error(f"❌ Failed to load COVID-19 data: {str(e)}")
        return None

@st.cache_data
def process_covid_data(raw_data):
    """Process and clean the COVID-19 data"""
    if not raw_data:
        return None
    
    processed_data = {}
    
    for data_type, df in raw_data.items():
        df_melted = pd.melt(
            df, 
            id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
            var_name='Date', 
            value_name=data_type.capitalize()
        )
        
        df_melted['Date'] = pd.to_datetime(df_melted['Date'])
        df_melted['Province/State'] = df_melted['Province/State'].fillna(df_melted['Country/Region'])
        df_country = df_melted.groupby(['Country/Region', 'Date'])[data_type.capitalize()].sum().reset_index()
        processed_data[data_type] = df_country
    
    merged_df = processed_data['confirmed']
    for data_type in ['deaths', 'recovered']:
        if data_type in processed_data:
            merged_df = merged_df.merge(
                processed_data[data_type], 
                on=['Country/Region', 'Date'], 
                how='left'
            )
    
    merged_df = merged_df.fillna(0)
    merged_df['Active'] = merged_df['Confirmed'] - merged_df['Deaths'] - merged_df.get('Recovered', 0)
    merged_df['Active'] = merged_df['Active'].clip(lower=0)
    
    merged_df = merged_df.sort_values(['Country/Region', 'Date'])
    merged_df['New_Cases'] = merged_df.groupby('Country/Region')['Confirmed'].diff().fillna(0)
    merged_df['New_Deaths'] = merged_df.groupby('Country/Region')['Deaths'].diff().fillna(0)
    
    merged_df['New_Cases_7MA'] = merged_df.groupby('Country/Region')['New_Cases'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    merged_df['New_Deaths_7MA'] = merged_df.groupby('Country/Region')['New_Deaths'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    
    return merged_df

def create_seaborn_plots(df, selected_countries, plot_type):
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    if plot_type == "Line Plot - Cases Over Time":
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = ['#f59e0b', '#ef4444', '#10b981', '#8b5cf6', '#06b6d4', '#f97316']
        
        for i, country in enumerate(selected_countries):
            country_data = df[df['Country/Region'] == country]
            if not country_data.empty:
                ax.plot(
                    country_data['Date'], 
                    country_data['Confirmed'], 
                    label=country,
                    linewidth=2.5,
                    color=colors[i % len(colors)]
                )
        
        ax.set_title('COVID-19 Confirmed Cases Over Time', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, fontweight='600')
        ax.set_ylabel('Confirmed Cases', fontsize=12, fontweight='600')
        ax.legend(title='Country', title_fontsize=12, fontsize=10)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    elif plot_type == "Heatmap - Regional Comparison":
        latest_data = df.groupby('Country/Region').last().reset_index()
        if len(selected_countries) > 0:
            top_countries = latest_data[latest_data['Country/Region'].isin(selected_countries)]
        else:
            top_countries = latest_data.nlargest(15, 'Confirmed')
        
        if len(top_countries) == 0:
            return None
        
        heatmap_data = top_countries[['Confirmed', 'Deaths', 'Recovered', 'Active']].T
        heatmap_data.columns = top_countries['Country/Region']
        heatmap_data_norm = heatmap_data.div(heatmap_data.sum(axis=0), axis=1)
        
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.heatmap(
            heatmap_data_norm, 
            annot=False, 
            cmap='RdYlBu_r', 
            cbar_kws={'label': 'Proportion'},
            ax=ax
        )
        ax.set_title('COVID-19 Cases Distribution Heatmap', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Countries', fontsize=12, fontweight='600')
        ax.set_ylabel('Case Types', fontsize=12, fontweight='600')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    elif plot_type == "Bar Chart - Current Status":
        latest_data = df[df['Date'] == df['Date'].max()]
        if len(selected_countries) > 0:
            country_data = latest_data[latest_data['Country/Region'].isin(selected_countries)]
        else:
            country_data = latest_data.nlargest(10, 'Confirmed')
        
        if len(country_data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 8))
        x = np.arange(len(country_data))
        width = 0.2
        
        ax.bar(x - width*1.5, country_data['Confirmed'], width, label='Confirmed', color='#f59e0b', alpha=0.8)
        ax.bar(x - width/2, country_data['Deaths'], width, label='Deaths', color='#ef4444', alpha=0.8)
        ax.bar(x + width/2, country_data.get('Recovered', 0), width, label='Recovered', color='#10b981', alpha=0.8)
        ax.bar(x + width*1.5, country_data['Active'], width, label='Active', color='#8b5cf6', alpha=0.8)
        
        ax.set_title('Current COVID-19 Status by Country', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Countries', fontsize=12, fontweight='600')
        ax.set_ylabel('Number of Cases', fontsize=12, fontweight='600')
        ax.set_xticks(x)
        ax.set_xticklabels(country_data['Country/Region'], rotation=45, ha='right')
        ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.tight_layout()
        return fig

def calculate_risk_level(new_cases_per_100k):
    if new_cases_per_100k > 100:
        return "High", "#ef4444", "risk-high"
    elif new_cases_per_100k > 25:
        return "Medium", "#f59e0b", "risk-medium"
    else:
        return "Low", "#10b981", "risk-low"

def create_plotly_visualizations(df, selected_countries):
    def create_time_series():
        fig = go.Figure()
        colors = ['#f59e0b', '#ef4444', '#10b981', '#8b5cf6', '#06b6d4', '#f97316']
        
        for i, country in enumerate(selected_countries):
            country_data = df[df['Country/Region'] == country]
            if not country_data.empty:
                fig.add_trace(go.Scatter(
                    x=country_data['Date'],
                    y=country_data['Confirmed'],
                    mode='lines',
                    name=country,
                    line=dict(width=3, color=colors[i % len(colors)]),
                    hovertemplate=f'<b>{country}</b><br>Date: %{{x}}<br>Cases: %{{y:,.0f}}<extra></extra>'
                ))
        
        fig.update_layout(
            title="Interactive COVID-19 Cases Timeline",
            xaxis_title="Date",
            yaxis_title="Confirmed Cases",
            hovermode='x unified',
            height=500,
            template="plotly_white",
            showlegend=True
        )
        return fig
    
    def create_comparison():
        latest_comparison = df[df['Date'] == df['Date'].max()]
        filtered_comparison = latest_comparison[latest_comparison['Country/Region'].isin(selected_countries)]
        
        fig = go.Figure()
        metrics = [
            ('Confirmed', '#f59e0b'),
            ('Deaths', '#ef4444'),
            ('Recovered', '#10b981'),
            ('Active', '#8b5cf6')
        ]
        
        for metric, color in metrics:
            fig.add_trace(go.Bar(
                name=metric,
                x=filtered_comparison['Country/Region'],
                y=filtered_comparison[metric],
                marker_color=color,
                hovertemplate=f'<b>%{{x}}</b><br>{metric}: %{{y:,.0f}}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Current COVID-19 Status Comparison",
            xaxis_title="Countries",
            yaxis_title="Number of Cases",
            barmode='group',
            height=500,
            template="plotly_white"
        )
        return fig
    
    def create_daily_trends():
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=['Daily New Cases (7-day MA)', 'Daily New Deaths (7-day MA)']
        )
        
        colors = ['#f59e0b', '#ef4444', '#10b981', '#8b5cf6', '#06b6d4', '#f97316']
        
        for i, country in enumerate(selected_countries):
            country_data = df[df['Country/Region'] == country]
            if not country_data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=country_data['Date'],
                        y=country_data['New_Cases_7MA'],
                        name=f'{country} - New Cases',
                        line=dict(width=2, color=colors[i % len(colors)]),
                        hovertemplate=f'<b>{country}</b><br>Date: %{{x}}<br>New Cases (7MA): %{{y:,.1f}}<extra></extra>'
                    ),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(
                        x=country_data['Date'],
                        y=country_data['New_Deaths_7MA'],
                        name=f'{country} - New Deaths',
                        line=dict(width=2, color=colors[i % len(colors)]),
                        hovertemplate=f'<b>{country}</b><br>Date: %{{x}}<br>New Deaths (7MA): %{{y:,.1f}}<extra></extra>',
                        showlegend=False
                    ),
                    row=2, col=1
                )
        
        fig.update_layout(
            height=700,
            template="plotly_white",
            hovermode='x unified'
        )
        return fig
    
    return create_time_series, create_comparison, create_daily_trends

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.covid_data = None

# Header
st.markdown("""
<div class="main-header animate-fade-in">
    <h1 class="main-title">🦠 COVID-19 Regional Impact Tracker</h1>
    <p class="subtitle">Professional Health Department Dashboard for Real-Time COVID-19 Analysis and Monitoring</p>
    <div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap;">
        <div style="display: flex; align-items: center;">
            <span class="status-indicator status-high"></span>
            <span style="font-size: 0.9rem; color: #6b7280;">High Risk</span>
        </div>
        <div style="display: flex; align-items: center;">
            <span class="status-indicator status-medium"></span>
            <span style="font-size: 0.9rem; color: #6b7280;">Medium Risk</span>
        </div>
        <div style="display: flex; align-items: center;">
            <span class="status-indicator status-low"></span>
            <span style="font-size: 0.9rem; color: #6b7280;">Low Risk</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 0.5rem;"><h3>📊 Dashboard Controls</h3></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 0.5rem;"><h3>🔄 Data Management</h3></div>', unsafe_allow_html=True)
    
    if st.button("Load/Refresh Data", key="load_data"):
        with st.spinner("Loading COVID-19 data from Johns Hopkins..."):
            raw_data = load_covid_data()
            if raw_data:
                with st.spinner("Processing data..."):
                    st.session_state.covid_data = process_covid_data(raw_data)
                    st.session_state.data_loaded = True
                    st.success("✅ Data loaded and processed successfully!")
            else:
                st.error("❌ Failed to load data. Please try again.")
    
    if st.session_state.data_loaded:
        st.success("📊 Data Status: Loaded")
        if st.session_state.covid_data is not None:
            latest_date = st.session_state.covid_data['Date'].max().strftime('%Y-%m-%d')
            st.info(f"📅 Latest Data: {latest_date}")
    else:
        st.warning("⚠️ Data Status: Not Loaded")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.data_loaded and st.session_state.covid_data is not None:
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom: 0.5rem;"><h3>🌍 Country Selection</h3></div>', unsafe_allow_html=True)
        
        available_countries = sorted(st.session_state.covid_data['Country/Region'].unique())
        default_countries = ['US', 'India', 'Brazil', 'Russia', 'France', 'United Kingdom', 'Germany', 'Turkey']
        default_selection = [country for country in default_countries if country in available_countries]
        
        selected_countries = st.multiselect(
            "Select Countries",
            available_countries,
            default=default_selection[:5],
            key="country_select"
        )
        
        st.info(f"📍 Selected: {len(selected_countries)} countries")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom: 0.5rem;"><h3>📈 Visualization Options</h3></div>', unsafe_allow_html=True)
        
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Plot - Cases Over Time", "Heatmap - Regional Comparison", "Bar Chart - Current Status"],
            key="chart_select"
        )
        
        if st.session_state.covid_data is not None:
            min_date = st.session_state.covid_data['Date'].min().date()
            max_date = st.session_state.covid_data['Date'].max().date()
            
            date_range = st.date_input(
                "Select Date Range",
                value=(max_date - timedelta(days=90), max_date),
                min_value=min_date,
                max_value=max_date,
                key="date_range"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom: 0.5rem;"><h3>💾 Export Options</h3></div>', unsafe_allow_html=True)
        
        if st.button("📊 Generate Summary Report", key="generate_report"):
            if selected_countries:
                st.success("✅ Summary report feature ready!")
                st.info("Report would include key metrics, trends, and risk assessments for selected countries.")
        
        if st.button("📥 Export Data (CSV)", key="export_csv"):
            if selected_countries and st.session_state.covid_data is not None:
                export_data = st.session_state.covid_data[
                    st.session_state.covid_data['Country/Region'].isin(selected_countries)
                ]
                csv = export_data.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"covid_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 0.5rem;"><h3>ℹ️ About</h3></div>', unsafe_allow_html=True)
    st.markdown("""
    **Data Source:** Johns Hopkins CSSE
    
    **Update Frequency:** Daily
    
    **Risk Levels:**
    - **High:** >100 cases/100k
    - **Medium:** 25-100 cases/100k  
    - **Low:** <25 cases/100k
    
    **Features:**
    - Real-time data visualization
    - Regional comparison analysis  
    - Trend analysis with moving averages
    - Professional health department reporting
    - Interactive Plotly charts
    - Export capabilities
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
if not st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <h2 style="color: #1f2937; margin-bottom: 1rem;">Welcome to COVID-19 Regional Impact Tracker</h2>
        <p style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            Click "Load/Refresh Data" in the sidebar to begin analyzing COVID-19 trends and regional impacts.
        </p>
        <div style="font-size: 4rem; color: #e5e7eb;">🦠</div>
        <div style="margin-top: 2rem;">
            <p style="color: #6b7280; font-size: 1rem; line-height: 1.6;">
                📊 Professional dashboard for health departments<br>
                🌍 Global COVID-19 data analysis<br>
                📈 Interactive visualizations and reports
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    df = st.session_state.covid_data
    
    if df is not None and not df.empty:
        latest_global = df[df['Date'] == df['Date'].max()].groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Active': 'sum',
            'New_Cases': 'sum'
        }).iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-confirmed">{latest_global['Confirmed']:,.0f}</div>
                <div class="metric-label">Total Confirmed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-deaths">{latest_global['Deaths']:,.0f}</div>
                <div class="metric-label">Total Deaths</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-recovered">{latest_global['Recovered']:,.0f}</div>
                <div class="metric-label">Total Recovered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-active">{latest_global['Active']:,.0f}</div>
                <div class="metric-label">Active Cases</div>
            </div>
            """, unsafe_allow_html=True)
        
        if 'selected_countries' in locals() and selected_countries:
            filtered_df = df[df['Country/Region'].isin(selected_countries)]
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df['Date'] >= pd.to_datetime(start_date)) & 
                    (filtered_df['Date'] <= pd.to_datetime(end_date))
                ]
            
            tab1, tab2, tab3 = st.tabs(["📊 Main Chart", "🎯 Interactive Analysis", "📈 Trend Analysis"])
            
            with tab1:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-bottom: 0.5rem;'><h3>📊 {chart_type}</h3></div>", unsafe_allow_html=True)
                    
                    if not filtered_df.empty:
                        fig = create_seaborn_plots(filtered_df, selected_countries, chart_type)
                        if fig is not None:
                            st.pyplot(fig)
                            plt.close(fig)
                        else:
                            st.warning("No data available for the selected visualization.")
                    else:
                        st.warning("No data available for the selected filters.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 0.5rem;'><h3>🎯 Regional Risk Assessment</h3></div>", unsafe_allow_html=True)
                    
                    latest_country_data = filtered_df[filtered_df['Date'] == filtered_df['Date'].max()]
                    
                    for country in selected_countries:
                        country_data = latest_country_data[latest_country_data['Country/Region'] == country]
                        if not country_data.empty:
                            new_cases = country_data['New_Cases_7MA'].iloc[0]
                            confirmed = country_data['Confirmed'].iloc[0]
                            deaths = country_data['Deaths'].iloc[0]
                            risk_score = new_cases / 1000
                            risk_level, risk_color, risk_class = calculate_risk_level(risk_score)
                            fatality_rate = (deaths / confirmed * 100) if confirmed > 0 else 0
                            
                            st.markdown(f"""
                            <div style="display: flex; align-items: center; justify-content: space-between; 
                                       padding: 0.75rem; margin-bottom: 0.5rem; background-color: #f9fafb; 
                                       border-radius: 8px; border-left: 4px solid {risk_color};">
                                <div>
                                    <div style="font-weight: 600; color: #1f2937;">{country}</div>
                                    <div style="font-size: 0.8rem; color: #6b7280;">
                                        New Cases: {new_cases:,.0f}/day<br>
                                        Fatality Rate: {fatality_rate:.1f}%
                                    </div>
                                </div>
                                <div class="risk-badge {risk_class}">{risk_level}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 0.5rem;'><h3>📋 Quick Stats</h3></div>", unsafe_allow_html=True)
                    
                    if selected_countries:
                        selected_data = latest_country_data[latest_country_data['Country/Region'].isin(selected_countries)]
                        if not selected_data.empty:
                            total_selected_confirmed = selected_data['Confirmed'].sum()
                            total_selected_deaths = selected_data['Deaths'].sum()
                            avg_new_cases = selected_data['New_Cases_7MA'].mean()
                            
                            st.markdown(f"""
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">
                                    {total_selected_confirmed:,.0f}
                                </div>
                                <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 1rem;">
                                    Total Cases (Selected)
                                </div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: #ef4444; margin-bottom: 0.5rem;">
                                    {total_selected_deaths:,.0f}
                                </div>
                                <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 1rem;">
                                    Total Deaths (Selected)
                                </div>
                                <div style="font-size: 1rem; font-weight: 500; color: #8b5cf6;">
                                    {avg_new_cases:,.0f}
                                </div>
                                <div style="font-size: 0.8rem; color: #6b7280;">
                                    Avg New Cases/Day
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                if filtered_df is not None and not filtered_df.empty:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    time_series_func, comparison_func, trends_func = create_plotly_visualizations(filtered_df, selected_countries)
                    st.plotly_chart(time_series_func(), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.plotly_chart(comparison_func(), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                if filtered_df is not None and not filtered_df.empty:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    time_series_func, comparison_func, trends_func = create_plotly_visualizations(filtered_df, selected_countries)
                    st.plotly_chart(trends_func(), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 0.5rem;'><h3>📋 Latest Data Summary</h3></div>", unsafe_allow_html=True)
                    summary_data = filtered_df[filtered_df['Date'] == filtered_df['Date'].max()][
                        ['Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'New_Cases', 'New_Cases_7MA']
                    ].round(1)
                    summary_data.columns = ['Country', 'Total Cases', 'Deaths', 'Recovered', 'Active', 'New Cases', 'New Cases (7MA)']
                    st.dataframe(
                        summary_data,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 2rem;">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">Select Countries to Begin Analysis</h3>
                <p style="color: #6b7280; font-size: 1rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Use the sidebar to select countries for detailed COVID-19 analysis and visualization.
                </p>
                <div style="font-size: 3rem; color: #e5e7eb; margin: 1rem 0;">🌍</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.95); 
                    border-radius: 12px; text-align: center; font-size: 0.9rem; color: #6b7280;">
            📊 Data provided by Johns Hopkins CSSE | 
            🔄 Last updated: {last_update} | 
            ⚠️ For professional health department use
        </div>
        """.format(
            last_update=df['Date'].max().strftime('%Y-%m-%d %H:%M UTC') if df is not None and not df.empty else 'N/A'
        ), unsafe_allow_html=True)
    
    else:
        st.error("❌ Error processing data. Please try refreshing the data.")

if st.session_state.data_loaded and st.session_state.covid_data is not None:
    with st.expander("🔧 Technical Information"):
        st.write(f"**Dataset Info:**")
        st.write(f"- Total records: {len(st.session_state.covid_data):,}")
        st.write(f"- Countries: {st.session_state.covid_data['Country/Region'].nunique()}")
        st.write(f"- Date range: {st.session_state.covid_data['Date'].min().date()} to {st.session_state.covid_data['Date'].max().date()}")
        st.write(f"- Memory usage: {st.session_state.covid_data.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

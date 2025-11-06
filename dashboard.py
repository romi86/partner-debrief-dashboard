"""
Partner Debrief Intelligence Dashboard
A sophisticated analytics platform for transforming coach feedback into strategic partner intelligence.
Created by Romina Labanca, Coach Community Associate | BetterUp
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Import Google Sheets libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Import custom modules
from data_processor import DebriefDataProcessor
from visualizer import DebriefVisualizer
from report_exporter import ReportExporter

# Page configuration
st.set_page_config(
    page_title="BetterUp Partner Debrief Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Rubine Color Theme
st.markdown("""
    <style>
    /* Main color scheme - Rubine */
    :root {
        --rubine: #CE0058;
        --rubine-light: #E91E7A;
        --rubine-dark: #A3004A;
        --accent-orange: #FF6B35;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #CE0058 0%, #FF6B35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1rem;
    }
    
    .creator-credit {
        font-size: 0.9rem;
        color: #CE0058;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* Metric cards with Rubine gradient */
    .metric-card {
        background: linear-gradient(135deg, #CE0058 0%, #E91E7A 50%, #FF6B35 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(206, 0, 88, 0.2);
    }
    
    /* Insight cards with Rubine accent */
    .insight-card {
        background: #FFF5F9;
        border-left: 4px solid #CE0058;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
        box-shadow: 0 2px 4px rgba(206, 0, 88, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #CE0058 0%, #E91E7A 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #A3004A 0%, #CE0058 100%);
        box-shadow: 0 4px 12px rgba(206, 0, 88, 0.3);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF5F9 0%, #FFFFFF 100%);
    }
    
    /* Radio buttons and selectbox with Rubine */
    .stRadio > label, .stSelectbox > label {
        color: #CE0058;
        font-weight: 600;
    }
    
    /* Metrics with Rubine accent */
    [data-testid="stMetricValue"] {
        color: #CE0058;
    }
    
    /* Headers with Rubine */
    h1, h2, h3 {
        color: #1E3A8A;
    }
    
    h2::before, h3::before {
        content: "";
        display: inline-block;
        width: 4px;
        height: 1em;
        background: linear-gradient(180deg, #CE0058 0%, #FF6B35 100%);
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    
    /* Download button special styling */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #CE0058 0%, #FF6B35 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(206, 0, 88, 0.2);
    }
    
    /* Info and warning boxes */
    .stAlert {
        border-left: 4px solid #CE0058;
    }
    
    /* Expander with Rubine */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #FFF5F9 0%, #FFFFFF 100%);
        border-left: 3px solid #CE0058;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFF5F9;
        border-radius: 0.5rem 0.5rem 0 0;
        color: #CE0058;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #CE0058 0%, #E91E7A 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data_from_sheets(sheet_url):
    """Load and cache data from Google Sheets."""
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["gcp_service_account"], scope
        )
        
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url)
        
        # Try common worksheet names
        worksheet_names = ['Form_Responses', 'Form Responses 1', 'Sheet1', 'Form Responses']
        worksheet = None
        
        for name in worksheet_names:
            try:
                worksheet = sheet.worksheet(name)
                break
            except:
                continue
        
        if worksheet is None:
            worksheet = sheet.get_worksheet(0)
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        if df.empty:
            st.error("The Google Sheet appears to be empty.")
            return None
        
        # Create processor with the data
        processor = DebriefDataProcessor(None)
        processor.df = df
        processor.df.columns = processor.df.columns.str.strip()
        
        # Convert date columns
        date_columns = ['Timestamp', 'Debrief Session Date']
        for col in date_columns:
            if col in processor.df.columns:
                processor.df[col] = pd.to_datetime(processor.df[col], errors='coerce')
        
        # Extract unique partners
        partner_col = 'Which partner program was this Debrief connected to?'
        if partner_col in processor.df.columns:
            processor.partners = sorted(processor.df[partner_col].dropna().unique().tolist())
        
        # Calculate date range
        if 'Debrief Session Date' in processor.df.columns:
            valid_dates = processor.df['Debrief Session Date'].dropna()
            if len(valid_dates) > 0:
                processor.date_range = (valid_dates.min(), valid_dates.max())
        
        return processor
    except Exception as e:
        st.error(f"Error loading from Google Sheets: {str(e)}")
        st.info("Make sure you've shared the sheet with the service account and the URL is correct.")
        return None

def render_header():
    """Render the dashboard header with BetterUp logo."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="main-header">🎯 Partner Debrief Intelligence Dashboard</div>', 
                   unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Strategic Coach Intelligence • Organizational Insights • Executive Themes</div>', 
                   unsafe_allow_html=True)
        st.markdown('<div class="creator-credit">Created by Romina Labanca, Coach Community Associate | BetterUp</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        # Display BetterUp logo
        # Logo will be loaded from GitHub after you upload it there
        try:
            st.image("https://raw.githubusercontent.com/romi86/partner-debrief-dashboard/main/betterup_logo.png", 
                    width=200)
        except:
            # Fallback to text if logo doesn't load
            st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 2rem; font-weight: 700; 
                         background: linear-gradient(135deg, #CE0058 0%, #FF6B35 100%);
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        BetterUp
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_overview(processor, visualizer):
    """Render the overview dashboard."""
    st.markdown("## 📊 Executive Dashboard")
    
    # Key metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Debriefs", len(processor.df))
    
    with col2:
        st.metric("Active Partners", len(processor.partners) if processor.partners else 0)
    
    with col3:
        if processor.date_range:
            days = (processor.date_range[1] - processor.date_range[0]).days
            st.metric("Date Range", f"{days} days")
        else:
            st.metric("Date Range", "N/A")
    
    with col4:
        coaches = processor.df['Coach ID'].nunique() if 'Coach ID' in processor.df.columns else 0
        st.metric("Unique Coaches", coaches)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Partner Activity")
        fig = visualizer.create_partner_activity_chart(processor.df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📅 Debrief Timeline")
        fig = visualizer.create_timeline_chart(processor.df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Trends
    st.markdown("### 🎯 Organizational Pressure Trends")
    trends_data = processor.extract_theme_frequencies('organizational_pressures')
    if trends_data:
        fig = visualizer.create_trends_chart(trends_data)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available yet.")

def render_partner_deep_dive(processor, visualizer, exporter):
    """Render partner-specific analysis."""
    st.markdown("## 🔍 Partner Deep Dive")
    
    if not processor.partners:
        st.warning("No partners found in the data.")
        return
    
    selected_partner = st.selectbox(
        "Select Partner",
        options=processor.partners,
        help="Choose a partner to view detailed intelligence"
    )
    
    if selected_partner:
        partner_data = processor.get_partner_data(selected_partner)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Debrief Sessions", len(partner_data))
        
        with col2:
            coaches = partner_data['Coach ID'].nunique() if 'Coach ID' in partner_data.columns else 0
            st.metric("Coaches Engaged", coaches)
        
        with col3:
            if 'Debrief Session Date' in partner_data.columns:
                dates = pd.to_datetime(partner_data['Debrief Session Date'], errors='coerce').dropna()
                if len(dates) > 0:
                    last_date = dates.max().strftime('%Y-%m-%d')
                    st.metric("Last Debrief", last_date)
        
        st.markdown("---")
        
        # Strategic Intelligence with insight cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Organizational Pressures")
            pressures = processor.extract_themes(partner_data, 'organizational_pressures')
            if pressures:
                for pressure in pressures[:5]:
                    st.markdown(f'<div class="insight-card">• {pressure}</div>', unsafe_allow_html=True)
            else:
                st.info("No pressure data available.")
        
        with col2:
            st.markdown("### 💡 Leadership Challenges")
            challenges = processor.extract_themes(partner_data, 'leadership_challenges')
            if challenges:
                for challenge in challenges[:5]:
                    st.markdown(f'<div class="insight-card">• {challenge}</div>', unsafe_allow_html=True)
            else:
                st.info("No challenge data available.")
        
        # Export button
        st.markdown("---")
        if st.button("📥 Export Partner Report", key="export_partner"):
            with st.spinner("Generating executive report..."):
                report_data = processor.generate_partner_report(selected_partner)
                excel_file = exporter.create_partner_report(report_data, selected_partner)
                
                with open(excel_file, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Excel Report",
                        data=f.read(),
                        file_name=f"{selected_partner}_Intelligence_Report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_partner"
                    )
                
                os.remove(excel_file)
                st.success("✅ Report generated successfully!")

def render_comparison(processor, visualizer, exporter):
    """Render partner comparison view."""
    st.markdown("## 🔄 Partner Comparison")
    
    if not processor.partners or len(processor.partners) < 2:
        st.warning("Need at least 2 partners for comparison.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        partner1 = st.selectbox("Select First Partner", processor.partners, key="p1")
    
    with col2:
        other_partners = [p for p in processor.partners if p != partner1]
        partner2 = st.selectbox("Select Second Partner", other_partners, key="p2")
    
    if partner1 and partner2:
        st.markdown("---")
        
        # Comparison metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {partner1}")
            data1 = processor.get_partner_data(partner1)
            st.metric("Debrief Sessions", len(data1))
            st.metric("Unique Coaches", data1['Coach ID'].nunique() if 'Coach ID' in data1.columns else 0)
        
        with col2:
            st.markdown(f"### {partner2}")
            data2 = processor.get_partner_data(partner2)
            st.metric("Debrief Sessions", len(data2))
            st.metric("Unique Coaches", data2['Coach ID'].nunique() if 'Coach ID' in data2.columns else 0)
        
        # Comparison chart
        st.markdown("### 📊 Organizational Pressures Comparison")
        fig = visualizer.create_comparison_chart([partner1, partner2], processor)
        st.plotly_chart(fig, use_container_width=True)
        
        # Export
        if st.button("📥 Export Comparison Report", key="export_comparison"):
            with st.spinner("Generating comparison report..."):
                excel_file = exporter.create_comparison_report([partner1, partner2], processor)
                
                with open(excel_file, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Comparison Report",
                        data=f.read(),
                        file_name=f"Partner_Comparison_{partner1}_vs_{partner2}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_comparison"
                    )
                
                os.remove(excel_file)
                st.success("✅ Comparison report generated successfully!")

def render_strategic_insights(processor):
    """Render strategic insights view."""
    st.markdown("## 💡 Strategic Insights")
    
    # Cross-partner themes
    st.markdown("### 🌐 Cross-Partner Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Organizational Pressures")
        all_pressures = processor.extract_theme_frequencies('organizational_pressures')
        if all_pressures:
            for theme, count in list(all_pressures.items())[:8]:
                st.markdown(f"""
                    <div class="insight-card">
                        <strong>{theme}</strong><br/>
                        <span style="color: #CE0058; font-weight: 600;">{count} mentions</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No pressure data available.")
    
    with col2:
        st.markdown("#### Top Leadership Challenges")
        all_challenges = processor.extract_theme_frequencies('leadership_challenges')
        if all_challenges:
            for theme, count in list(all_challenges.items())[:8]:
                st.markdown(f"""
                    <div class="insight-card">
                        <strong>{theme}</strong><br/>
                        <span style="color: #CE0058; font-weight: 600;">{count} mentions</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No challenge data available.")
    
    st.markdown("---")
    
    # Implementation obstacles
    st.markdown("### 🚧 Implementation Obstacles")
    obstacles = processor.extract_theme_frequencies('implementation_obstacles')
    if obstacles:
        for theme, count in list(obstacles.items())[:10]:
            st.markdown(f"""
                <div class="insight-card">
                    <strong>{theme}</strong> 
                    <span style="color: #CE0058; font-weight: 600;">({count} mentions)</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No obstacle data available.")

def main():
    """Main application logic."""
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📂 Data Source")
        
        # Google Sheets URL input
        sheet_url = st.text_input(
            "Google Sheet URL",
            value="",
            help="Paste the full URL of your Google Sheet with survey responses",
            placeholder="https://docs.google.com/spreadsheets/d/..."
        )
        
        st.caption("📊 Data auto-refreshes every 5 minutes")
        
        # Manual refresh button
        if st.button("🔄 Refresh Data Now"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        st.markdown("## 🧭 Navigation")
        view = st.radio(
            "Select View",
            ["📊 Overview", "🔍 Partner Deep Dive", "🔄 Partner Comparison", "💡 Strategic Insights"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Partner Debrief Intelligence Dashboard**
            
            Transform coach insights into strategic intelligence for partner conversations.
            
            **Created by:** Romina Labanca  
            Coach Community Associate | BetterUp
            
            ---
            
            **This dashboard surfaces:**
            - Organizational pressures executives are facing
            - Leadership challenges emerging in coaching
            - Implementation obstacles preventing progress
            - Cross-partner trends and patterns
            
            **Core Intelligence:**
            - Real-time organizational pressure tracking
            - Leadership theme analysis across sessions
            - Implementation barrier identification
            - Strategic pattern recognition
            """)
    
    # Main content
    if not sheet_url:
        st.info("👆 Please enter your Google Sheet URL in the sidebar to begin.")
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Enter your Google Sheet URL** in the sidebar
        2. **Ensure the sheet is shared** with the service account
        3. **Data loads automatically** and refreshes every 5 minutes
        
        ---
        
        **Need help?** Contact Romina Labanca, Coach Community Associate
        """)
        st.stop()
    
    # Load data
    with st.spinner("Loading intelligence from Google Sheets..."):
        processor = load_data_from_sheets(sheet_url)
    
    if processor is None:
        st.error("❌ Failed to load data. Please check your Google Sheet URL and permissions.")
        st.info("""
        **Troubleshooting:**
        - Verify the sheet is shared with the service account
        - Check that the URL is correct
        - Ensure the sheet contains data
        """)
        st.stop()
    
    # Initialize visualizer and exporter
    visualizer = DebriefVisualizer()
    exporter = ReportExporter()
    
    # Render selected view
    if view == "📊 Overview":
        render_overview(processor, visualizer)
    elif view == "🔍 Partner Deep Dive":
        render_partner_deep_dive(processor, visualizer, exporter)
    elif view == "🔄 Partner Comparison":
        render_comparison(processor, visualizer, exporter)
    elif view == "💡 Strategic Insights":
        render_strategic_insights(processor)

if __name__ == "__main__":
    main()

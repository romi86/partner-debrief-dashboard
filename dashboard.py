"""
Partner Debrief Intelligence Dashboard
BetterUp Executive Suite - Coach Intelligence Platform

A comprehensive dashboard for analyzing coach feedback and partner insights
from Partner Debrief sessions.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Import custom modules
from data_processor import DebriefDataProcessor
from visualizer import DebriefVisualizer
from report_exporter import ReportExporter

# Password protection
def check_password():
    """Returns True if the user has the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "CC0TeamTacoTruck_2@25!":  # ⚠️ CHANGE THIS PASSWORD!
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.write("*Contact Romina Labanca (romina.labanca@betterup.co) for access*")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# Stop here if password is incorrect
if not check_password():
    st.stop()
    
# Page configuration
st.set_page_config(
    page_title="BetterUp Partner Debrief Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for BetterUp branding
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4A90E2;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .metric-card {
        background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .insight-box {
        background-color: #F8F9FA;
        padding: 1rem;
        border-left: 4px solid #4A90E2;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(file_path):
    """Load and cache the survey data."""
    processor = DebriefDataProcessor(file_path)
    processor.load_data()
    return processor


def render_header():
    """Render the dashboard header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="main-header">🎯 Partner Debrief Intelligence Dashboard</div>', 
                   unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Strategic Coach Intelligence • Organizational Insights • Executive Themes</div>', 
                   unsafe_allow_html=True)
        st.caption("Created by Romina Labanca, Coach Community Associate | BetterUp")
    
    with col2:
        st.image("https://www.betterup.com/hubfs/BetterUp_PrimaryLogo_Teal_RGB-1.png", 
                width=150)


def render_overview_metrics(processor: DebriefDataProcessor):
    """Render key overview metrics."""
    st.markdown("### 📈 Strategic Intelligence Overview")
    
    # Get overall metrics
    metrics = processor.get_partner_metrics()
    themes = processor.get_theme_analysis()
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Debrief Sessions",
            value=metrics['unique_sessions'],
            delta=None,
            help="Total number of unique partner debrief sessions held"
        )
    
    with col2:
        st.metric(
            label="Coach Intelligence Inputs",
            value=metrics['total_responses'],
            delta=None,
            help="Total coach contributions across all sessions"
        )
    
    with col3:
        pressure_count = len(themes.get('organizational_pressures', []))
        st.metric(
            label="Unique Pressures Identified",
            value=pressure_count,
            delta=None,
            help="Distinct organizational pressures mentioned by coaches"
        )
    
    with col4:
        challenge_count = len(themes.get('leadership_challenges', []))
        st.metric(
            label="Leadership Themes",
            value=challenge_count,
            delta=None,
            help="Distinct leadership challenges identified"
        )
    
    # Date range
    if metrics['date_range'][0] != 'N/A':
        st.caption(f"📅 Data Period: {metrics['date_range'][0]} to {metrics['date_range'][1]}")
    
    # Partners covered
    st.caption(f"🤝 Partners: {', '.join(processor.partners)}")


def render_partner_deep_dive(processor: DebriefDataProcessor, visualizer: DebriefVisualizer):
    """Render detailed partner analysis."""
    st.markdown("### 🔍 Partner Deep Dive")
    
    # Partner selection
    selected_partner = st.selectbox(
        "Select Partner Program",
        options=processor.partners,
        key="partner_select"
    )
    
    if selected_partner:
        # Get partner data
        metrics = processor.get_partner_metrics(selected_partner)
        themes = processor.get_theme_analysis(selected_partner)
        time_series = processor.get_time_series_data(selected_partner)
        
        # Partner metrics
        st.markdown(f"#### {selected_partner} - Intelligence Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sessions", metrics['unique_sessions'], help="Unique debrief sessions for this partner")
        with col2:
            st.metric("Coach Inputs", metrics['total_responses'], help="Total coach intelligence contributions")
        with col3:
            pressure_count = len(themes.get('organizational_pressures', []))
            st.metric("Pressures", pressure_count, help="Unique organizational pressures identified")
        with col4:
            challenge_count = len(themes.get('leadership_challenges', []))
            st.metric("Challenges", challenge_count, help="Unique leadership challenges identified")
        
        # Visualizations
        tab1, tab2, tab3 = st.tabs(["🎯 Organizational Pressures", "🚀 Leadership Challenges", "💬 All Insights"])
        
        with tab1:
            st.markdown("##### What Executives Are Facing Right Now")
            if 'organizational_pressures' in themes and themes['organizational_pressures']:
                fig = visualizer.create_theme_distribution(
                    themes['organizational_pressures'],
                    "Top Organizational Pressures"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show top 5 in text
                st.markdown("**Top 5 Pressures:**")
                for i, (theme, count) in enumerate(themes['organizational_pressures'][:5], 1):
                    st.write(f"{i}. **{theme}** — *mentioned {count} time(s)*")
            else:
                st.info("No organizational pressure data available for this partner.")
        
        with tab2:
            st.markdown("##### Recurring Leadership Development Needs")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'leadership_challenges' in themes and themes['leadership_challenges']:
                    fig = visualizer.create_theme_distribution(
                        themes['leadership_challenges'],
                        "Leadership Challenges"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No leadership challenge data available.")
            
            with col2:
                if 'implementation_obstacles' in themes and themes['implementation_obstacles']:
                    fig = visualizer.create_theme_distribution(
                        themes['implementation_obstacles'],
                        "Implementation Obstacles"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No implementation obstacle data available.")
        
        with tab3:
            insights = processor.get_qualitative_insights(selected_partner)
            
            if insights:
                for category, responses in insights.items():
                    if responses:
                        st.markdown(f"**{category}**")
                        
                        # Display in expandable sections
                        for i, response in enumerate(responses[:10], 1):
                            with st.expander(f"Response {i}"):
                                st.write(response)
                        
                        if len(responses) > 10:
                            st.caption(f"Showing 10 of {len(responses)} responses")
            else:
                st.info("No qualitative insights available for this partner.")
        
        # Export button
        st.markdown("---")
        if st.button(f"📥 Export {selected_partner} Report", key="export_partner"):
            with st.spinner("Generating comprehensive report..."):
                exporter = ReportExporter()
                report_data = processor.export_partner_report_data(selected_partner)
                
                output_path = f"/mnt/user-data/outputs/{selected_partner.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
                exporter.export_partner_report_excel(report_data, output_path)
                
                st.success(f"✅ Report generated successfully!")
                st.markdown(f"[View your report](computer://{output_path})")


def render_partner_comparison(processor: DebriefDataProcessor, visualizer: DebriefVisualizer):
    """Render cross-partner comparison."""
    st.markdown("### 🏆 Cross-Partner Strategic Intelligence")
    
    st.markdown("""
    Compare the strategic themes and patterns emerging across your partner portfolio. 
    Identify which pressures and challenges are universal vs. partner-specific.
    """)
    
    # Select metrics for comparison
    available_metrics = ['avg_relevance', 'avg_support', 'avg_urgency', 'unique_sessions', 'total_responses']
    
    selected_metrics = st.multiselect(
        "Select metrics to compare",
        options=available_metrics,
        default=['avg_relevance', 'avg_support', 'unique_sessions'],
        format_func=lambda x: x.replace('avg_', '').replace('_', ' ').title()
    )
    
    if selected_metrics:
        # Get comparison data
        comparison_df = processor.compare_partners(selected_metrics)
        
        # Visualization tabs
        tab1, tab2, tab3 = st.tabs(["📊 Bar Charts", "🔥 Heatmap", "📋 Data Table"])
        
        with tab1:
            # Session volume
            if 'unique_sessions' in selected_metrics:
                fig = visualizer.create_session_volume_chart(comparison_df)
                st.plotly_chart(fig, use_container_width=True)
            
            # Partner comparison
            fig = visualizer.create_partner_comparison(comparison_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = visualizer.create_heatmap_comparison(comparison_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Format the dataframe for display
            display_df = comparison_df.copy()
            
            # Round numeric columns
            for col in display_df.columns:
                if col != 'Partner' and pd.api.types.is_numeric_dtype(display_df[col]):
                    display_df[col] = display_df[col].round(2)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        
        # Export comparison report
        st.markdown("---")
        if st.button("📥 Export Comparison Report", key="export_comparison"):
            with st.spinner("Generating comparison report..."):
                exporter = ReportExporter()
                
                # Get themes for all partners
                all_themes = {}
                for partner in processor.partners:
                    all_themes[partner] = processor.get_theme_analysis(partner)
                
                output_path = f"/mnt/user-data/outputs/Partner_Comparison_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
                exporter.export_comparison_report_excel(comparison_df, all_themes, output_path)
                
                st.success("✅ Comparison report generated successfully!")
                st.markdown(f"[View your report](computer://{output_path})")


def render_insights_summary(processor: DebriefDataProcessor):
    """Render AI-generated insights summary."""
    st.markdown("### 🧠 Strategic Insights")
    
    # Overall themes across all partners
    all_themes = processor.get_theme_analysis()
    
    if all_themes:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Top Organizational Pressures")
            if 'organizational_pressures' in all_themes and all_themes['organizational_pressures']:
                for i, (theme, count) in enumerate(all_themes['organizational_pressures'][:5], 1):
                    st.markdown(f"{i}. **{theme}** ({count} mentions)")
            else:
                st.info("No data available")
        
        with col2:
            st.markdown("#### 🚀 Key Leadership Challenges")
            if 'leadership_challenges' in all_themes and all_themes['leadership_challenges']:
                for i, (theme, count) in enumerate(all_themes['leadership_challenges'][:5], 1):
                    st.markdown(f"{i}. **{theme}** ({count} mentions)")
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # Implementation obstacles
        st.markdown("#### ⚠️ Common Implementation Obstacles")
        if 'implementation_obstacles' in all_themes and all_themes['implementation_obstacles']:
            obstacles_df = pd.DataFrame(
                all_themes['implementation_obstacles'][:8],
                columns=['Obstacle', 'Frequency']
            )
            st.dataframe(obstacles_df, use_container_width=True, hide_index=True)
        else:
            st.info("No data available")


def main():
    """Main application function."""
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📂 Data Source")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Survey Data",
            type=['xlsx'],
            help="Upload the Excel file containing survey responses"
        )
        
        # Use default file if none uploaded
        file_path = "/home/claude/Debrief_Survey_Data.xlsx" if not uploaded_file else None
        
        if uploaded_file:
            # Save uploaded file
            file_path = f"/home/claude/uploaded_data.xlsx"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
        
        st.markdown("---")
        
        # Navigation
        st.markdown("## 🧭 Navigation")
        view_mode = st.radio(
            "Select View",
            options=[
                "📈 Overview",
                "🔍 Partner Deep Dive",
                "🏆 Partner Comparison",
                "🧠 Strategic Insights"
            ]
        )
        
        st.markdown("---")
        
        # Info
        st.markdown("## ℹ️ About")
        st.info(
            """
            **Partner Debrief Intelligence Dashboard**
            
            Transform coach insights into strategic intelligence for partner 
            conversations. This dashboard surfaces real-time organizational 
            pressures, leadership themes, and implementation barriers from 
            BetterUp's coach network.
            
            **Core Intelligence:**
            - Organizational pressures executives face
            - Leadership development themes
            - Implementation obstacles
            - Cross-partner pattern recognition
            """
        )
    
    # Main content
    if file_path and os.path.exists(file_path):
        try:
            # Load data
            processor = load_data(file_path)
            visualizer = DebriefVisualizer()
            
            # Render selected view
            if view_mode == "📈 Overview":
                render_overview_metrics(processor)
                st.markdown("---")
                render_insights_summary(processor)
            
            elif view_mode == "🔍 Partner Deep Dive":
                render_partner_deep_dive(processor, visualizer)
            
            elif view_mode == "🏆 Partner Comparison":
                render_partner_comparison(processor, visualizer)
            
            elif view_mode == "🧠 Strategic Insights":
                render_insights_summary(processor)
        
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.exception(e)
    else:
        st.warning("⚠️ Please upload survey data to begin analysis.")


if __name__ == "__main__":
    main()

# Partner Debrief Intelligence Dashboard

## Executive Summary

A sophisticated, CEO-ready analytics platform for BetterUp's Partner Debrief program. This dashboard transforms coach feedback into strategic intelligence, enabling data-driven decisions about partner programs and coaching effectiveness.

## 🎯 Purpose

The Partner Debrief Intelligence Dashboard serves as BetterUp's central intelligence hub for:

- **Strategic Partner Insights**: Real-time visibility into partner program health and coach satisfaction
- **Trend Analysis**: Identify emerging leadership themes and organizational pressures across partners
- **Benchmarking**: Compare partner performance across key satisfaction metrics
- **Executive Reporting**: Generate boardroom-ready reports with one click

## 🚀 Key Features

### 1. **Interactive Dashboard**
- Real-time metrics visualization
- Multi-partner comparison views
- Trend analysis over time
- Theme extraction and analysis

### 2. **Partner Deep Dive**
- Detailed partner-specific analytics
- Qualitative insights from coaches
- Time series trends
- Thematic analysis of organizational pressures and leadership challenges

### 3. **Cross-Partner Benchmarking**
- Performance heatmaps
- Comparative bar charts
- Session volume analysis
- Multi-metric comparison tools

### 4. **Executive Report Generation**
- One-click Excel reports
- Professional formatting with BetterUp branding
- Comprehensive data tables
- Exportable insights

## 📊 Data Structure

The dashboard expects Excel data with the following structure:

### Required Sheets:
1. **Form_Responses**: Main survey response data
2. **Survey Questions**: Question definitions and options

### Key Columns:
- `Timestamp`: Response submission time
- `Debrief Session Date`: Date of debrief session
- `Which partner program was this Debrief connected to?`: Partner name
- `What single organizational pressure is most frequently mentioned by your executives right now?`: Strategic insight
- `What leadership challenge or development need keeps coming up across multiple executive sessions?`: Coaching themes
- `What's the biggest obstacle preventing your executives from implementing what they learn in coaching?`: Implementation barriers

## 🏃 Getting Started

### Prerequisites
```bash
python 3.10+
pip install -r requirements.txt
```

### Installation

1. **Install Dependencies**
```bash
pip install pandas openpyxl plotly streamlit pillow reportlab --break-system-packages
```

2. **Prepare Your Data**
   - Export survey responses from Google Forms to Excel
   - Ensure the file follows the expected structure
   - Place file in the project directory or prepare to upload via UI

3. **Launch Dashboard**
```bash
cd /home/claude
streamlit run dashboard.py
```

4. **Access Dashboard**
   - Open browser to `http://localhost:8501`
   - Upload your survey data or use the default sample data
   - Navigate through views using the sidebar

## 📖 User Guide

### Navigation

#### 📈 Overview
- High-level KPIs across all partners
- Total sessions, responses, and satisfaction scores
- Top organizational pressures and leadership challenges
- Date range of available data

#### 🔍 Partner Deep Dive
1. Select a partner from the dropdown
2. View partner-specific metrics
3. Explore three analysis tabs:
   - **Trends**: Time series of satisfaction scores
   - **Themes**: Top organizational pressures, leadership challenges, and obstacles
   - **Insights**: Qualitative feedback from coaches
4. Export comprehensive partner report

#### 🏆 Partner Comparison
1. Select metrics to compare
2. View visualizations:
   - **Bar Charts**: Side-by-side metric comparison
   - **Heatmap**: Performance matrix across all metrics
   - **Data Table**: Detailed numeric comparison
3. Export cross-partner comparison report

#### 🧠 Strategic Insights
- Aggregated themes across all partners
- Top organizational pressures
- Key leadership challenges
- Common implementation obstacles

### Exporting Reports

#### Partner-Specific Report
1. Navigate to Partner Deep Dive
2. Select target partner
3. Click "Export [Partner] Report"
4. Report includes:
   - Executive summary
   - Detailed metrics
   - Theme analysis
   - Qualitative insights
   - Complete session details

#### Comparison Report
1. Navigate to Partner Comparison
2. Select metrics to include
3. Click "Export Comparison Report"
4. Report includes:
   - Cross-partner metrics table
   - Individual partner theme analyses
   - Performance benchmarks

## 🎨 Technical Architecture

### Modules

1. **data_processor.py**
   - Data loading and validation
   - Metric calculation
   - Theme extraction
   - Time series preparation
   - Export data preparation

2. **visualizer.py**
   - Plotly chart generation
   - BetterUp brand styling
   - Interactive visualizations
   - Color-coded rating systems

3. **report_exporter.py**
   - Excel report generation
   - Professional formatting
   - Multi-sheet workbooks
   - Data aggregation

4. **dashboard.py**
   - Streamlit UI
   - Navigation logic
   - State management
   - User interactions

### Key Design Principles

- **CEO-Ready**: Every visualization and report is boardroom-ready
- **BetterUp Branding**: Consistent color scheme and professional styling
- **Performance**: Cached data loading for fast interactions
- **Modularity**: Separation of concerns for maintainability
- **Scalability**: Handles growing data volumes efficiently

## 📊 Strategic Intelligence Framework

### Quantitative Metrics

- **Session Count**: Number of unique debrief sessions held
- **Coach Intelligence Inputs**: Total number of coach contributions
- **Theme Frequency**: Count of mentions for each organizational pressure or challenge
- **Partner Coverage**: Number of partners participating in debriefs
- **Trend Velocity**: Rate of change in theme emergence

### Qualitative Insights (Core Focus)

- **Organizational Pressures**: Current challenges executives are navigating
  - Examples: Change management, strategic clarity, talent retention
  - Use: Anticipate partner needs and market trends
  
- **Leadership Challenges**: Recurring development needs across coaching sessions
  - Examples: Executive presence, leading through change, team performance
  - Use: Design targeted coaching programs and content
  
- **Implementation Obstacles**: Systemic barriers preventing application of learnings
  - Examples: Time constraints, culture norms, lack of support
  - Use: Address root causes in partnership conversations and program design

### Strategic Value

These insights enable BetterUp to:
1. **Anticipate Needs**: Identify emerging themes before partners articulate them
2. **Demonstrate Value**: Show understanding of partner ecosystem through coach intelligence
3. **Design Solutions**: Create targeted interventions based on real-time feedback
4. **Position Strategically**: Act as trusted advisor rather than service provider

## 🎯 Best Practices

### For Data Accuracy
1. Ensure consistent partner naming in survey responses
2. Complete all required fields in surveys
3. Submit surveys within 24 hours of sessions
4. Use standardized date formats

### For Actionable Insights
1. Review dashboard monthly to identify trends
2. Compare partners quarterly for benchmarking
3. Export reports before executive briefings
4. Share qualitative insights with relevant stakeholders

### For Report Generation
1. Select appropriate date ranges
2. Include context in report titles
3. Validate data before exporting
4. Combine quantitative and qualitative insights

## 🔧 Troubleshooting

### Common Issues

**Dashboard won't load data**
- Verify Excel file format matches expected structure
- Check that all required columns are present
- Ensure date columns are properly formatted

**Visualizations are empty**
- Confirm data exists for the selected partner
- Check that rating columns contain numeric values
- Verify date range includes available data

**Export fails**
- Ensure output directory exists
- Check write permissions
- Verify sufficient disk space

### Support

For technical issues or feature requests:
1. Check data format requirements
2. Review error messages in console
3. Verify all dependencies are installed
4. Contact BetterUp technical team

## 🚀 Future Enhancements

### Planned Features
- **AI-Powered Insights**: Automated trend detection and recommendations
- **Sentiment Analysis**: NLP analysis of qualitative feedback
- **Predictive Analytics**: Forecast future coaching needs
- **Integration**: Direct connection to survey platform
- **Mobile Optimization**: Responsive design for tablets/phones
- **Role-Based Access**: Different views for different stakeholders

### Enhancement Requests
Submit enhancement requests to the BetterUp product team with:
- Use case description
- Expected benefit
- Priority level
- Supporting data/examples

## 📝 Version History

### v1.0.0 (Current)
- Initial release
- Core dashboard functionality
- Partner comparison views
- Excel export capabilities
- BetterUp branding

## 📄 License

Proprietary - BetterUp, Inc. All rights reserved.

## 👥 Credits

**Developed for**: BetterUp Executive Suite Team
**Purpose**: Partner Debrief Intelligence & Coach Insights
**Platform**: Python, Streamlit, Plotly

---

*This dashboard transforms coach intelligence into strategic insights, positioning BetterUp as a trusted advisor that anticipates organizational needs and demonstrates measurable value through human-centered data.*

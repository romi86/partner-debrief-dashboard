# QUICK REFERENCE GUIDE
# Partner Debrief Intelligence Dashboard

## 🚀 QUICK START (30 Seconds)

```bash
cd /mnt/user-data/outputs
streamlit run dashboard.py
```

Browser opens at: http://localhost:8501

---

## 📊 DASHBOARD VIEWS

### 1. OVERVIEW (Default View)
**Shows**: Cross-partner intelligence, emerging themes, strategic patterns
**Use When**: Need executive summary or identifying trends across portfolio
**Key Intelligence**:
- Total Debrief Sessions Held
- Total Coach Intelligence Inputs
- Top Organizational Pressures (across all partners)
- Recurring Leadership Challenges
- Common Implementation Obstacles

### 2. PARTNER DEEP DIVE
**Shows**: Detailed analysis for one partner
**Use When**: Preparing for partner meetings or reviewing specific program
**Features**:
- Select partner from dropdown
- View 3 tabs: Trends | Themes | Insights
- Export comprehensive partner report

**Export Path**: Saves to `/mnt/user-data/outputs/[Partner]_Report_[Date].xlsx`

### 3. PARTNER COMPARISON
**Shows**: Side-by-side benchmarking
**Use When**: Quarterly reviews or portfolio analysis
**Features**:
- Select metrics to compare
- View as: Bar Charts | Heatmap | Data Table
- Export comparison report

**Export Path**: Saves to `/mnt/user-data/outputs/Partner_Comparison_Report_[Date].xlsx`

### 4. STRATEGIC INSIGHTS
**Shows**: Aggregated themes across all partners
**Use When**: Identifying enterprise-wide trends
**Displays**:
- Top Organizational Pressures
- Key Leadership Challenges
- Common Implementation Obstacles

---

## 📥 EXPORTING REPORTS

### Partner Report
1. Navigate to "Partner Deep Dive"
2. Select partner
3. Click "Export [Partner] Report"
4. Click the download link

**Contains**:
- Executive Summary
- Detailed Metrics
- Theme Analysis
- Qualitative Insights
- Session Details

### Comparison Report
1. Navigate to "Partner Comparison"
2. Select metrics
3. Click "Export Comparison Report"
4. Click the download link

**Contains**:
- Cross-partner metrics table
- Individual partner themes
- Performance benchmarks

---

## 🎯 INTERPRETING STRATEGIC INTELLIGENCE

### Organizational Pressures
What executives are facing right now:
- **Change Management & Organizational Agility**: Restructuring, transformation
- **Strategic Clarity & Direction**: Vision, long-term planning
- **Talent Acquisition & Retention**: Hiring, retention challenges
- **Cross-functional Alignment & Collaboration**: Silos, coordination
- **Resource Constraints & Budget Pressures**: Doing more with less

**Action**: Identify patterns across partners to anticipate market trends

### Leadership Challenges
What leaders need to develop:
- **Executive Presence & Influence**: Building credibility, impact
- **Leading Through Change & Uncertainty**: Navigating ambiguity
- **Strategic Thinking & Vision**: Future-focused leadership
- **Team Performance & Motivation**: Engaging and developing teams
- **Stakeholder Management & Communication**: Managing up/across

**Action**: Design coaching programs around recurring themes

### Implementation Obstacles
What prevents application of learning:
- **Insufficient Time / Competing Priorities**: Bandwidth constraints
- **Organizational Culture / Norms**: Cultural resistance
- **Lack of Leadership Support**: Top-down alignment issues
- **Unclear Accountability / Ownership**: Role confusion
- **Resistance to Change**: Team or organizational inertia

**Action**: Address systemic barriers in partnership discussions

---

## 🔧 COMMON TASKS

### Upload New Data
1. Click "Browse files" in sidebar
2. Select Excel file
3. Data auto-loads

### Change Date Range
*Currently shows all available data*
*Filter by selecting specific partner to see their date range*

### Compare Specific Partners
1. Go to Partner Comparison
2. All partners shown by default
3. Use heatmap for quick visual comparison

### Find Specific Theme
1. Go to Partner Deep Dive
2. Select partner
3. Click "Themes" tab
4. Review bar charts

### Get Qualitative Feedback
1. Go to Partner Deep Dive
2. Select partner
3. Click "Insights" tab
4. Expand responses to read

---

## ⚠️ TROUBLESHOOTING

### Dashboard won't load
```bash
# Verify installation
bash quickstart.sh

# Run system test
python test_system.py
```

### No data showing
- Check Excel file format matches template
- Verify partner names in data
- Confirm date columns are formatted as dates

### Export not working
- Ensure `/mnt/user-data/outputs/` directory exists
- Check write permissions
- Verify sufficient disk space

### Charts are empty
- Confirm data exists for selected partner
- Check that rating columns contain numbers (1-5)
- Verify date range includes data

---

## 📋 DATA REQUIREMENTS CHECKLIST

Required columns in Excel:
- ✅ Debrief Session Date
- ✅ Which partner program was this Debrief connected to?
- ✅ What single organizational pressure is most frequently mentioned...?
- ✅ What leadership challenge or development need keeps coming up...?
- ✅ What's the biggest obstacle preventing your executives from implementing...?

Optional but valuable:
- ✅ Timestamp
- ✅ Coach ID / BetterUp Email
- ✅ Additional qualitative feedback columns

---

## 🎨 COLOR CODE MEANINGS

### Charts & Gauges
- **Green**: Excellent performance (4.5-5.0)
- **Blue**: Good performance (3.5-4.5)
- **Orange**: Average/Needs attention (2.5-3.5)
- **Red**: Poor performance (<2.5)

### Dashboard
- **Blue (#4A90E2)**: BetterUp primary
- **Green (#50C878)**: Positive metrics
- **Purple (#7B68EE)**: Secondary highlights
- **Orange (#FFA500)**: Warnings/urgency

---

## ⌨️ KEYBOARD SHORTCUTS

**Streamlit Default**:
- `R`: Rerun dashboard
- `C`: Clear cache
- `?`: Show keyboard shortcuts

**Browser**:
- `Ctrl/Cmd + F`: Find on page
- `Ctrl/Cmd + P`: Print view
- `Ctrl/Cmd + S`: Save page

---

## 📞 SUPPORT RESOURCES

1. **Detailed Documentation**: `README.md`
2. **System Test**: `python test_system.py`
3. **Quick Verification**: `bash quickstart.sh`
4. **Sample Data**: `Debrief_Survey_Data.xlsx`

---

## 💡 BEST PRACTICES

### Daily Use
- Check Overview for new responses
- Monitor relevance/support trends
- Review urgent items (urgency score 4-5)

### Weekly Use
- Deep dive into 1-2 partners
- Review qualitative insights
- Export reports for meetings

### Monthly Use
- Run full partner comparison
- Analyze trends over time
- Export comparison report
- Share insights with leadership

### Quarterly Use
- Complete partner portfolio review
- Identify emerging themes
- Benchmark against targets
- Plan strategic interventions

---

## 🎯 QUICK WINS

### Before Partner Meeting
1. Export partner report (2 min)
2. Review top 3 themes (3 min)
3. Note avg scores vs target (1 min)
**Total**: 6 minutes prepared

### Before Executive Briefing
1. Open Overview (1 min)
2. Export comparison report (2 min)
3. Review strategic insights (3 min)
**Total**: 6 minutes prepared

### Monthly Review
1. Compare all partners (5 min)
2. Identify trend changes (5 min)
3. Export reports (2 min)
4. Draft insights (10 min)
**Total**: 22 minutes complete

---

## 📈 SUCCESS METRICS

**Track these monthly**:
- Average relevance score trend
- Average support score trend
- Number of sessions held
- Response rate
- Theme consistency/changes

**Quarterly goals**:
- Relevance score: 4.0+
- Support score: 4.0+
- 100% session response rate
- Decreasing urgency scores (indicates proactive support)

---

*Keep this guide handy for quick reference*
*Partner Debrief Intelligence Dashboard*
*BetterUp Executive Suite*

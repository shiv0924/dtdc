import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="DTDC | Festive Surge Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚚"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ── ROOT TOKENS ── */
:root {
  --navy:       #0B1A35;
  --navy-mid:   #112249;
  --navy-light: #1A3168;
  --red:        #E8003D;
  --red-dim:    #9E0029;
  --white:      #F5F7FA;
  --muted:      #8A9BBE;
  --border:     rgba(255,255,255,0.07);
  --card-bg:    rgba(17,34,73,0.85);
  --glass:      rgba(255,255,255,0.04);
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: var(--navy);
  color: var(--white);
}

.stApp {
  background: var(--navy);
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(232,0,61,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(26,49,104,0.5) 0%, transparent 70%);
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: var(--navy-mid) !important;
  border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
  padding-top: 0 !important;
}

/* ── SIDEBAR LOGO HEADER ── */
.sidebar-logo-block {
  background: linear-gradient(135deg, #0B1A35 0%, #1A3168 100%);
  padding: 28px 20px 22px;
  margin-bottom: 24px;
  border-bottom: 2px solid var(--red);
  text-align: center;
}

.sidebar-logo-block img {
  max-width: 130px;
  filter: brightness(0) invert(1);
}

.sidebar-tagline {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 10px;
}

/* ── SIDEBAR NAV ── */
.stRadio [role="radiogroup"] {
  gap: 4px;
}

.stRadio label {
  font-family: 'Poppins', sans-serif !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  letter-spacing: 0.8px !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
  padding: 10px 16px !important;
  border-radius: 6px !important;
  border: 1px solid transparent !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
}

.stRadio label:hover {
  background: var(--glass) !important;
  color: var(--white) !important;
  border-color: var(--border) !important;
}

/* ── PAGE HEADER ── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32px 0 28px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 36px;
}

.page-header-left {}

.page-label {
  font-family: 'Poppins', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--red);
  margin-bottom: 6px;
}

.page-title {
  font-family: 'Poppins', sans-serif;
  font-size: 36px;
  font-weight: 800;
  color: var(--white);
  line-height: 1.1;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--muted);
  margin-top: 6px;
}

/* ── KPI CARDS ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 28px 0;
}

.kpi-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--red), transparent);
}

.kpi-card:hover {
  transform: translateY(-2px);
  border-color: rgba(232,0,61,0.3);
}

.kpi-card .kpi-label {
  font-family: 'Poppins', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 10px;
}

.kpi-card .kpi-value {
  font-family: 'Poppins', sans-serif;
  font-size: 34px;
  font-weight: 800;
  color: var(--white);
  line-height: 1;
}

.kpi-card .kpi-delta {
  font-size: 11px;
  color: var(--red);
  margin-top: 6px;
  font-weight: 500;
}

.kpi-card .kpi-delta.positive { color: #10B981; }

/* ── ALERT BOX ── */
.alert-box {
  background: linear-gradient(135deg, rgba(232,0,61,0.08) 0%, rgba(232,0,61,0.03) 100%);
  border: 1px solid rgba(232,0,61,0.25);
  border-left: 3px solid var(--red);
  border-radius: 10px;
  padding: 18px 22px;
  margin: 20px 0;
  font-size: 14px;
  line-height: 1.7;
  color: #CBD5E9;
}

.alert-box strong { color: var(--white); }

.info-box {
  background: rgba(26,49,104,0.4);
  border: 1px solid var(--border);
  border-left: 3px solid #3B82F6;
  border-radius: 10px;
  padding: 18px 22px;
  margin: 20px 0;
  font-size: 14px;
  line-height: 1.7;
  color: #CBD5E9;
}

.info-box strong { color: var(--white); }

/* ── SECTION HEADING ── */
.section-heading {
  font-family: 'Poppins', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--white);
  margin: 32px 0 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-heading .dot {
  width: 6px; height: 6px;
  background: var(--red);
  border-radius: 50%;
  display: inline-block;
}

/* ── CHART CONTAINERS ── */
.chart-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 6px;
  backdrop-filter: blur(12px);
  margin-bottom: 20px;
}

/* ── RECOMMENDATIONS ── */
.rec-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  height: 100%;
}

.rec-card h4 {
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 18px;
}

.rec-card h4.quick { color: #F59E0B; }
.rec-card h4.strategic { color: #3B82F6; }

.rec-item {
  display: flex;
  gap: 12px;
  margin-bottom: 14px;
  font-size: 13.5px;
  line-height: 1.6;
  color: #CBD5E9;
}

.rec-item .rec-num {
  font-family: 'Poppins', sans-serif;
  font-size: 11px;
  font-weight: 800;
  color: var(--red);
  min-width: 20px;
  margin-top: 2px;
}

.rec-item strong { color: var(--white); }

/* ── KPI TAG ── */
.kpi-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 24px;
}

.kpi-tag {
  background: rgba(26,49,104,0.6);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px 14px;
  font-family: 'Poppins', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.8px;
  color: var(--muted);
}

/* ── CAUSE CARD ── */
.cause-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 14px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.cause-num {
  font-family: 'Poppins', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: rgba(232,0,61,0.2);
  line-height: 1;
  min-width: 32px;
}

.cause-body strong {
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--white);
}

.cause-body p {
  font-size: 13px;
  color: var(--muted);
  margin-top: 4px;
  line-height: 1.6;
}

/* ── DIVIDER ── */
.divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 32px 0;
}

/* ── STREAMLIT OVERRIDES ── */
.stMetric {
  background: var(--card-bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 16px !important;
}

div[data-testid="metric-container"] {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
}

div[data-testid="stExpander"] {
  background: var(--card-bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

div[data-testid="stExpander"] summary {
  color: var(--muted) !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 12px !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
}

.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--navy-light); border-radius: 3px; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#8A9BBE', size=12),
    title_font=dict(family='Syne', color='#F5F7FA', size=15, weight='bold' if False else None),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.07)', tickfont=dict(size=11)),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.07)', tickfont=dict(size=11)),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8A9BBE', size=11)),
    margin=dict(l=10, r=10, t=45, b=10),
    colorway=['#E8003D','#3B82F6','#10B981','#F59E0B','#8B5CF6','#06B6D4'],
)

def styled_fig(fig, title=None):
    update = dict(**PLOTLY_LAYOUT)
    if title:
        update['title'] = dict(text=title, font=dict(family='Syne', color='#F5F7FA', size=14), x=0.01)
    fig.update_layout(**update)
    return fig

# ---------------------------------------------------------
# 2. DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    orders = pd.read_csv("orders.csv")
    customers = pd.read_csv("customers.csv")
    nps = pd.read_csv("nps.csv")
    complaints = pd.read_csv("complaints.csv")
    hub = pd.read_csv("hub_performance.csv")
    courier = pd.read_csv("courier_performance.csv")

    for col in ['order_date', 'promised_date', 'delivery_date']:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
    nps['response_date'] = pd.to_datetime(nps['response_date'], errors='coerce')
    customers['signup_date'] = pd.to_datetime(customers['signup_date'], errors='coerce')

    orders['delivery_delay'] = (orders['delivery_date'] - orders['promised_date']).dt.days
    orders['sla_breach_flag'] = orders['delivery_delay'].apply(lambda x: 'Yes' if x > 0 else 'No')
    orders['order_month'] = orders['order_date'].dt.to_period('M').astype(str)

    def categorize_nps(score):
        if score <= 6: return 'Detractor'
        elif score <= 8: return 'Passive'
        else: return 'Promoter'
    nps['category'] = nps['score'].apply(categorize_nps)
    nps['response_month'] = nps['response_date'].dt.to_period('M').astype(str)

    return orders, customers, nps, complaints, hub, courier

orders, customers, nps, complaints, hub, courier = load_data()
master_df = orders.merge(customers[['customer_id', 'segment']], on='customer_id', how='left')

# ---------------------------------------------------------
# 3. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-block">
        <img src="data:image/png;base64,{logo_b64}" alt="DTDC Logo"/>
        <div class="sidebar-tagline">Intelligence Dashboard</div>
    </div>
    """.replace("{logo_b64}", __import__('base64').b64encode(open('DTDC_logo.png','rb').read()).decode()), unsafe_allow_html=True)

    st.markdown("<div style='padding: 0 12px; margin-bottom: 8px;'><span style='font-family:Syne; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#8A9BBE;'>SECTIONS</span></div>", unsafe_allow_html=True)

    sections = ["1. Executive Summary", "2. CX & NPS Deep Dive", "3. Operational Diagnostics", "4. End-to-End Funnel", "5. Retention & Recommendations"]
    selection = st.radio("", sections, label_visibility="collapsed")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.07); margin: 28px 12px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding: 0 12px;'>
        <div style='font-family:Syne; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#8A9BBE; margin-bottom:10px;'>REPORT PERIOD</div>
        <div style='font-family:Syne; font-size:15px; font-weight:700; color:#F5F7FA;'>Oct – Dec 2025</div>
        <div style='font-size:12px; color:#8A9BBE; margin-top:4px;'>Festive Surge Season</div>
        <div style='margin-top:14px; font-family:Syne; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#8A9BBE;'>PREPARED BY</div>
        <div style='font-size:12px; color:#CBD5E9; margin-top:4px;'>Shivam (shivam24x09@gmail.com)</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SHARED KPI CALCULATIONS
# ---------------------------------------------------------
nps_counts = nps['category'].value_counts(normalize=True)
overall_nps = (nps_counts.get('Promoter', 0) - nps_counts.get('Detractor', 0)) * 100
sla_breach_pct = (orders['sla_breach_flag'] == 'Yes').mean() * 100
complaint_rate = (len(complaints) / len(orders)) * 100

# ---------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY
# ---------------------------------------------------------
if selection == "1. Executive Summary":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-label">Festive Surge Diagnostic · 2025</div>
            <div class="page-title">Delivery Experience<br>Intelligence Report</div>
            <div class="page-subtitle">Root-cause analysis of CX decline during Oct–Dec peak season</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-box">
        <strong>Critical Finding:</strong> Operational scaling failed in Tier-2 cities, primarily driven by a single logistics partner (QuickShip). This triggered a cascade of SLA breaches → "Fake Delivery Attempt" complaints → NPS collapse → severe Repeat Purchase Rate decline.
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Overall NPS · Oct–Dec</div>
            <div class="kpi-value">{overall_nps:.1f}</div>
            <div class="kpi-delta">↓ Critical threshold</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">SLA Breach Rate</div>
            <div class="kpi-value">{sla_breach_pct:.1f}%</div>
            <div class="kpi-delta">↑ Urgent intervention required</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Complaint Rate</div>
            <div class="kpi-value">{complaint_rate:.1f}%</div>
            <div class="kpi-delta">↑ Elevated vs baseline</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{len(orders):,}</div>
            <div class="kpi-delta positive">Peak season volume</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="dot"></span>Identified Root Causes</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="cause-card">
        <div class="cause-num">01</div>
        <div class="cause-body">
            <strong>Courier Vendor Failure in Tier-2 Cities</strong>
            <p>'QuickShip' carries a disastrous 32% SLA breach rate and is overwhelmingly failing in Nagpur and Indore, where logistics capacity is insufficient for festive demand spikes.</p>
        </div>
    </div>
    <div class="cause-card">
        <div class="cause-num">02</div>
        <div class="cause-body">
            <strong>Systemic "Fake Delivery Attempt" Fraud</strong>
            <p>When couriers miss SLAs due to volume overload, they log false delivery attempts to artificially pause the SLA clock — directly converting customers into Detractors.</p>
        </div>
    </div>
    <div class="cause-card">
        <div class="cause-num">03</div>
        <div class="cause-body">
            <strong>High-Value Cohort Churn Risk</strong>
            <p>Poor delivery experiences are disproportionately hitting 'High Value' and 'New' festive cohorts — the exact customers with highest LTV potential, destroying acquisition ROI.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 2: CX & NPS DEEP DIVE
# ---------------------------------------------------------
elif selection == "2. CX & NPS Deep Dive":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-label">Customer Experience</div>
            <div class="page-title">NPS & CX Deep Dive</div>
            <div class="page-subtitle">Sentiment trends, segment breakdown, and detractor drivers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    # NPS Trend
    nps_trend = nps.groupby('response_month')['category'].value_counts(normalize=True).unstack().fillna(0)
    nps_trend['NPS_Score'] = (nps_trend.get('Promoter', 0) - nps_trend.get('Detractor', 0)) * 100

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=nps_trend.index, y=nps_trend['NPS_Score'],
        mode='lines+markers+text',
        text=[f"{v:.1f}" for v in nps_trend['NPS_Score']],
        textposition='top center',
        textfont=dict(family='Syne', color='#F5F7FA', size=11),
        line=dict(color='#E8003D', width=2.5),
        marker=dict(size=8, color='#E8003D', line=dict(color='#F5F7FA', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(232,0,61,0.06)'
    ))
    styled_fig(fig1, "NPS Trend — Month on Month")
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    # NPS by Segment
    nps_cust = nps.merge(customers[['customer_id', 'segment']], on='customer_id', how='left')
    seg_nps = nps_cust.groupby('segment')['category'].value_counts(normalize=True).unstack().fillna(0)
    seg_nps['NPS_Score'] = (seg_nps.get('Promoter', 0) - seg_nps.get('Detractor', 0)) * 100
    seg_data = seg_nps.reset_index()

    colors = ['#E8003D' if v < 0 else '#10B981' for v in seg_data['NPS_Score']]
    fig2 = go.Figure(go.Bar(
        x=seg_data['segment'], y=seg_data['NPS_Score'],
        marker_color=colors,
        text=[f"{v:.1f}" for v in seg_data['NPS_Score']],
        textposition='outside',
        textfont=dict(family='Syne', color='#F5F7FA', size=11),
    ))
    styled_fig(fig2, "NPS by Customer Segment")
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>Key Insight:</strong> NPS crashed significantly from October through December as peak season dragged on. Critically, our <strong>High Value</strong> and <strong>New</strong> segments experienced the lowest NPS — meaning we're burning the exact cohorts acquired at highest CAC during the festive season.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="dot"></span>Top Drivers of Detractors</div>', unsafe_allow_html=True)

    detractors = nps[nps['category'] == 'Detractor']
    detractor_complaints = detractors.merge(complaints, on='order_id', how='inner')
    complaint_counts = detractor_complaints['issue_type'].value_counts().reset_index()
    complaint_counts.columns = ['Issue Type', 'Volume']

    fig3 = go.Figure(go.Bar(
        x=complaint_counts['Volume'],
        y=complaint_counts['Issue Type'],
        orientation='h',
        marker=dict(
            color=complaint_counts['Volume'],
            colorscale=[[0, 'rgba(232,0,61,0.3)'], [1, '#E8003D']],
            showscale=False
        ),
        text=complaint_counts['Volume'],
        textposition='outside',
        textfont=dict(family='Syne', color='#F5F7FA', size=11),
    ))
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    styled_fig(fig3, "Top Complaint Types Among Detractors")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("View NPS Pivot Table"):
        st.dataframe(nps_trend[['NPS_Score']].style.background_gradient(cmap='RdYlGn'))

# ---------------------------------------------------------
# SECTION 3: OPERATIONAL DIAGNOSTICS
# ---------------------------------------------------------
elif selection == "3. Operational Diagnostics":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-label">Operations</div>
            <div class="page-title">Operational Diagnostics</div>
            <div class="page-subtitle">Hub performance, courier analysis, and root-cause isolation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    tier_mapping = {'Mumbai': 'Tier-1', 'Pune': 'Tier-1', 'Nagpur': 'Tier-2', 'Indore': 'Tier-2'}
    hub['Tier'] = hub['city'].map(tier_mapping)
    hub['Failed Attempt Rate'] = hub['failed_attempts'] / hub['total_orders']
    hub['RTO Rate'] = hub['rto_count'] / hub['total_orders']

    hub_melted = hub.melt(id_vars=['city','Tier'], value_vars=['Failed Attempt Rate','RTO Rate'], var_name='Metric', value_name='Rate')
    colors_map = {'Failed Attempt Rate': '#E8003D', 'RTO Rate': '#F59E0B'}

    fig4 = go.Figure()
    for metric, color in colors_map.items():
        sub = hub_melted[hub_melted['Metric'] == metric]
        fig4.add_trace(go.Bar(
            name=metric, x=sub['city'], y=sub['Rate'],
            marker_color=color, text=[f"{v:.1%}" for v in sub['Rate']],
            textposition='outside', textfont=dict(size=11, family='Syne', color='#F5F7FA')
        ))
    fig4.update_layout(barmode='group')
    styled_fig(fig4, "Hub Inefficiency — Tier 1 vs Tier 2")

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    fig5 = px.scatter(
        courier, x='sla_breach_rate', y='complaint_rate',
        size='avg_delivery_time', color='courier_partner',
        text='courier_partner',
        color_discrete_sequence=['#E8003D','#3B82F6','#10B981','#F59E0B']
    )
    fig5.update_traces(textposition='top center', textfont=dict(size=11, family='Syne', color='#F5F7FA'))
    styled_fig(fig5, "Courier Performance Matrix")

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig5, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-box">
        <strong>Diagnostic Conclusion:</strong> The data confirms the hypothesis. Tier-2 cities (Nagpur, Indore) have vastly higher Failed Attempt and RTO rates. Mapping to Courier Partners, <strong>QuickShip</strong> is the critical outlier — 32% SLA breach rate, causing systemic bottlenecks. High "Fake Delivery Attempts" are couriers artificially managing SLA clocks due to insufficient Tier-2 capacity.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View Raw Pivot Tables"):
        c1, c2 = st.columns(2)
        with c1:
            st.caption("COURIER DATA")
            st.dataframe(courier)
        with c2:
            st.caption("HUB DATA")
            st.dataframe(hub)

# ---------------------------------------------------------
# SECTION 4: END-TO-END FUNNEL
# ---------------------------------------------------------
elif selection == "4. End-to-End Funnel":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-label">Funnel Analysis</div>
            <div class="page-title">End-to-End Failure Funnel</div>
            <div class="page-subtitle">Tracing order volume from placement to detractor conversion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_orders = len(orders)
    delayed_orders = len(orders[orders['sla_breach_flag'] == 'Yes'])
    total_complaints = len(complaints)
    total_detractors = len(nps[nps['category'] == 'Detractor'])

    fig_funnel = go.Figure(go.Funnel(
        y=["Total Orders Placed", "Delayed Deliveries", "Resulted in Complaints", "Converted to Detractors"],
        x=[total_orders, delayed_orders, total_complaints, total_detractors],
        textinfo="value+percent initial",
        textfont=dict(family='Syne', color='#F5F7FA', size=13),
        marker=dict(color=["#1A3168", "#F59E0B", "#E8003D", "#7F0022"]),
        connector=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
    ))
    styled_fig(fig_funnel, "The Failure Funnel: Orders → Detractors")
    fig_funnel.update_layout(margin=dict(l=200, r=80, t=60, b=30))

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_funnel, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>Funnel Insight:</strong> A significant portion of delayed orders directly generate complaint tickets. The conversion rate from Complaint → Detractor is alarmingly high. Because logistics is the final, most tangible touchpoint of the e-commerce experience, every operational failure instantly destroys brand equity built through marketing and acquisition spend.
    </div>
    """, unsafe_allow_html=True)

    # Funnel Stats Row
    breach_to_complaint = (total_complaints / delayed_orders * 100) if delayed_orders else 0
    complaint_to_detractor = (total_detractors / total_complaints * 100) if total_complaints else 0
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Delayed Deliveries</div>
            <div class="kpi-value">{delayed_orders:,}</div>
            <div class="kpi-delta">{delayed_orders/total_orders*100:.1f}% of total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Complaint Conversion</div>
            <div class="kpi-value">{breach_to_complaint:.1f}%</div>
            <div class="kpi-delta">Delays → Complaints</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Detractor Conversion</div>
            <div class="kpi-value">{complaint_to_detractor:.1f}%</div>
            <div class="kpi-delta">Complaints → Detractors</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 5: RETENTION & RECOMMENDATIONS
# ---------------------------------------------------------
elif selection == "5. Retention & Recommendations":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-label">Strategy</div>
            <div class="page-title">Retention Analysis &<br>Action Plan</div>
            <div class="page-subtitle">Cohort retention impact and prioritised strategic recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="dot"></span>Repeat Order Cohort Analysis</div>', unsafe_allow_html=True)

    orders['order_month_p'] = pd.to_datetime(orders['order_date']).dt.to_period('M')
    customers['signup_month'] = pd.to_datetime(customers['signup_date']).dt.to_period('M')
    cohort_df = orders.merge(customers[['customer_id', 'signup_month']], on='customer_id')
    cohort_pivot = cohort_df.groupby(['signup_month', 'order_month_p'])['customer_id'].nunique().unstack(fill_value=0)

    st.dataframe(cohort_pivot.style.background_gradient(cmap='YlOrRd_r', axis=None), use_container_width=True)

    st.markdown("""
    <div class="info-box">
        <strong>Retention Insight:</strong> Users acquired in early festive months (Aug/Sep/Oct) show steep drop-off in repeat purchases through Nov/Dec. Poor delivery experience dramatically reduces return purchase likelihood. CAC is entirely wasted if operations cannot retain the user beyond the first order.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="dot"></span>Strategic Action Plan</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
        <div class="rec-card">
            <h4 class="quick">⚡ Quick Wins — Short Term</h4>
            <div class="rec-item">
                <span class="rec-num">01</span>
                <div><strong>Throttle QuickShip Volume:</strong> Immediately redistribute Tier-2 allocation (Nagpur/Indore) to FastEx and audit capacity thresholds.</div>
            </div>
            <div class="rec-item">
                <span class="rec-num">02</span>
                <div><strong>Proactive CRM Intervention:</strong> Automate WhatsApp/SMS apology + retention discount when any order hits SLA breach threshold, before a ticket is raised.</div>
            </div>
            <div class="rec-item">
                <span class="rec-num">03</span>
                <div><strong>GPS-Fence Delivery Executives:</strong> Implement geofencing to prevent logging 'Failed Attempt' when miles from customer — cut fake attempts at source.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="rec-card">
            <h4 class="strategic">🏗 Strategic Improvements — Long Term</h4>
            <div class="rec-item">
                <span class="rec-num">01</span>
                <div><strong>Tier-2 Hub Restructuring:</strong> The Tier-1/2 disparity is untenable. Re-evaluate hub capacity and commission dedicated peak-season last-mile contractors in Nagpur/Indore.</div>
            </div>
            <div class="rec-item">
                <span class="rec-num">02</span>
                <div><strong>Dynamic SLA Promises:</strong> During festive peaks, dynamically adjust 'Promised Dates' on the frontend using real-time capacity data to manage expectations accurately.</div>
            </div>
            <div class="rec-item">
                <span class="rec-num">03</span>
                <div><strong>Vendor Penalty Framework:</strong> Introduce financial penalties for courier partners maintaining complaint rates above 15%, with quarterly SLA-breach scorecards.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top: 8px;'>
        <div style='font-family:Syne; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:#8A9BBE; margin-bottom:12px;'>SUGGESTED KPIS TO TRACK GOING FORWARD</div>
        <div class="kpi-tags">
            <span class="kpi-tag">First-Attempt Delivery Rate (FADR)</span>
            <span class="kpi-tag">True RTO % (excl. fake attempts)</span>
            <span class="kpi-tag">NPS by Delivery Partner</span>
            <span class="kpi-tag">Cost Per Successful Delivery (CPSD)</span>
            <span class="kpi-tag">Detractor Recovery Rate</span>
            <span class="kpi-tag">Cohort 90-Day Repeat Rate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

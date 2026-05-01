# ═══════════════════════════════════════════════════════════════════════════
# LogiTrack PRO — Supply Chain Dashboard
# Python | Streamlit | Plotly | SQLite (12 SQL Queries)
# ═══════════════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sqlite3

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogiTrack PRO",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #070b18 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }
.block-container { padding: 1.2rem 1.6rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid #1a2540 !important;
    width: 195px !important; min-width: 195px !important;
}
section[data-testid="stSidebar"] > div:first-child { width: 195px !important; }

/* ── Logo ── */
.logo-wrap {
    display: flex; flex-direction: column; align-items: center;
    padding: 20px 10px 14px;
}
.logo-icon {
    width: 60px; height: 60px; border-radius: 14px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; margin-bottom: 8px;
    box-shadow: 0 0 22px rgba(99,102,241,0.6), 0 0 44px rgba(37,99,235,0.25);
}
.logo-name { font-size: 1.1rem; font-weight: 700; color: #fff; }
.logo-badge { font-size: 0.55rem; font-weight: 700; color: #a78bfa; letter-spacing: 3px; text-transform: uppercase; }

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important; text-align: left !important;
    padding: 8px 12px !important; border-radius: 9px !important;
    border: none !important; font-size: 0.82rem !important;
    font-weight: 500 !important; color: #94a3b8 !important;
    background: transparent !important; margin-bottom: 2px !important;
    transition: all 0.2s !important; box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,102,241,0.12) !important; color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .nav-active .stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: #fff !important; font-weight: 600 !important;
    box-shadow: 0 0 14px rgba(99,102,241,0.55), 0 4px 10px rgba(37,99,235,0.3) !important;
}

/* ── Main area filter buttons — compact pills ── */
.main .stButton > button {
    padding: 2px 10px !important; height: 24px !important;
    min-height: 24px !important; font-size: 0.71rem !important;
    border-radius: 12px !important; border: 1px solid #243050 !important;
    background: transparent !important; color: #94a3b8 !important;
    font-weight: 500 !important; margin: 1px !important;
    transition: all 0.15s !important; box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
}
.main .stButton > button:hover {
    background: rgba(59,130,246,0.12) !important;
    border-color: #3b82f6 !important; color: #93c5fd !important;
}
.main .stButton > button:focus, .main .stButton > button:active {
    background: rgba(30,58,138,0.4) !important;
    border-color: #3b82f6 !important; color: #93c5fd !important;
    box-shadow: 0 0 8px rgba(59,130,246,0.35) !important;
}

/* ── Filter section ── */
.filter-section {
    background: #0c1424; border: 1px solid #1a2540;
    border-radius: 11px; padding: 10px 16px 8px; margin-bottom: 18px;
}
.filter-label {
    font-size: 0.64rem; font-weight: 600; color: #475569;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin: 3px 0 !important; padding-top: 3px !important;
}

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 12px; margin-bottom: 18px; }
.kpi-card {
    background: linear-gradient(145deg, #0f1629, #0b101f);
    border-radius: 13px; padding: 18px 16px;
    border: 1px solid #1e2a4a; position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 13px 13px 0 0;
}
.kpi-blue   { box-shadow: 0 0 20px rgba(59,130,246,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-blue::before   { background: linear-gradient(90deg,#3b82f6,#2563eb); }
.kpi-green  { box-shadow: 0 0 20px rgba(16,185,129,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-green::before  { background: linear-gradient(90deg,#10b981,#059669); }
.kpi-cyan   { box-shadow: 0 0 20px rgba(6,182,212,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-cyan::before   { background: linear-gradient(90deg,#06b6d4,#0891b2); }
.kpi-red    { box-shadow: 0 0 20px rgba(239,68,68,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-red::before    { background: linear-gradient(90deg,#ef4444,#dc2626); }
.kpi-purple { box-shadow: 0 0 20px rgba(139,92,246,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-purple::before { background: linear-gradient(90deg,#8b5cf6,#7c3aed); }
.kpi-yellow { box-shadow: 0 0 20px rgba(245,158,11,0.2), 0 4px 14px rgba(0,0,0,0.35); }
.kpi-yellow::before { background: linear-gradient(90deg,#f59e0b,#d97706); }
.kpi-top { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; }
.kpi-title { font-size: 0.62rem; font-weight: 600; color: #475569; letter-spacing: 1.4px; text-transform: uppercase; }
.kpi-icon  { font-size: 1.1rem; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #fff; line-height: 1.1; margin-bottom: 4px; }
.kpi-sub   { font-size: 0.68rem; color: #334155; }

/* ── Chart Cards ── */
.chart-card {
    background: linear-gradient(145deg, #0f1629, #0b101f);
    border: 1px solid #1a2540; border-radius: 13px; padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 0 22px rgba(20,30,60,0.5), 0 4px 16px rgba(0,0,0,0.35);
    transition: box-shadow 0.3s;
}
.chart-card:hover { box-shadow: 0 0 32px rgba(59,130,246,0.1), 0 6px 20px rgba(0,0,0,0.4); }
.chart-title {
    font-size: 0.88rem; font-weight: 600; color: #e2e8f0;
    margin-bottom: 12px; display: flex; align-items: center; gap: 7px;
}

/* ── Page Title ── */
.page-title {
    display: flex; align-items: center; gap: 10px; white-space: nowrap;
    font-size: 1.45rem; font-weight: 800; color: #fff; margin-bottom: 18px;
}
.page-title-bar {
    width: 4px; height: 26px; flex-shrink: 0;
    background: linear-gradient(180deg, #3b82f6, #7c3aed);
    border-radius: 2px; display: inline-block;
    box-shadow: 0 0 10px rgba(99,102,241,0.6);
}

/* ── Nav label ── */
.nav-label {
    font-size: 0.6rem; font-weight: 600; color: #2d3a5a;
    letter-spacing: 2px; text-transform: uppercase; padding: 0 6px; margin: 10px 0 4px;
}
.data-badge {
    background: #070b18; border: 1px solid #1a2540; border-radius: 8px;
    padding: 8px 10px; font-size: 0.7rem; color: #334155; line-height: 1.9;
}

/* ── Table ── */
[data-testid="stDataFrame"] { border: 1px solid #1a2540 !important; border-radius: 10px !important; overflow: hidden !important; }
hr { border-color: #1a2540 !important; margin: 8px 0 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #1e2a4a; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_2024_25.csv")
    df["Order_Date"]             = pd.to_datetime(df["Order_Date"])
    df["Expected_Delivery_Date"] = pd.to_datetime(df["Expected_Delivery_Date"])
    df["Actual_Delivery_Date"]   = pd.to_datetime(df["Actual_Delivery_Date"])
    df["Quality_Rating"] = pd.to_numeric(df["Quality_Rating"], errors="coerce")
    df["Final_Cost_INR"] = pd.to_numeric(df["Final_Cost_INR"], errors="coerce")
    df["Delay_Days"]     = pd.to_numeric(df["Delay_Days"],     errors="coerce").fillna(0)
    df["Month"]          = df["Order_Date"].dt.to_period("M").astype(str)
    df["Delay_Flag"]     = (df["Delay_Days"] > 0).astype(int)
    return df

df_raw = load_data()

# ─── SQL ENGINE + 12 QUERIES ─────────────────────────────────────────────────
def run_sql(df, query):
    """Run SQL on a DataFrame using in-memory SQLite."""
    conn = sqlite3.connect(":memory:")
    df.to_sql("orders", conn, index=False, if_exists="replace")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

SQL = {
    # Q1 — Overall KPI summary
    "Q1_kpi": """
        SELECT COUNT(*) AS total_orders,
               ROUND(SUM(Final_Cost_INR), 2) AS total_revenue,
               ROUND(AVG(Lead_Time_Days), 1) AS avg_lead_time,
               SUM(CASE WHEN Order_Status='Delayed'   THEN 1 ELSE 0 END) AS delayed,
               SUM(CASE WHEN Order_Status='Delivered' THEN 1 ELSE 0 END) AS delivered,
               ROUND(AVG(Quality_Rating), 2) AS avg_quality
        FROM orders
    """,
    # Q2 — Monthly order count
    "Q2_monthly_orders": """
        SELECT strftime('%Y-%m', Order_Date) AS month, COUNT(*) AS orders
        FROM orders GROUP BY month ORDER BY month
    """,
    # Q3 — Order status split
    "Q3_status": """
        SELECT Order_Status, COUNT(*) AS count
        FROM orders GROUP BY Order_Status ORDER BY count DESC
    """,
    # Q4 — Revenue by product category
    "Q4_rev_category": """
        SELECT Category, ROUND(SUM(Final_Cost_INR)/1000, 1) AS revenue_k
        FROM orders GROUP BY Category ORDER BY revenue_k DESC
    """,
    # Q5 — Monthly revenue trend
    "Q5_monthly_revenue": """
        SELECT strftime('%Y-%m', Order_Date) AS month,
               ROUND(SUM(Final_Cost_INR)/1000, 1) AS revenue_k
        FROM orders GROUP BY month ORDER BY month
    """,
    # Q6 — Monthly total orders vs delayed
    "Q6_orders_delays": """
        SELECT strftime('%Y-%m', Order_Date) AS month,
               COUNT(*) AS total_orders,
               SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS delayed
        FROM orders GROUP BY month ORDER BY month
    """,
    # Q7 — Delay count per warehouse
    "Q7_wh_delays": """
        SELECT Warehouse,
               SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS delays,
               COUNT(*) AS total
        FROM orders GROUP BY Warehouse ORDER BY delays DESC
    """,
    # Q8 — Supplier quality ranking
    "Q8_supplier_quality": """
        SELECT Supplier_Name, ROUND(AVG(Quality_Rating), 2) AS avg_quality, COUNT(*) AS orders
        FROM orders WHERE Quality_Rating IS NOT NULL
        GROUP BY Supplier_Name ORDER BY avg_quality DESC
    """,
    # Q9 — Revenue per supplier
    "Q9_supplier_revenue": """
        SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000, 1) AS revenue_k, COUNT(*) AS orders
        FROM orders GROUP BY Supplier_Name ORDER BY revenue_k DESC
    """,
    # Q10 — Freight cost by shipping mode
    "Q10_freight_mode": """
        SELECT Shipping_Mode,
               ROUND(SUM(Freight_Cost_INR)/1000, 1) AS freight_k,
               ROUND(AVG(Freight_Cost_INR), 0)      AS avg_freight
        FROM orders GROUP BY Shipping_Mode ORDER BY freight_k DESC
    """,
    # Q11 — Warehouse × Category revenue matrix
    "Q11_wh_cat": """
        SELECT Warehouse, Category, ROUND(SUM(Final_Cost_INR)/1000, 1) AS revenue_k
        FROM orders GROUP BY Warehouse, Category ORDER BY Warehouse, Category
    """,
    # Q12 — Order status count by category
    "Q12_status_category": """
        SELECT Category, Order_Status, COUNT(*) AS count
        FROM orders GROUP BY Category, Order_Status ORDER BY Category, Order_Status
    """,
}

# ─── COLORS ──────────────────────────────────────────────────────────────────
PLOT_BG = "#0f1629"
GRID_C  = "#1a2540"
TICK_C  = "#64748b"
TEXT_C  = "#94a3b8"
FONT    = "Inter, sans-serif"

STATUS_COLORS = {
    "Delivered": "#10b981", "Delayed": "#f43f5e",
    "In Transit": "#3b82f6", "Pending": "#f59e0b", "Cancelled": "#6b7280",
}
CAT_COLORS  = ["#818cf8", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"]
SHIP_COLORS = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b"]
WH_COLORS   = ["#818cf8", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"]
SUP_COLORS  = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899","#8b5cf6","#ef4444","#3b82f6"]

def hex_rgba(h, a):
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

# ─── CHART HELPERS ───────────────────────────────────────────────────────────
def base_layout(height=300, bmargin=50):
    return dict(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT, color=TEXT_C, size=11),
        height=height, margin=dict(l=8, r=8, t=5, b=bmargin),
        hoverlabel=dict(
            bgcolor="#111827", bordercolor="#818cf8",
            font=dict(color="white", size=12, family=FONT),
        ),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C, size=10),
            orientation="h", y=-0.22, x=0.5, xanchor="center", itemgap=20,
        ),
    )

def ax(spike=False):
    d = dict(
        gridcolor=GRID_C, linecolor=GRID_C, tickcolor=GRID_C,
        tickfont=dict(color=TICK_C, size=10), zerolinecolor=GRID_C,
    )
    if spike:
        d.update(showspikes=True, spikesnap="cursor", spikemode="across",
                 spikethickness=1, spikecolor="rgba(255,255,255,0.45)", spikedash="solid")
    return d

def glow_line(fig, x, y, color, name, fill=True, show_legend=True):
    """Line chart with layered glow blur effect."""
    for w, a in [(16, 0.04), (10, 0.10), (5, 0.22)]:
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines",
            line=dict(color=hex_rgba(color, a), width=w),
            showlegend=False, hoverinfo="skip",
        ))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", name=name,
        line=dict(color=color, width=2),
        fill="tozeroy" if fill else None,
        fillcolor=hex_rgba(color, 0.08) if fill else None,
        marker=dict(size=5, color=color, line=dict(color="rgba(255,255,255,0.4)", width=1)),
        hovertemplate="<b>%{y}</b><extra>" + name + "</extra>",
        showlegend=show_legend,
    ))

def fmt_month(m):
    """Format '2024-07' → '07', '2025-02' → ''25-02'"""
    parts = m.split("-")
    if parts[0] == "2024":
        return parts[1]
    return f"'{parts[0][2:]}-{parts[1]}"

def big_hover():
    return dict(bgcolor="#111827", bordercolor="#818cf8",
                font=dict(color="white", size=12, family=FONT))

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "page"       not in st.session_state: st.session_state.page       = "Overview"
if "cat_filter" not in st.session_state: st.session_state.cat_filter = "All"
if "wh_filter"  not in st.session_state: st.session_state.wh_filter  = "All"

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-icon">📦</div>
        <div class="logo-name">LogiTrack</div>
        <div class="logo-badge">PRO</div>
    </div>
    <hr>
    <div class="nav-label">Navigation</div>
    """, unsafe_allow_html=True)

    NAV = [
        ("📊", "Overview"), ("🚚", "Delivery"),
        ("💰", "Cost & Revenue"), ("🏭", "Suppliers"), ("🏢", "Warehouse"),
    ]
    for icon, name in NAV:
        active = st.session_state.page == name
        if active: st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(f"{icon}  {name}", key=f"nav_{name}"):
            st.session_state.page = name
            st.rerun()
        if active: st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Dataset</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="data-badge">
    📅 FY 2024-25<br>
    📋 {len(df_raw)} Orders<br>
    🏭 {df_raw['Warehouse'].nunique()} Warehouses<br>
    🤝 {df_raw['Supplier_Name'].nunique()} Suppliers
    </div>""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def apply_filters(df):
    if st.session_state.cat_filter != "All":
        df = df[df["Category"] == st.session_state.cat_filter]
    if st.session_state.wh_filter != "All":
        df = df[df["Warehouse"] == st.session_state.wh_filter]
    return df.copy()

def filter_bar():
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    cats = ["All"] + sorted(df_raw["Category"].unique().tolist())
    whs  = ["All"] + sorted(df_raw["Warehouse"].unique().tolist())
    cc = st.columns([0.75] + [0.44] * len(cats))
    with cc[0]: st.markdown('<p class="filter-label">⚡ Category</p>', unsafe_allow_html=True)
    for i, c in enumerate(cats):
        with cc[i+1]:
            if st.button(c, key=f"cat_{c}", use_container_width=True):
                st.session_state.cat_filter = c; st.rerun()
    wc = st.columns([0.75] + [0.58] * len(whs))
    with wc[0]: st.markdown('<p class="filter-label">🏢 Warehouse</p>', unsafe_allow_html=True)
    for i, w in enumerate(whs):
        with wc[i+1]:
            if st.button(w, key=f"wh_{w}", use_container_width=True):
                st.session_state.wh_filter = w; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def kpi(title, value, sub, icon, cls):
    return (f'<div class="kpi-card {cls}">'
            f'<div class="kpi-top"><span class="kpi-title">{title}</span>'
            f'<span class="kpi-icon">{icon}</span></div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')

def cw(title, emoji):
    return f'<div class="chart-card"><div class="chart-title">{emoji} {title}</div>'


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
def page_overview():
    st.markdown('<div class="page-title"><span class="page-title-bar"></span>Supply Chain Overview</div>',
                unsafe_allow_html=True)
    filter_bar()
    df = apply_filters(df_raw)

    # Q1 KPIs
    row = run_sql(df, SQL["Q1_kpi"]).iloc[0]
    n      = int(row["total_orders"])
    rev    = float(row["total_revenue"] or 0)
    lead   = float(row["avg_lead_time"] or 0)
    dly    = int(row["delayed"])
    dlvd   = int(row["delivered"])
    aq     = float(row["avg_quality"] or 0)
    dpct   = dly/n*100 if n else 0
    dpct2  = dlvd/n*100 if n else 0
    rev_s  = f"₹{rev/100000:.1f}L" if rev >= 100000 else f"₹{rev:,.0f}"

    st.markdown('<div class="kpi-grid">' +
        kpi("TOTAL ORDERS",   str(n),            "filtered records",        "📦", "kpi-blue")   +
        kpi("REVENUE",        rev_s,              "final cost INR",          "📈", "kpi-green")  +
        kpi("AVG LEAD TIME",  f"{lead:.1f}d",     "order → delivery",        "⏱", "kpi-cyan")   +
        kpi("DELAYED ORDERS", str(dly),           f"{dpct:.0f}% delay rate", "⚠", "kpi-red")    +
        kpi("DELIVERED",      f"{dpct2:.0f}%",    f"{dlvd} orders",          "✅", "kpi-purple") +
        kpi("AVG QUALITY",    f"{aq:.2f}",        "rating / 5.0",            "⭐", "kpi-yellow") +
        '</div>', unsafe_allow_html=True)

    # Q2 Monthly Orders Trend (line + glow) | Q3 Order Status Donut
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(cw("Monthly Orders Trend", "📅"), unsafe_allow_html=True)
        mo = run_sql(df, SQL["Q2_monthly_orders"])
        mo["lbl"] = mo["month"].apply(fmt_month)
        fig = go.Figure()
        glow_line(fig, mo["lbl"], mo["orders"], "#818cf8", "Orders", fill=True, show_legend=False)
        fig.update_layout(**base_layout(290, 30), showlegend=False)
        fig.update_xaxes(**ax(spike=True))
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(cw("Order Status Split", "🍩"), unsafe_allow_html=True)
        sc = run_sql(df, SQL["Q3_status"])
        colors = [STATUS_COLORS.get(s, "#6b7280") for s in sc["Order_Status"]]
        fig = go.Figure(go.Pie(
            labels=sc["Order_Status"], values=sc["count"], hole=0.55,
            marker=dict(colors=colors, line=dict(color=PLOT_BG, width=3)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 30), hoverlabel=big_hover())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Q4 Revenue by Category (bar) | Q5 Monthly Revenue (line + glow)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Revenue by Category (₹K)", "💰"), unsafe_allow_html=True)
        rc = run_sql(df, SQL["Q4_rev_category"])
        fig = go.Figure(go.Bar(
            x=rc["Category"], y=rc["revenue_k"],
            marker=dict(color=CAT_COLORS[:len(rc)], opacity=0.9, line=dict(width=0)),
            text=rc["revenue_k"].apply(lambda v: f"₹{v:.0f}K"),
            textposition="outside", textfont=dict(size=9, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 55), showlegend=False, bargap=0.35)
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown(cw("Monthly Revenue (₹K)", "📈"), unsafe_allow_html=True)
        rm = run_sql(df, SQL["Q5_monthly_revenue"])
        rm["lbl"] = rm["month"].apply(fmt_month)
        fig = go.Figure()
        glow_line(fig, rm["lbl"], rm["revenue_k"], "#06b6d4", "Revenue (₹K)", fill=True, show_legend=False)
        fig.update_layout(**base_layout(290, 30), showlegend=False)
        fig.update_xaxes(**ax(spike=True))
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DELIVERY
# ══════════════════════════════════════════════════════════════════════════════
def page_delivery():
    st.markdown('<div class="page-title"><span class="page-title-bar"></span>Delivery Analytics</div>',
                unsafe_allow_html=True)
    filter_bar()
    df = apply_filters(df_raw)

    vm = df["Order_Status"].value_counts()
    on_time  = df[df["Delay_Days"] == 0].shape[0]
    avg_dly  = df[df["Delay_Days"] > 0]["Delay_Days"].mean() if df[df["Delay_Days"] > 0].shape[0] else 0

    st.markdown('<div class="kpi-grid">' +
        kpi("ON-TIME",    str(on_time),          "no delays",            "✅", "kpi-green")  +
        kpi("AVG DELAY",  f"{avg_dly:.1f}d",     "among delayed orders", "⚠", "kpi-red")    +
        kpi("DELIVERED",  str(vm.get("Delivered",0)), "completed",        "📦", "kpi-blue")  +
        kpi("IN TRANSIT", str(vm.get("In Transit",0)),"currently moving", "🚚", "kpi-cyan")  +
        kpi("CANCELLED",  str(vm.get("Cancelled",0)),  "cancelled",       "❌", "kpi-red")   +
        kpi("PENDING",    str(vm.get("Pending",0)),    "awaiting dispatch","⏳", "kpi-yellow")+
        '</div>', unsafe_allow_html=True)

    # Shipping Mode Pie | Lead Time Histogram
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(cw("Shipping Mode Distribution", "🚢"), unsafe_allow_html=True)
        sm = df["Shipping_Mode"].value_counts().reset_index()
        sm.columns = ["Mode", "Count"]
        fig = go.Figure(go.Pie(
            labels=sm["Mode"], values=sm["Count"], hole=0.52,
            marker=dict(colors=SHIP_COLORS, line=dict(color=PLOT_BG, width=3)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 40), hoverlabel=big_hover())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(cw("Lead Time Distribution", "📊"), unsafe_allow_html=True)
        fig = go.Figure(go.Histogram(
            x=df["Lead_Time_Days"], nbinsx=15,
            marker=dict(color="#818cf8", opacity=0.85, line=dict(color=PLOT_BG, width=1)),
            hovertemplate="Lead Time: <b>%{x}d</b><br>Count: <b>%{y}</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 50), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax(), title_text="Lead Time (Days)", title_font=dict(size=10, color=TICK_C))
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Q6 Monthly Orders vs Delays (overlay bar — matches screenshot 2)
    st.markdown(cw("Monthly Orders vs Delays", "📅"), unsafe_allow_html=True)
    od = run_sql(df, SQL["Q6_orders_delays"])
    od["lbl"] = od["month"].apply(fmt_month)
    fig = go.Figure()
    # Total Orders behind (blue, drawn first)
    fig.add_trace(go.Bar(
        x=od["lbl"], y=od["total_orders"], name="Total Orders",
        marker=dict(color="#4f6bbd", opacity=0.85, line=dict(width=0)),
        hovertemplate="Total Orders: <b>%{y}</b><extra></extra>",
    ))
    # Delayed on top (red, drawn second)
    fig.add_trace(go.Bar(
        x=od["lbl"], y=od["delayed"], name="Delayed",
        marker=dict(color="#f43f5e", opacity=0.95, line=dict(width=0)),
        hovertemplate="Delayed: <b>%{y}</b><extra></extra>",
    ))
    fig.update_layout(
        **base_layout(300, 68),
        barmode="overlay", bargap=0.22,
        hoverlabel=big_hover(),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C, size=10),
            orientation="h", y=-0.24, x=0.5, xanchor="center",
            itemgap=30, traceorder="reversed",
        ),
    )
    fig.update_xaxes(**ax())
    fig.update_yaxes(**ax())
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Q7 Delays by Warehouse | Q12 Status by Category stacked bar
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Delays by Warehouse", "🏭"), unsafe_allow_html=True)
        wd = run_sql(df, SQL["Q7_wh_delays"])
        fig = go.Figure(go.Bar(
            x=wd["Warehouse"], y=wd["delays"],
            marker=dict(color="#f43f5e", opacity=0.9, line=dict(width=0)),
            text=wd["delays"], textposition="outside",
            textfont=dict(size=10, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Delays: <b>%{y}</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(300, 50), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        # Q12 Order Status by Category stacked bar (matches screenshot 3)
        st.markdown(cw("Order Status by Category", "📦"), unsafe_allow_html=True)
        sc12 = run_sql(df, SQL["Q12_status_category"])
        status_order = ["Cancelled", "Delayed", "Delivered", "In Transit", "Pending"]
        fig = go.Figure()
        for s in status_order:
            sub = sc12[sc12["Order_Status"] == s]
            if sub.empty: continue
            fig.add_trace(go.Bar(
                x=sub["Category"], y=sub["count"], name=s,
                marker=dict(color=STATUS_COLORS[s], opacity=0.9, line=dict(width=0)),
                hovertemplate=f"{s}: <b>%{{y}}</b><extra></extra>",
            ))
        fig.update_layout(
            **base_layout(300, 72),
            barmode="stack", bargap=0.3,
            hoverlabel=big_hover(),
            legend=dict(
                bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C, size=10),
                orientation="h", y=-0.27, x=0.5, xanchor="center", itemgap=14,
            ),
        )
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Monthly delivery trend (multi-line glow)
    st.markdown(cw("Monthly Delivery Status Trend", "📈"), unsafe_allow_html=True)
    mdt = df.groupby(["Month", "Order_Status"]).size().reset_index(name="Count")
    mdt["lbl"] = mdt["Month"].apply(fmt_month)
    fig = go.Figure()
    for status, color in STATUS_COLORS.items():
        sub = mdt[mdt["Order_Status"] == status]
        if sub.empty: continue
        glow_line(fig, sub["lbl"], sub["Count"], color, status, fill=False, show_legend=True)
    fig.update_layout(**base_layout(290, 45), hoverlabel=big_hover())
    fig.update_xaxes(**ax(spike=True))
    fig.update_yaxes(**ax())
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — COST & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
def page_cost_revenue():
    st.markdown('<div class="page-title"><span class="page-title-bar"></span>Cost & Revenue Analysis</div>',
                unsafe_allow_html=True)
    filter_bar()
    df = apply_filters(df_raw)

    tot_rev  = df["Final_Cost_INR"].sum()
    tot_cost = df["Total_Cost_INR"].sum()
    freight  = df["Freight_Cost_INR"].sum()
    avg_disc = df["Discount_Pct"].mean()
    avg_unit = df["Unit_Cost_INR"].mean()
    margin   = (tot_rev - freight) / tot_rev * 100 if tot_rev else 0

    st.markdown('<div class="kpi-grid">' +
        kpi("TOTAL REVENUE",  f"₹{tot_rev/100000:.1f}L",  "final cost INR",   "📈", "kpi-green")  +
        kpi("BASE COST",      f"₹{tot_cost/100000:.1f}L", "before discount",  "💼", "kpi-blue")   +
        kpi("FREIGHT COST",   f"₹{freight/1000:.0f}K",    "logistics spend",  "🚢", "kpi-cyan")   +
        kpi("AVG DISCOUNT",   f"{avg_disc:.1f}%",          "avg discount",     "🏷", "kpi-yellow") +
        kpi("AVG UNIT PRICE", f"₹{avg_unit:,.0f}",         "per unit",         "📦", "kpi-purple") +
        kpi("NET MARGIN",     f"{margin:.1f}%",            "after freight",    "💰", "kpi-green")  +
        '</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(cw("Revenue by Category (₹K)", "💰"), unsafe_allow_html=True)
        rc = run_sql(df, SQL["Q4_rev_category"]).sort_values("revenue_k")
        fig = go.Figure(go.Bar(
            y=rc["Category"], x=rc["revenue_k"], orientation="h",
            marker=dict(color=CAT_COLORS[:len(rc)][::-1], opacity=0.9, line=dict(width=0)),
            text=rc["revenue_k"].apply(lambda v: f"₹{v:.0f}K"),
            textposition="outside", textfont=dict(size=9, color=TEXT_C),
            hovertemplate="<b>%{y}</b><br>Revenue: <b>₹%{x:.0f}K</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 20), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(cw("Freight Cost by Shipping Mode", "🚢"), unsafe_allow_html=True)
        fm = run_sql(df, SQL["Q10_freight_mode"])
        fig = go.Figure(go.Pie(
            labels=fm["Shipping_Mode"], values=fm["freight_k"], hole=0.52,
            marker=dict(colors=SHIP_COLORS, line=dict(color=PLOT_BG, width=3)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Freight: <b>₹%{value:.0f}K</b><br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 40), hoverlabel=big_hover())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Monthly Revenue Trend (₹K)", "📅"), unsafe_allow_html=True)
        rm = run_sql(df, SQL["Q5_monthly_revenue"])
        rm["lbl"] = rm["month"].apply(fmt_month)
        fig = go.Figure()
        glow_line(fig, rm["lbl"], rm["revenue_k"], "#06b6d4", "Revenue (₹K)", fill=True, show_legend=False)
        fig.update_layout(**base_layout(290, 30), showlegend=False)
        fig.update_xaxes(**ax(spike=True))
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown(cw("Avg Discount by Category", "🏷"), unsafe_allow_html=True)
        dc = df.groupby("Category")["Discount_Pct"].mean().reset_index()
        dc.columns = ["Category", "Avg_Disc"]
        fig = go.Figure(go.Bar(
            x=dc["Category"], y=dc["Avg_Disc"],
            marker=dict(color=CAT_COLORS[:len(dc)], opacity=0.9, line=dict(width=0)),
            text=dc["Avg_Disc"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside", textfont=dict(size=9, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Avg Discount: <b>%{y:.1f}%</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 55), showlegend=False, bargap=0.35,
                          hoverlabel=big_hover())
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(cw("Quantity vs Revenue by Category", "🔍"), unsafe_allow_html=True)
    fig = px.scatter(df, x="Quantity", y="Final_Cost_INR", color="Category",
                     color_discrete_sequence=CAT_COLORS, size="Lead_Time_Days", opacity=0.8,
                     hover_data=["Order_ID", "Supplier_Name"])
    fig.update_layout(**base_layout(310, 50), hoverlabel=big_hover())
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_xaxes(**ax())
    fig.update_yaxes(**ax())
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SUPPLIERS
# ══════════════════════════════════════════════════════════════════════════════
def page_suppliers():
    st.markdown('<div class="page-title"><span class="page-title-bar"></span>Supplier Performance</div>',
                unsafe_allow_html=True)
    filter_bar()
    df = apply_filters(df_raw)

    sq8    = run_sql(df, SQL["Q8_supplier_quality"])
    sr9    = run_sql(df, SQL["Q9_supplier_revenue"])
    total_s = df["Supplier_Name"].nunique()
    best_s  = sq8.iloc[0]["Supplier_Name"] if len(sq8) else "N/A"
    best_sc = sq8.iloc[0]["avg_quality"]    if len(sq8) else 0
    top_rs  = sr9.iloc[0]["Supplier_Name"] if len(sr9) else "N/A"
    most_o  = df["Supplier_Name"].value_counts().idxmax() if len(df) else "N/A"
    avg_q   = df["Quality_Rating"].mean()
    pay_t   = df["Payment_Terms"].nunique()

    st.markdown('<div class="kpi-grid">' +
        kpi("SUPPLIERS",   str(total_s),          "active",              "🏭", "kpi-blue")   +
        kpi("BEST QUALITY",best_s.split()[0],     f"★ {best_sc:.2f}",   "⭐", "kpi-yellow") +
        kpi("TOP REVENUE", top_rs.split()[0],     "highest revenue",    "💰", "kpi-green")  +
        kpi("AVG QUALITY", f"{avg_q:.2f}",        "rating / 5.0",       "📊", "kpi-cyan")   +
        kpi("MOST ORDERS", most_o.split()[0],     "by order count",     "📦", "kpi-purple") +
        kpi("PAY TYPES",   str(pay_t),            "payment terms used", "💳", "kpi-red")    +
        '</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(cw("Avg Quality Rating by Supplier", "⭐"), unsafe_allow_html=True)
        sq = sq8.sort_values("avg_quality")
        fig = go.Figure(go.Bar(
            y=sq["Supplier_Name"], x=sq["avg_quality"], orientation="h",
            marker=dict(color=sq["avg_quality"].tolist(),
                        colorscale=[[0,"#ef4444"],[0.5,"#f59e0b"],[1,"#10b981"]],
                        opacity=0.9, showscale=False),
            text=sq["avg_quality"].apply(lambda v: f"{v:.2f}"),
            textposition="outside", textfont=dict(size=9, color=TEXT_C),
            hovertemplate="<b>%{y}</b><br>Quality: <b>%{x:.2f}</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(330, 20), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax(), range=[0, 5.8])
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(cw("Revenue by Supplier (₹K)", "💰"), unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=sr9["Supplier_Name"], y=sr9["revenue_k"],
            marker=dict(color=SUP_COLORS[:len(sr9)], opacity=0.9, line=dict(width=0)),
            text=sr9["revenue_k"].apply(lambda v: f"₹{v:.0f}K"),
            textposition="outside", textfont=dict(size=9, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(330, 60), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax(), tickangle=-30, tickfont=dict(size=9, color=TICK_C))
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Orders by Supplier", "📦"), unsafe_allow_html=True)
        so = df["Supplier_Name"].value_counts().reset_index()
        so.columns = ["Supplier", "Orders"]
        fig = go.Figure(go.Pie(
            labels=so["Supplier"], values=so["Orders"], hole=0.52,
            marker=dict(colors=SUP_COLORS, line=dict(color=PLOT_BG, width=2)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Orders: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**base_layout(310, 40), hoverlabel=big_hover())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown(cw("Payment Terms Distribution", "💳"), unsafe_allow_html=True)
        pt = df["Payment_Terms"].value_counts().reset_index()
        pt.columns = ["Terms", "Count"]
        fig = go.Figure(go.Bar(
            x=pt["Terms"], y=pt["Count"],
            marker=dict(color=CAT_COLORS[:len(pt)], opacity=0.9, line=dict(width=0)),
            text=pt["Count"], textposition="outside",
            textfont=dict(size=10, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Count: <b>%{y}</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(310, 55), showlegend=False, bargap=0.35,
                          hoverlabel=big_hover())
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(cw("Supplier Summary Table", "📋"), unsafe_allow_html=True)
    summ = df.groupby("Supplier_Name").agg(
        Orders=("Order_ID","count"),
        Revenue=("Final_Cost_INR","sum"),
        Avg_Lead=("Lead_Time_Days","mean"),
        Avg_Quality=("Quality_Rating","mean"),
        Delayed=("Delay_Flag","sum"),
    ).reset_index()
    summ["Revenue"]     = summ["Revenue"].apply(lambda v: f"₹{v:,.0f}")
    summ["Avg_Lead"]    = summ["Avg_Lead"].apply(lambda v: f"{v:.1f}d")
    summ["Avg_Quality"] = summ["Avg_Quality"].apply(lambda v: f"{v:.2f}" if pd.notna(v) else "N/A")
    summ.columns = ["Supplier","Orders","Revenue","Avg Lead","Avg Quality","Delayed"]
    st.dataframe(summ, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — WAREHOUSE
# ══════════════════════════════════════════════════════════════════════════════
def page_warehouse():
    st.markdown('<div class="page-title"><span class="page-title-bar"></span>Warehouse Analytics</div>',
                unsafe_allow_html=True)
    filter_bar()
    df = apply_filters(df_raw)

    wo = df["Warehouse"].value_counts()
    wr = df.groupby("Warehouse")["Final_Cost_INR"].sum()
    total_wh  = df["Warehouse"].nunique()
    busy_wh   = wo.idxmax()
    top_r_wh  = wr.idxmax()
    total_qty = int(df["Quantity"].sum())
    avg_qty   = df.groupby("Warehouse")["Quantity"].sum().mean()

    st.markdown('<div class="kpi-grid">' +
        kpi("WAREHOUSES",  str(total_wh),                "active locations",   "🏢", "kpi-blue")   +
        kpi("BUSIEST WH",  busy_wh.replace("WH-",""),    f"{wo.max()} orders", "📦", "kpi-cyan")   +
        kpi("TOP REVENUE", top_r_wh.replace("WH-",""),   "highest revenue",    "💰", "kpi-green")  +
        kpi("TOTAL QTY",   f"{total_qty:,}",              "units processed",    "📊", "kpi-purple") +
        kpi("AVG QTY/WH",  f"{avg_qty:,.0f}",             "per warehouse",      "⚖", "kpi-yellow") +
        kpi("CATEGORIES",  str(df["Category"].nunique()), "product types",      "🏷", "kpi-red")    +
        '</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(cw("Orders by Warehouse", "📦"), unsafe_allow_html=True)
        wod = wo.reset_index(); wod.columns = ["Warehouse","Orders"]
        fig = go.Figure(go.Pie(
            labels=wod["Warehouse"], values=wod["Orders"], hole=0.52,
            marker=dict(colors=WH_COLORS, line=dict(color=PLOT_BG, width=2)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Orders: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 40), hoverlabel=big_hover())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(cw("Revenue by Warehouse (₹K)", "💰"), unsafe_allow_html=True)
        wrd = wr.div(1000).reset_index().sort_values("Final_Cost_INR", ascending=False)
        wrd.columns = ["Warehouse", "Revenue_K"]
        fig = go.Figure(go.Bar(
            x=wrd["Warehouse"], y=wrd["Revenue_K"],
            marker=dict(color=WH_COLORS[:len(wrd)], opacity=0.9, line=dict(width=0)),
            text=wrd["Revenue_K"].apply(lambda v: f"₹{v:.0f}K"),
            textposition="outside", textfont=dict(size=10, color=TEXT_C),
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        fig.update_layout(**base_layout(290, 50), showlegend=False, hoverlabel=big_hover())
        fig.update_xaxes(**ax())
        fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Category Mix by Warehouse", "🏷"), unsafe_allow_html=True)
        wc2 = df.groupby(["Warehouse","Category"]).size().reset_index(name="Count")
        fig = px.bar(wc2, x="Warehouse", y="Count", color="Category",
                     color_discrete_sequence=CAT_COLORS, barmode="stack")
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**base_layout(290, 70), hoverlabel=big_hover(),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C, size=10),
                                      orientation="h", y=-0.26, x=0.5, xanchor="center",
                                      itemgap=12, title_text=""))
        fig.update_xaxes(**ax()); fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown(cw("Shipping Mode by Warehouse", "🚚"), unsafe_allow_html=True)
        ws = df.groupby(["Warehouse","Shipping_Mode"]).size().reset_index(name="Count")
        fig = px.bar(ws, x="Warehouse", y="Count", color="Shipping_Mode",
                     color_discrete_sequence=SHIP_COLORS, barmode="group")
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**base_layout(290, 70), hoverlabel=big_hover(),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C, size=10),
                                      orientation="h", y=-0.26, x=0.5, xanchor="center",
                                      itemgap=12, title_text=""))
        fig.update_xaxes(**ax()); fig.update_yaxes(**ax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Q11 Revenue Heatmap
    st.markdown(cw("Revenue Heatmap — Warehouse × Category (₹K)", "🔥"), unsafe_allow_html=True)
    pivot = df.pivot_table(values="Final_Cost_INR", index="Warehouse",
                           columns="Category", aggfunc="sum", fill_value=0).div(1000)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,"#0f1629"],[0.3,"#1e3a5f"],[0.6,"#2563eb"],[1,"#818cf8"]],
        text=np.round(pivot.values, 0),
        texttemplate="₹%{text}K", textfont=dict(size=10, color="white"),
        showscale=True,
        colorbar=dict(tickfont=dict(color=TEXT_C), outlinecolor=GRID_C, outlinewidth=1),
        hovertemplate="<b>%{y} × %{x}</b><br>Revenue: <b>₹%{z:.0f}K</b><extra></extra>",
    ))
    fig.update_layout(**base_layout(300, 20), hoverlabel=big_hover())
    fig.update_xaxes(tickfont=dict(color=TICK_C, size=10))
    fig.update_yaxes(tickfont=dict(color=TICK_C, size=10))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ─── ROUTER ──────────────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "Overview":      page_overview()
elif page == "Delivery":      page_delivery()
elif page == "Cost & Revenue": page_cost_revenue()
elif page == "Suppliers":     page_suppliers()
elif page == "Warehouse":     page_warehouse()

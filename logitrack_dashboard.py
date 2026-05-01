# ═══════════════════════════════════════════════════════════════════════════
# LogiTrack PRO | Supply Chain Dashboard
# Streamlit + Plotly + SQLite | 12 SQL Queries
# ═══════════════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sqlite3
st.set_page_config(
    page_title="LogiTrack PRO",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #070b18 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }
.block-container { padding: 1.2rem 1.8rem !important; max-width: 100% !important; }
/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid #1a2540 !important;
    width: 210px !important; min-width: 210px !important;
}
section[data-testid="stSidebar"] > div:first-child { width: 210px !important; }
/* ── Logo ── */
.logo-wrap {
    display: flex; flex-direction: column; align-items: center;
    padding: 22px 12px 16px;
}
.logo-box {
    width: 66px; height: 66px; border-radius: 16px;
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 10px;
    box-shadow: 0 0 28px rgba(99,102,241,0.6), 0 0 55px rgba(37,99,235,0.2);
}
.logo-name { font-size: 1.15rem; font-weight: 700; color: #fff; }
.logo-pro  { font-size: 0.54rem; font-weight: 700; color: #a78bfa; letter-spacing: 3.5px; text-transform: uppercase; margin-top: 2px; }
/* ── Sidebar nav ── */
.nav-label {
    font-size: 0.6rem; font-weight: 600; color: #2d3a5a;
    letter-spacing: 2px; text-transform: uppercase; padding: 0 8px; margin: 10px 0 5px;
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important; text-align: left !important;
    padding: 9px 14px !important; border-radius: 10px !important;
    border: none !important; font-size: 0.84rem !important;
    font-weight: 500 !important; color: #64748b !important;
    background: transparent !important; margin-bottom: 2px !important;
    transition: all 0.2s !important; box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,102,241,0.1) !important; color: #cbd5e1 !important;
}
section[data-testid="stSidebar"] .nav-active .stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: #fff !important; font-weight: 600 !important;
    box-shadow: 0 0 18px rgba(99,102,241,0.55), inset 0 0 20px rgba(255,255,255,0.05) !important;
}
/* ── Filter pills (st.pills) ── */
button[data-testid="stPillsButton"] {
    padding: 2px 10px !important; height: 24px !important;
    min-height: 24px !important; font-size: 0.71rem !important;
    border-radius: 12px !important; border: 1px solid #243050 !important;
    background: transparent !important; color: #64748b !important;
    font-weight: 500 !important; transition: all 0.15s !important;
    font-family: 'Inter', sans-serif !important; box-shadow: none !important;
}
button[data-testid="stPillsButton"][aria-pressed="true"] {
    background: rgba(30,58,138,0.45) !important;
    border-color: #3b82f6 !important; color: #93c5fd !important;
    box-shadow: 0 0 10px rgba(59,130,246,0.3) !important;
}
button[data-testid="stPillsButton"]:hover {
    border-color: #3b82f6 !important; color: #93c5fd !important;
    background: rgba(30,58,138,0.2) !important;
}
div[data-testid="stPills"] { gap: 2px !important; flex-wrap: wrap !important; }
div[data-testid="stPills"] > div > label {
    font-size: 0.63rem !important; color: #475569 !important;
    font-weight: 600 !important; letter-spacing: 1.4px !important;
    text-transform: uppercase !important;
}
/* ── Filter wrapper ── */
.filter-wrap {
    background: #0c1424; border: 1px solid #1a2540;
    border-radius: 11px; padding: 10px 16px 10px; margin-bottom: 18px;
}
/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 12px; margin-bottom: 18px; }
.kc {
    background: linear-gradient(145deg,#0f1629,#0b101f);
    border-radius: 13px; padding: 17px 15px;
    border: 1px solid #1e2a4a; position: relative; overflow: hidden;
    transition: transform 0.2s;
}
.kc:hover { transform: translateY(-2px); }
.kc::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:13px 13px 0 0; }
.kb  { box-shadow: 0 0 22px rgba(59,130,246,0.18),  0 4px 14px rgba(0,0,0,0.4); }
.kb::before  { background: linear-gradient(90deg,#3b82f6,#2563eb); }
.kg  { box-shadow: 0 0 22px rgba(16,185,129,0.18),   0 4px 14px rgba(0,0,0,0.4); }
.kg::before  { background: linear-gradient(90deg,#10b981,#059669); }
.kc2 { box-shadow: 0 0 22px rgba(6,182,212,0.18),    0 4px 14px rgba(0,0,0,0.4); }
.kc2::before { background: linear-gradient(90deg,#06b6d4,#0891b2); }
.kr  { box-shadow: 0 0 22px rgba(239,68,68,0.18),    0 4px 14px rgba(0,0,0,0.4); }
.kr::before  { background: linear-gradient(90deg,#ef4444,#dc2626); }
.kp  { box-shadow: 0 0 22px rgba(139,92,246,0.18),   0 4px 14px rgba(0,0,0,0.4); }
.kp::before  { background: linear-gradient(90deg,#8b5cf6,#7c3aed); }
.ky  { box-shadow: 0 0 22px rgba(245,158,11,0.18),   0 4px 14px rgba(0,0,0,0.4); }
.ky::before  { background: linear-gradient(90deg,#f59e0b,#d97706); }
.kt { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; }
.kn { font-size:0.61rem; font-weight:600; color:#475569; letter-spacing:1.4px; text-transform:uppercase; }
.ki { font-size:1.05rem; }
.kv { font-size:1.78rem; font-weight:800; color:#fff; line-height:1.1; margin-bottom:4px; }
.ks { font-size:0.67rem; color:#2d3a5a; }
/* ── Chart Cards ── */
.cc {
    background: linear-gradient(145deg,#0f1629,#0b101f);
    border: 1px solid #1a2540; border-radius: 13px; padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 0 24px rgba(15,22,41,0.6), 0 4px 16px rgba(0,0,0,0.4);
    transition: box-shadow 0.3s;
}
.cc:hover { box-shadow: 0 0 35px rgba(59,130,246,0.08), 0 6px 20px rgba(0,0,0,0.45); }
.ct { font-size:0.88rem; font-weight:600; color:#e2e8f0; margin-bottom:12px; display:flex; align-items:center; gap:7px; }
/* ── Page Title ── */
.pt {
    display:flex; align-items:center; gap:10px; white-space:nowrap;
    font-size:1.45rem; font-weight:800; color:#fff; margin-bottom:18px;
}
.ptb {
    width:4px; height:26px; flex-shrink:0;
    background:linear-gradient(180deg,#3b82f6,#7c3aed);
    border-radius:2px; display:inline-block;
    box-shadow:0 0 12px rgba(99,102,241,0.65);
}
/* ── Table & misc ── */
[data-testid="stDataFrame"] { border:1px solid #1a2540 !important; border-radius:10px !important; }
hr { border-color:#1a2540 !important; margin:8px 0 !important; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#0a0f1e; }
::-webkit-scrollbar-thumb { background:#1e2a4a; border-radius:10px; }
</style>
""", unsafe_allow_html=True)
# ─── DATA LOADING ─────────────────────────────────────────────────────────────
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
    conn = sqlite3.connect(":memory:")
    df.to_sql("orders", conn, index=False, if_exists="replace")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result
SQL = {
    # Q1  Overall KPI summary
    "Q1":  "SELECT COUNT(*) AS n, ROUND(SUM(Final_Cost_INR),2) AS rev, ROUND(AVG(Lead_Time_Days),1) AS lead, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS dly, SUM(CASE WHEN Order_Status='Delivered' THEN 1 ELSE 0 END) AS dlvd, ROUND(AVG(Quality_Rating),2) AS aq FROM orders",
    # Q2  Monthly order count
    "Q2":  "SELECT strftime('%Y-%m',Order_Date) AS m, COUNT(*) AS n FROM orders GROUP BY m ORDER BY m",
    # Q3  Order status split
    "Q3":  "SELECT Order_Status AS s, COUNT(*) AS n FROM orders GROUP BY s ORDER BY n DESC",
    # Q4  Revenue by category
    "Q4":  "SELECT Category AS c, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev FROM orders GROUP BY c ORDER BY rev DESC",
    # Q5  Monthly revenue
    "Q5":  "SELECT strftime('%Y-%m',Order_Date) AS m, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev FROM orders GROUP BY m ORDER BY m",
    # Q6  Monthly orders vs delayed
    "Q6":  "SELECT strftime('%Y-%m',Order_Date) AS m, COUNT(*) AS total, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS dly FROM orders GROUP BY m ORDER BY m",
    # Q7  Delays by warehouse
    "Q7":  "SELECT Warehouse AS wh, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS dly FROM orders GROUP BY wh ORDER BY dly DESC",
    # Q8  Supplier quality ranking
    "Q8":  "SELECT Supplier_Name AS sup, ROUND(AVG(Quality_Rating),2) AS aq FROM orders WHERE Quality_Rating IS NOT NULL GROUP BY sup ORDER BY aq DESC",
    # Q9  Revenue per supplier
    "Q9":  "SELECT Supplier_Name AS sup, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev FROM orders GROUP BY sup ORDER BY rev DESC",
    # Q10 Freight by shipping mode
    "Q10": "SELECT Shipping_Mode AS mode, ROUND(SUM(Freight_Cost_INR)/1000,1) AS fr FROM orders GROUP BY mode ORDER BY fr DESC",
    # Q11 Warehouse x Category revenue
    "Q11": "SELECT Warehouse AS wh, Category AS c, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev FROM orders GROUP BY wh,c ORDER BY wh,c",
    # Q12 Order status by category
    "Q12": "SELECT Category AS c, Order_Status AS s, COUNT(*) AS n FROM orders GROUP BY c,s ORDER BY c,s",
}
# ─── COLORS ───────────────────────────────────────────────────────────────────
BG   = "#0f1629"
GRID = "#1a2540"
TICK = "#64748b"
TEXT = "#94a3b8"
FONT = "Inter, sans-serif"
SC = {
    "Delivered": "#10b981", "Delayed":    "#f43f5e",
    "In Transit":"#3b82f6", "Pending":    "#f59e0b",
    "Cancelled": "#6b7280",
}
C5 = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899"]
C4 = ["#3b82f6","#10b981","#8b5cf6","#f59e0b"]
C8 = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899","#8b5cf6","#ef4444","#3b82f6"]
HLABEL = dict(
    bgcolor="#0d1830", bordercolor="#818cf8",
    font=dict(color="white", size=12, family=FONT)
)
def lc(h, a):
    h = h.lstrip("#")
    r, g, b = int(h[:2],16), int(h[2:4],16), int(h[4:],16)
    return f"rgba({r},{g},{b},{a})"
def fmt(m):
    p = m.split("-")
    return p[1] if p[0] == "2024" else f"'{p[0][2:]}-{p[1]}"
def xax():
    return dict(
        gridcolor=GRID, linecolor=GRID, tickcolor=GRID,
        tickfont=dict(color=TICK, size=10), zerolinecolor=GRID
    )
def spike_ax():
    return dict(
        showspikes=True, spikesnap="cursor", spikemode="across",
        spikethickness=1, spikecolor="rgba(255,255,255,0.4)", spikedash="solid"
    )
def yax():
    return dict(
        gridcolor=GRID, linecolor=GRID, tickcolor=GRID,
        tickfont=dict(color=TICK, size=10), zerolinecolor=GRID
    )
def base_pie(fig, h=290, bm=42):
    fig.update_layout(
        paper_bgcolor=BG, height=h,
        margin=dict(l=8, r=8, t=5, b=bm),
        hoverlabel=HLABEL, showlegend=True,
        font=dict(family=FONT, color=TEXT, size=11),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=10),
            orientation="h", y=-0.12, x=0.5, xanchor="center"
        ),
    )
def base_bar(fig, h=300, bm=55, show_legend=False, leg_y=-0.22):
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, height=h,
        margin=dict(l=8, r=8, t=5, b=bm),
        showlegend=show_legend,
        hoverlabel=HLABEL, hovermode="x unified",
        font=dict(family=FONT, color=TEXT, size=11),
    )
    if show_legend:
        fig.update_layout(legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=10),
            orientation="h", y=leg_y, x=0.5, xanchor="center", itemgap=16,
        ))
def glow(fig, x, y, color, name, fill=True, show_leg=True):
    """Line with layered glow effect."""
    for w, a in [(15, 0.04), (9, 0.11), (5, 0.23)]:
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines",
            line=dict(color=lc(color, a), width=w),
            showlegend=False, hoverinfo="skip",
        ))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", name=name,
        line=dict(color=color, width=2),
        fill="tozeroy" if fill else None,
        fillcolor=lc(color, 0.08) if fill else None,
        marker=dict(size=5, color=color,
                    line=dict(color="rgba(255,255,255,0.35)", width=1)),
        hovertemplate="%{y}<extra>" + name + "</extra>",
        showlegend=show_leg,
    ))
def base_line(fig, h=290, bm=30, show_legend=False):
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, height=h,
        margin=dict(l=8, r=8, t=5, b=bm),
        showlegend=show_legend,
        hoverlabel=HLABEL, hovermode="x unified",
        font=dict(family=FONT, color=TEXT, size=11),
    )
    if show_legend:
        fig.update_layout(legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=10),
            orientation="h", y=-0.22, x=0.5, xanchor="center", itemgap=16,
        ))
# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Overview"
# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-box">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none"
             stroke="white" stroke-width="1.6"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
          <line x1="12" y1="22.08" x2="12" y2="12"/>
        </svg>
      </div>
      <div class="logo-name">LogiTrack</div>
      <div class="logo-pro">PRO</div>
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
        if active:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(f"{icon}  {name}", key=f"nav_{name}"):
            st.session_state.page = name
            st.rerun()
        if active:
            st.markdown("</div>", unsafe_allow_html=True)
# ─── FILTER BAR ───────────────────────────────────────────────────────────────
def filter_bar():
    cats = ["All"] + sorted(df_raw["Category"].unique().tolist())
    whs  = ["All"] + sorted(df_raw["Warehouse"].unique().tolist())
    st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        cat = st.pills("⚡ Category", cats, default="All", key="f_cat")
    with c2:
        wh  = st.pills("🏢 Warehouse", whs, default="All", key="f_wh")
    st.markdown("</div>", unsafe_allow_html=True)
    return (cat or "All"), (wh or "All")
def filt(df, cat, wh):
    if cat != "All": df = df[df["Category"] == cat]
    if wh  != "All": df = df[df["Warehouse"] == wh]
    return df.copy()
# ─── KPI + CHART HELPERS ──────────────────────────────────────────────────────
def kpi(title, val, sub, icon, cls):
    return (f'<div class="kc {cls}"><div class="kt">'
            f'<span class="kn">{title}</span><span class="ki">{icon}</span></div>'
            f'<div class="kv">{val}</div><div class="ks">{sub}</div></div>')
def cw(title, em):
    return f'<div class="cc"><div class="ct">{em} {title}</div>'
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
def page_overview():
    st.markdown('<div class="pt"><span class="ptb"></span>Supply Chain Overview</div>',
                unsafe_allow_html=True)
    cat, wh = filter_bar()
    df = filt(df_raw, cat, wh)
    r   = run_sql(df, SQL["Q1"]).iloc[0]
    n   = int(r["n"])
    rev = float(r["rev"] or 0)
    ld  = float(r["lead"] or 0)
    dy  = int(r["dly"])
    dv  = int(r["dlvd"])
    aq  = float(r["aq"] or 0)
    rs  = f"₹{rev/100000:.1f}L" if rev >= 100000 else f"₹{rev:,.0f}"
    dp  = dy / n * 100 if n else 0
    dp2 = dv / n * 100 if n else 0
    st.markdown('<div class="kpi-grid">' +
        kpi("TOTAL ORDERS",   str(n),        "filtered records",        "📦", "kb")  +
        kpi("REVENUE",        rs,             "final cost INR",          "📈", "kg")  +
        kpi("AVG LEAD TIME",  f"{ld:.1f}d",  "order → delivery",        "⏱", "kc2") +
        kpi("DELAYED ORDERS", str(dy),        f"{dp:.0f}% delay rate",   "⚠", "kr")  +
        kpi("DELIVERED",      f"{dp2:.0f}%",  f"{dv} orders",            "✅", "kp")  +
        kpi("AVG QUALITY",    f"{aq:.2f}",    "rating / 5.0",            "⭐", "ky")  +
        '</div>', unsafe_allow_html=True)
    # Q2 Monthly Orders Trend | Q3 Donut
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(cw("Monthly Orders Trend", "📅"), unsafe_allow_html=True)
        mo = run_sql(df, SQL["Q2"])
        mo["lbl"] = mo["m"].apply(fmt)
        fig = go.Figure()
        glow(fig, mo["lbl"], mo["n"], "#818cf8", "Orders", fill=True, show_leg=False)
        base_line(fig, 290, 30, show_legend=False)
        fig.update_xaxes(**xax(), **spike_ax())
        fig.update_yaxes(**yax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(cw("Order Status Split", "🍩"), unsafe_allow_html=True)
        sc = run_sql(df, SQL["Q3"])
        cols = [SC.get(s, "#6b7280") for s in sc["s"]]
        fig = go.Figure(go.Pie(
            labels=sc["s"], values=sc["n"], hole=0.55,
            marker=dict(colors=cols, line=dict(color=BG, width=3)),
            textposition="none",
            hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        base_pie(fig, 290, 30)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    # Q4 Revenue by Category | Q5 Monthly Revenue
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(cw("Revenue by Category (₹K)", "💰"), unsafe_allow_html=True)
        rc = run_sql(df, SQL["Q4"])
        fig = go.Figure(go.Bar(
            x=rc["c"], y=rc["rev"],
            marker=dict(color=C5[:len(rc)], opacity=0.9, line=dict(width=0)),
            text=rc["rev"].apply(lambda v: f"₹{v:.0f}K"),
            textposition="outside", textfont=dict(size=9, color=TEXT),
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        base_bar(fig, 290, 55, show_legend=False)
        fig.update_layout(bargap=0.3)
        fig.update_xaxes(**xax())
        fig.update_yaxes(**yax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(cw("Monthly Revenue (₹K)", "📈"), unsafe_allow_html=True)
        rm = run_sql(df, SQL["Q5"])
        rm["lbl"] = rm["m"].apply(fmt)
        fig = go.Figure()
        glow(fig, rm["lbl"], rm["rev"], "#06b6d4", "Revenue (₹K)", fill=True, show_leg=False)
        base_line(fig, 290, 30, show_legend=False)
        fig.update_xaxes(**xax(), **spike_ax())
        fig.update_yaxes(**yax())
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DELIVERY
# ══════════════════════════════════════════════════════════════════════════════
def page_delivery():
    st.markdown('<div class="pt"><span class="ptb"></span>Delivery Analytics</div>',
                unsafe_allow_html=True)
    cat, wh = filter_bar()
    df = filt(df_raw, cat, wh)
    vm  = df["Order_Status"].value_counts()
    ot  = df[df["Delay_Days"] == 0].shape[0]
    ddf = df[df["Delay_Days"] > 0]
    ad  = ddf["Delay_Days"].mean() if len(ddf) else 0
    st.markdown('<div class="kpi-grid">') +
        kpi("ON-TIME",    str(ot),                     "no delays",            "✅", "kg")  +
        kpi("AVG DELAY",  f"{ad:.1f}d",                "among delayed",        "⚠", "kr")  +
        kpi("DELIVERED",  str(vm.get("Delivered", 0)), "completed",            "📦", "kb")  +
        kpi("IN TRANSIT", str(vm.get("In Transit", 0)),"moving",              "🚚", "kc2") +

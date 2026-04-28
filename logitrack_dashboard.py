# ============================================================
#  LogiTrack Pro — Supply Chain Analytics Dashboard
#  Author  : Manish Patil
#  Stack   : Python · Streamlit · Plotly · SQLite · Pandas
#  Dataset : supply_chain_2024_25.csv  (200 rows, 24 cols)
#  Run     : streamlit run logitrack_dashboard.py
# ============================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="LogiTrack Pro · Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS: Dark theme + Glow KPI cards ─────────────────────────
st.markdown("""
<style>
.stApp { background-color: #030312; color: #e2e8f0; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060618 0%, #04040f 100%);
    border-right: 1px solid rgba(129,140,248,0.1);
}
header[data-testid="stHeader"] { display: none; }
[data-baseweb="tag"] {
    background-color: rgba(99,102,241,0.2) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
}
.stButton>button {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(129,140,248,0.15);
    color: #64748b;
    border-radius: 10px;
    width: 100%;
    transition: all 0.15s;
}
.stButton>button:hover {
    background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.4);
    color: #a5b4fc;
}
.active-btn>button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.45) !important;
}
.kpi-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border-radius: 16px;
    padding: 18px 16px;
    margin-bottom: 6px;
    position: relative;
    overflow: hidden;
}
hr { border-color: rgba(129,140,248,0.1); }
footer { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Data Load ─────────────────────────────────────────────────
@st.cache_resource
def load_data():
    df = pd.read_csv("supply_chain_2024_25.csv")
    conn = sqlite3.connect(":memory:")
    df.to_sql("sc", conn, index=False, if_exists="replace")
    return df, conn

df, conn = load_data()

# ── Color maps ────────────────────────────────────────────────
STATUS_COLORS = {
    "Delivered":  "#10b981",
    "In Transit": "#3b82f6",
    "Delayed":    "#f43f5e",
    "Cancelled":  "#6b7280",
    "Pending":    "#f59e0b"
}
PALETTE = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899","#f43f5e","#a78bfa","#22d3ee"]

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#94a3b8",
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
)

# ── Helper: KPI Glow Card ─────────────────────────────────────
def kpi_card(label, value, sub, glow):
    st.markdown(f"""
    <div class="kpi-card" style="border:1px solid {glow}30;
         box-shadow:0 0 32px {glow}18, 0 4px 20px rgba(0,0,0,0.5);">
      <div style="position:absolute;top:-20px;right:-20px;width:70px;height:70px;
           border-radius:50%;background:radial-gradient(circle,{glow}30,transparent 70%);"></div>
      <div style="font-size:9px;color:#475569;text-transform:uppercase;
           letter-spacing:0.12em;font-weight:700;margin-bottom:10px;">{label}</div>
      <div style="font-size:28px;font-weight:900;color:#f8fafc;line-height:1;">{value}</div>
      <div style="font-size:11px;color:#475569;margin-top:6px;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Helper: Page Header ───────────────────────────────────────
def page_header(icon, title):
    st.markdown(f"""
    <h1 style="font-size:22px;font-weight:900;margin:0 0 18px;
        background:linear-gradient(135deg,#c7d2fe 0%,#a5f3fc 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      {icon} {title}
    </h1>
    """, unsafe_allow_html=True)

# ── Session state: page ───────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "overview"

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding-bottom:20px;margin-bottom:16px;
         border-bottom:1px solid rgba(129,140,248,0.1);">
      <div style="width:64px;height:64px;margin:0 auto 12px;
           filter:drop-shadow(0 0 18px rgba(99,102,241,0.7));">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" width="64" height="64">
          <defs>
            <linearGradient id="topF" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#a5b4fc"/><stop offset="100%" stop-color="#818cf8"/>
            </linearGradient>
            <linearGradient id="leftF" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#3730a3"/>
            </linearGradient>
            <linearGradient id="rightF" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#06b6d4"/><stop offset="100%" stop-color="#0284c7"/>
            </linearGradient>
          </defs>
          <polygon points="32,6 56,19 32,32 8,19" fill="url(#topF)" opacity="0.95"/>
          <polygon points="8,19 32,32 32,57 8,44" fill="url(#leftF)"/>
          <polygon points="32,32 56,19 56,44 32,57" fill="url(#rightF)"/>
        </svg>
      </div>
      <div style="font-weight:900;font-size:16px;
           background:linear-gradient(120deg,#c7d2fe 0%,#a5f3fc 100%);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;">LogiTrack</div>
      <div style="font-size:9px;color:#4f46e5;font-weight:800;
           letter-spacing:0.18em;text-transform:uppercase;margin-top:2px;">PRO</div>
    </div>
    """, unsafe_allow_html=True)

    PAGES = [
        ("overview",  "📊  Overview"),
        ("delivery",  "🚚  Delivery"),
        ("cost",      "💰  Cost & Revenue"),
        ("supplier",  "🏆  Suppliers"),
        ("warehouse", "🏭  Warehouse"),
    ]
    for pid, plabel in PAGES:
        active = st.session_state.page == pid
        if active:
            st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button(plabel, key=f"nav_{pid}"):
            st.session_state.page = pid
            st.rerun()
        if active:
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "overview":
    page_header("📊", "Supply Chain Overview")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_sel = st.multiselect("📁 Category", sorted(df["Category"].unique()), default=list(df["Category"].unique()))
    with col_f2:
        wh_sel = st.multiselect("🏭 Warehouse", sorted(df["Warehouse"].unique()), default=list(df["Warehouse"].unique()))

    d = df[df["Category"].isin(cat_sel) & df["Warehouse"].isin(wh_sel)]
    conn_f = sqlite3.connect(":memory:")
    d.to_sql("sc", conn_f, index=False, if_exists="replace")

    kpi = pd.read_sql("""
        SELECT COUNT(*) AS n,
               ROUND(SUM(Final_Cost_INR)/100000,2) AS rev_lakhs,
               ROUND(AVG(Lead_Time_Days),1) AS avg_lead,
               SUM(CASE WHEN Order_Status='Delayed'   THEN 1 ELSE 0 END) AS delayed,
               SUM(CASE WHEN Order_Status='Delivered' THEN 1 ELSE 0 END) AS delivered,
               ROUND(AVG(CASE WHEN Quality_Rating IS NOT NULL
                         THEN CAST(Quality_Rating AS FLOAT) END),2) AS avg_q
        FROM sc
    """, conn_f).iloc[0]
    n = int(kpi["n"])

    st.markdown("---")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: kpi_card("Total Orders",  str(n), "filtered records", "#818cf8")
    with c2: kpi_card("Revenue", f"₹{kpi['rev_lakhs']}L", "final cost INR", "#06b6d4")
    with c3: kpi_card("Avg Lead Time", f"{kpi['avg_lead']}d", "order to delivery", "#10b981")
    with c4: kpi_card("Delayed", str(int(kpi['delayed'])), f"{round(kpi['delayed']/n*100) if n else 0}% rate", "#f43f5e")
    with c5: kpi_card("Delivered", f"{round(kpi['delivered']/n*100) if n else 0}%", f"{int(kpi['delivered'])} orders", "#10b981")
    with c6: kpi_card("Avg Quality", str(kpi['avg_q']) if kpi['avg_q'] else "N/A", "rating / 5.0", "#f59e0b")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        monthly = pd.read_sql("SELECT SUBSTR(Order_Date,1,7) AS month, COUNT(*) AS orders, ROUND(SUM(Final_Cost_INR)/1000,1) AS revenue FROM sc GROUP BY month ORDER BY month", conn_f)
        fig = px.area(monthly, x="month", y="orders", title="📅 Monthly Orders Trend", color_discrete_sequence=["#818cf8"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(129,140,248,0.15)", line_width=2.5)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        by_stat = pd.read_sql("SELECT Order_Status, COUNT(*) AS cnt FROM sc GROUP BY Order_Status", conn_f)
        fig = px.pie(by_stat, names="Order_Status", values="cnt", title="🥧 Order Status Split", hole=0.55, color="Order_Status", color_discrete_map=STATUS_COLORS)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        by_cat = pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev_k FROM sc GROUP BY Category ORDER BY rev_k DESC", conn_f)
        fig = px.bar(by_cat, x="Category", y="rev_k", title="💰 Revenue by Category (₹K)", color="Category", color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch4:
        monthly = pd.read_sql("SELECT SUBSTR(Order_Date,1,7) AS month, ROUND(SUM(Final_Cost_INR)/1000,1) AS revenue FROM sc GROUP BY month ORDER BY month", conn_f)
        fig = px.area(monthly, x="month", y="revenue", title="📈 Monthly Revenue (₹K)", color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(6,182,212,0.15)", line_width=2.5)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    conn_f.close()

# ══════════════════════════════════════════════════════════════
#  PAGE: DELIVERY
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "delivery":
    page_header("🚚", "Delivery Performance & Delays")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        stat_sel = st.multiselect("📋 Status", sorted(df["Order_Status"].unique()), default=list(df["Order_Status"].unique()))
    with col_f2:
        ship_sel = st.multiselect("🚚 Shipping Mode", sorted(df["Shipping_Mode"].unique()), default=list(df["Shipping_Mode"].unique()))
    with col_f3:
        max_dly = int(df["Delay_Days"].fillna(0).max())
        dly_max = st.slider("⏱️ Max Delay Days", 0, max_dly, max_dly)

    d = df[df["Order_Status"].isin(stat_sel) & df["Shipping_Mode"].isin(ship_sel) & (df["Delay_Days"].fillna(0) <= dly_max)]
    conn_f = sqlite3.connect(":memory:")
    d.to_sql("sc", conn_f, index=False, if_exists="replace")

    kpi = pd.read_sql("SELECT COUNT(*) AS n, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS delayed, SUM(CASE WHEN Order_Status='Delivered' THEN 1 ELSE 0 END) AS delivered, SUM(CASE WHEN Order_Status='Cancelled' THEN 1 ELSE 0 END) AS cancelled, ROUND(AVG(Lead_Time_Days),1) AS avg_lead FROM sc", conn_f).iloc[0]
    n = int(kpi["n"])

    st.markdown("---")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Total Orders", str(n), "in filter", "#818cf8")
    with c2: kpi_card("Delayed", str(int(kpi["delayed"])), f"{round(kpi['delayed']/n*100,1) if n else 0}% rate", "#f43f5e")
    with c3: kpi_card("Delivered", str(int(kpi["delivered"])), f"{round(kpi['delivered']/n*100,1) if n else 0}% rate", "#10b981")
    with c4: kpi_card("Avg Lead Time", f"{kpi['avg_lead']}d", "order to delivery", "#06b6d4")
    with c5: kpi_card("Cancelled", str(int(kpi["cancelled"])), "orders cancelled", "#6b7280")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        sd = pd.read_sql("SELECT Shipping_Mode, ROUND(100.0*SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END)/COUNT(*),1) AS delay_rate FROM sc GROUP BY Shipping_Mode", conn_f)
        fig = px.bar(sd, x="Shipping_Mode", y="delay_rate", title="🚚 Delay Rate by Shipping Mode (%)", color_discrete_sequence=["#f43f5e"])
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        md = pd.read_sql("SELECT SUBSTR(Order_Date,1,7) AS month, COUNT(*) AS orders, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS delayed FROM sc GROUP BY month ORDER BY month", conn_f)
        fig = go.Figure()
        fig.add_bar(x=md["month"], y=md["orders"], name="Total Orders", marker_color="rgba(129,140,248,0.25)")
        fig.add_bar(x=md["month"], y=md["delayed"], name="Delayed", marker_color="#f43f5e")
        fig.update_layout(barmode="overlay", title="📅 Monthly Orders vs Delays", **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        lc = pd.read_sql("SELECT Category, ROUND(AVG(Lead_Time_Days),1) AS avg_lead FROM sc GROUP BY Category", conn_f)
        fig = px.bar(lc, x="Category", y="avg_lead", title="⏱️ Avg Lead Time by Category", color="Category", color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch4:
        sc_df = pd.read_sql("SELECT Category, Order_Status, COUNT(*) AS cnt FROM sc GROUP BY Category, Order_Status", conn_f)
        fig = px.bar(sc_df, x="Category", y="cnt", color="Order_Status", title="📊 Status by Category", color_discrete_map=STATUS_COLORS)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    conn_f.close()

# ══════════════════════════════════════════════════════════════
#  PAGE: COST & REVENUE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "cost":
    page_header("💰", "Cost & Revenue Analysis")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_sel = st.multiselect("📁 Category", sorted(df["Category"].unique()), default=list(df["Category"].unique()))
    with col_f2:
        pay_sel = st.multiselect("💳 Payment Terms", sorted(df["Payment_Terms"].unique()), default=list(df["Payment_Terms"].unique()))

    d = df[df["Category"].isin(cat_sel) & df["Payment_Terms"].isin(pay_sel)]
    conn_f = sqlite3.connect(":memory:")
    d.to_sql("sc", conn_f, index=False, if_exists="replace")

    kpi = pd.read_sql("SELECT COUNT(*) AS n, ROUND(SUM(Final_Cost_INR)/100000,2) AS rev_l, ROUND(SUM(Freight_Cost_INR)/100000,2) AS frt_l, ROUND(AVG(Discount_Pct),1) AS avg_disc, ROUND((SUM(Final_Cost_INR)-SUM(Freight_Cost_INR))/100000,2) AS margin_l FROM sc", conn_f).iloc[0]
    n = int(kpi["n"])

    st.markdown("---")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Total Revenue", f"₹{kpi['rev_l']}L", "final cost INR", "#06b6d4")
    with c2: kpi_card("Total Freight", f"₹{kpi['frt_l']}L", f"{round(kpi['frt_l']/kpi['rev_l']*100,1) if kpi['rev_l'] else 0}% of revenue", "#f43f5e")
    with c3: kpi_card("Avg Discount", f"{kpi['avg_disc']}%", "applied to orders", "#f59e0b")
    with c4: kpi_card("Net Margin", f"₹{kpi['margin_l']}L", "rev minus freight", "#10b981")
    with c5: kpi_card("Orders", str(n), "filtered", "#818cf8")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        cc = pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev_k, ROUND(SUM(Freight_Cost_INR)/1000,1) AS frt_k FROM sc GROUP BY Category ORDER BY rev_k DESC", conn_f)
        fig = go.Figure()
        fig.add_bar(x=cc["Category"], y=cc["rev_k"], name="Revenue ₹K", marker_color="#818cf8")
        fig.add_bar(x=cc["Category"], y=cc["frt_k"], name="Freight ₹K", marker_color="#f43f5e")
        fig.update_layout(barmode="group", title="💰 Revenue vs Freight (₹K)", **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        mr = pd.read_sql("SELECT SUBSTR(Order_Date,1,7) AS month, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev_k FROM sc GROUP BY month ORDER BY month", conn_f)
        fig = px.area(mr, x="month", y="rev_k", title="📈 Monthly Revenue (₹K)", color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(6,182,212,0.15)", line_width=2.5)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        sf = pd.read_sql("SELECT Shipping_Mode, ROUND(AVG(Freight_Cost_INR),0) AS avg_frt FROM sc GROUP BY Shipping_Mode", conn_f)
        fig = px.bar(sf, x="Shipping_Mode", y="avg_frt", title="🚢 Avg Freight by Mode (₹)", color_discrete_sequence=["#f59e0b"])
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch4:
        pc = pd.read_sql("SELECT Payment_Terms, COUNT(*) AS cnt FROM sc GROUP BY Payment_Terms", conn_f)
        fig = px.pie(pc, names="Payment_Terms", values="cnt", hole=0.55, title="💳 Orders by Payment Terms", color_discrete_sequence=PALETTE)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    conn_f.close()

# ══════════════════════════════════════════════════════════════
#  PAGE: SUPPLIERS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "supplier":
    page_header("🏆", "Supplier Performance")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sup_sel = st.multiselect("🏢 Supplier", sorted(df["Supplier_Name"].unique()), default=list(df["Supplier_Name"].unique()))
    with col_f2:
        city_sel = st.multiselect("📍 City", sorted(df["Supplier_City"].unique()), default=list(df["Supplier_City"].unique()))

    d = df[df["Supplier_Name"].isin(sup_sel) & df["Supplier_City"].isin(city_sel)]
    conn_f = sqlite3.connect(":memory:")
    d.to_sql("sc", conn_f, index=False, if_exists="replace")

    kpi = pd.read_sql("SELECT COUNT(*) AS n, COUNT(DISTINCT Supplier_Name) AS sup_cnt, ROUND(AVG(CAST(Quality_Rating AS FLOAT)),2) AS avg_q, SUM(CASE WHEN CAST(Quality_Rating AS FLOAT)<3 AND Quality_Rating IS NOT NULL THEN 1 ELSE 0 END) AS low_q, ROUND(AVG(Lead_Time_Days),1) AS avg_lead FROM sc", conn_f).iloc[0]

    st.markdown("---")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Suppliers", str(int(kpi["sup_cnt"])), "active", "#818cf8")
    with c2: kpi_card("Avg Quality", str(kpi["avg_q"]) if kpi["avg_q"] else "N/A", "out of 5.0", "#f59e0b")
    with c3: kpi_card("Low Quality", str(int(kpi["low_q"])), "ratings below 3", "#f43f5e")
    with c4: kpi_card("Avg Lead", f"{kpi['avg_lead']}d", "order to delivery", "#06b6d4")
    with c5: kpi_card("Total Orders", str(int(kpi["n"])), "filtered", "#10b981")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        ts = pd.read_sql("SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev_k FROM sc GROUP BY Supplier_Name ORDER BY rev_k DESC LIMIT 8", conn_f)
        fig = px.bar(ts, y="Supplier_Name", x="rev_k", orientation="h", title="🥇 Top Suppliers by Revenue (₹K)", color="Supplier_Name", color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        sq = pd.read_sql("SELECT Supplier_Name, ROUND(AVG(CAST(Quality_Rating AS FLOAT)),2) AS avg_q FROM sc WHERE Quality_Rating IS NOT NULL GROUP BY Supplier_Name ORDER BY avg_q DESC LIMIT 8", conn_f)
        fig = px.bar(sq, y="Supplier_Name", x="avg_q", orientation="h", title="⭐ Quality Rating by Supplier", color="avg_q", color_continuous_scale=["#f43f5e","#f59e0b","#10b981"], range_color=[1,5])
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        cc = pd.read_sql("SELECT Supplier_City, COUNT(*) AS cnt FROM sc GROUP BY Supplier_City", conn_f)
        fig = px.pie(cc, names="Supplier_City", values="cnt", hole=0.55, title="📍 Orders by City", color_discrete_sequence=PALETTE)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch4:
        ls = pd.read_sql("SELECT Supplier_Name, ROUND(AVG(Lead_Time_Days),1) AS avg_lead FROM sc GROUP BY Supplier_Name ORDER BY avg_lead DESC LIMIT 8", conn_f)
        fig = px.bar(ls, x="Supplier_Name", y="avg_lead", title="⏱️ Avg Lead Time by Supplier", color="Supplier_Name", color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)
    conn_f.close()

# ══════════════════════════════════════════════════════════════
#  PAGE: WAREHOUSE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "warehouse":
    page_header("🏭", "Warehouse Operations")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        wh_sel = st.multiselect("🏭 Warehouse", sorted(df["Warehouse"].unique()), default=list(df["Warehouse"].unique()))
    with col_f2:
        cat_sel = st.multiselect("📁 Category", sorted(df["Category"].unique()), default=list(df["Category"].unique()))
    with col_f3:
        ship_sel = st.multiselect("🚚 Shipping", sorted(df["Shipping_Mode"].unique()), default=list(df["Shipping_Mode"].unique()))

    d = df[df["Warehouse"].isin(wh_sel) & df["Category"].isin(cat_sel) & df["Shipping_Mode"].isin(ship_sel)]
    conn_f = sqlite3.connect(":memory:")
    d.to_sql("sc", conn_f, index=False, if_exists="replace")

    kpi = pd.read_sql("SELECT COUNT(*) AS n, COUNT(DISTINCT Warehouse) AS wh_cnt, ROUND(AVG(Quantity),1) AS avg_qty FROM sc", conn_f).iloc[0]
    top_wh   = pd.read_sql("SELECT Warehouse, COUNT(*) AS cnt FROM sc GROUP BY Warehouse ORDER BY cnt DESC LIMIT 1", conn_f).iloc[0]["Warehouse"].replace("WH-","")
    worst_wh = pd.read_sql("SELECT Warehouse, COUNT(*) AS cnt FROM sc WHERE Order_Status='Delayed' GROUP BY Warehouse ORDER BY cnt DESC LIMIT 1", conn_f)
    worst_wh = worst_wh.iloc[0]["Warehouse"].replace("WH-","") if len(worst_wh) else "N/A"

    st.markdown("---")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Warehouses",   str(int(kpi["wh_cnt"])), "active locations", "#818cf8")
    with c2: kpi_card("Total Orders", str(int(kpi["n"])),      "filtered",         "#06b6d4")
    with c3: kpi_card("Most Active",  top_wh,                  "by order count",   "#10b981")
    with c4: kpi_card("Most Delays",  worst_wh,                "by delay count",   "#f43f5e")
    with c5: kpi_card("Avg Qty",      str(kpi["avg_qty"]),     "units per order",  "#f59e0b")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        wp = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS wh, COUNT(*) AS orders, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS delayed FROM sc GROUP BY Warehouse", conn_f)
        fig = go.Figure()
        fig.add_bar(x=wp["wh"], y=wp["orders"], name="Total Orders", marker_color="rgba(129,140,248,0.25)")
        fig.add_bar(x=wp["wh"], y=wp["delayed"], name="Delayed", marker_color="#f43f5e")
        fig.update_layout(barmode="overlay", title="🏭 Orders vs Delays by Warehouse", **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        wr = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS wh, ROUND(SUM(Final_Cost_INR)/1000,1) AS rev_k FROM sc GROUP BY Warehouse", conn_f)
        fig = px.pie(wr, names="wh", values="rev_k", hole=0.55, title="💰 Revenue by Warehouse (₹K)", color_discrete_sequence=PALETTE)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    cw = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS wh, Category, COUNT(*) AS cnt FROM sc GROUP BY Warehouse, Category", conn_f)
    fig = px.bar(cw, x="wh", y="cnt", color="Category", title="📁 Category Mix by Warehouse", color_discrete_sequence=PALETTE)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    conn_f.close()

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="LogiTrack Pro · Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif !important; box-sizing: border-box; }
.stApp { background: #030312 !important; color: #e2e8f0 !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060618 0%, #04040f 100%) !important;
    border-right: 1px solid rgba(129,140,248,0.08) !important;
}
[data-testid="stSidebarContent"] { padding: 20px 12px !important; }
.block-container { padding-top: 1.8rem !important; padding-bottom: 1rem !important; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }
.viewerBadge_container__1QSob { display: none !important; }
[data-testid="stSidebarContent"] [data-testid="stButton"] > button {
    background: rgba(255,255,255,0.02) !important;
    border: none !important;
    color: #4b5563 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 12px !important;
    text-align: left !important;
    padding: 9px 12px !important;
    margin-bottom: 2px !important;
    transition: all 0.15s !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebarContent"] [data-testid="stButton"] > button:hover {
    background: rgba(129,140,248,0.08) !important;
    color: #a5b4fc !important;
}
[data-testid="stPills"] { gap: 5px !important; flex-wrap: wrap !important; }
[data-testid="stPills"] span[role="checkbox"],
[data-testid="stPills"] span[role="radio"] {
    background: transparent !important;
    border: 1px solid rgba(129,140,248,0.2) !important;
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    cursor: pointer !important;
    transition: all 0.12s !important;
    line-height: 1.4 !important;
}
[data-testid="stPills"] span[role="checkbox"][aria-checked="true"],
[data-testid="stPills"] span[role="radio"][aria-checked="true"],
[data-testid="stPills"] span[aria-selected="true"] {
    background: rgba(129,140,248,0.15) !important;
    border-color: rgba(129,140,248,0.6) !important;
    color: #a5b4fc !important;
    font-weight: 600 !important;
    box-shadow: 0 0 10px rgba(129,140,248,0.2) !important;
}
[data-testid="stPills"] label {
    font-size: 9px !important;
    color: #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 800 !important;
}
[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.025), rgba(255,255,255,0.01)) !important;
    border: 1px solid rgba(129,140,248,0.1) !important;
    border-radius: 16px !important;
    box-shadow: 0 0 24px rgba(129,140,248,0.06), 0 4px 20px rgba(0,0,0,0.5) !important;
    padding: 4px !important;
    overflow: hidden !important;
}
[data-testid="stSlider"] [role="slider"] { background: #818cf8 !important; }
hr { border-color: rgba(129,140,248,0.06) !important; margin: 14px 0 !important; }
[data-testid="stDataFrame"] > div { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stMainBlockContainer"] [data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_csv('supply_chain_2024_25.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    return df

df = load_data()

PAL = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899","#f43f5e","#a78bfa","#22d3ee"]
STATUS_CLR = {"Delivered":"#10b981","In Transit":"#3b82f6","Delayed":"#f43f5e","Cancelled":"#6b7280","Pending":"#f59e0b"}
GLOW = {
    "indigo":"#818cf8","cyan":"#06b6d4","green":"#10b981",
    "red":"#f43f5e","yellow":"#f59e0b","gray":"#6b7280","pink":"#ec4899"
}
CHART_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b", family="Inter,-apple-system,sans-serif", size=11),
    margin=dict(l=12, r=12, t=44, b=12),
    title_font=dict(color="#c7d2fe", size=13, family="Inter"),
    legend=dict(font=dict(color="#64748b", size=10), bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#475569", size=10), showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#475569", size=10), showline=False),
    hoverlabel=dict(
        bgcolor="#0a0a1f",
        bordercolor="rgba(129,140,248,0.4)",
        font=dict(color="#e2e8f0", size=12, family="Inter"),
    ),
    hovermode="x unified",
)

def kpi(icon, label, value, sub, color):
    g = GLOW.get(color, "#818cf8")
    return f"""
    <div style="flex:1 1 145px;min-width:130px;background:linear-gradient(145deg,rgba(255,255,255,0.03),rgba(255,255,255,0.01));
        border:1px solid {g}28;border-radius:18px;padding:20px 18px;position:relative;overflow:hidden;
        box-shadow:0 0 40px {g}18,0 4px 24px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05);">
      <div style="position:absolute;top:-28px;right:-28px;width:85px;height:85px;border-radius:50%;
          background:radial-gradient(circle,{g}35,transparent 70%);pointer-events:none;"></div>
      <div style="position:absolute;bottom:-20px;left:-20px;width:60px;height:60px;border-radius:50%;
          background:radial-gradient(circle,{g}15,transparent 70%);pointer-events:none;"></div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
        <span style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;">{label}</span>
        <div style="background:{g}18;border-radius:8px;padding:7px;font-size:13px;box-shadow:0 0 12px {g}30;">{icon}</div>
      </div>
      <div style="font-size:28px;font-weight:900;color:#f8fafc;line-height:1;letter-spacing:-0.02em;">{value}</div>
      <div style="font-size:11px;color:#475569;margin-top:6px;font-weight:500;">{sub}</div>
    </div>"""

def kpi_row(cards):
    return '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">' + ''.join(cards) + '</div>'

def page_header(title):
    st.markdown(f"""
    <div style="margin-bottom:18px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:6px;height:28px;background:linear-gradient(180deg,#818cf8,#4f46e5);border-radius:3px;"></div>
        <div style="font-size:24px;font-weight:900;letter-spacing:-0.02em;
            background:linear-gradient(135deg,#e2e8f0 0%,#a5b4fc 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2;">
          {title}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def filter_bar_start():
    st.markdown("""<div style="background:rgba(129,140,248,0.03);border:1px solid rgba(129,140,248,0.08);
        border-radius:14px;padding:14px 18px 10px;margin-bottom:18px;">
      <div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">
        <span style="font-size:11px;">⚡</span>
        <span style="font-size:9px;color:#818cf8;font-weight:800;text-transform:uppercase;letter-spacing:0.14em;">Filters</span>
        <div style="flex:1;height:1px;background:rgba(129,140,248,0.1);margin-left:4px;"></div>
      </div>""", unsafe_allow_html=True)

def filter_bar_end():
    st.markdown("</div>", unsafe_allow_html=True)

def safe_pills(label, options, key=None):
    all_opts = ["All"] + list(options)
    sel = st.pills(label, options=all_opts, selection_mode="multi", default=["All"], key=key)
    if not sel or "All" in sel:
        return list(options)
    return sel

def show(fig, height=280, title="", icon=""):
    if title:
        fig.update_layout(**CHART_BASE, height=height,
            title=dict(text=f"<b>{icon}  {title}</b>", x=0, pad=dict(l=6, t=4)))
    else:
        fig.update_layout(**CHART_BASE, height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

if "page" not in st.session_state:
    st.session_state.page = "overview"

CUBE_SVG = """<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" width="62" height="62">
  <defs>
    <linearGradient id="tf2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a5b4fc"/><stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
    <linearGradient id="lf2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#3730a3"/>
    </linearGradient>
    <linearGradient id="rf2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#06b6d4"/><stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
  </defs>
  <polygon points="32,6 56,19 32,32 8,19" fill="url(#tf2)" opacity="0.95"/>
  <polygon points="8,19 32,32 32,57 8,44" fill="url(#lf2)"/>
  <polygon points="32,32 56,19 56,44 32,57" fill="url(#rf2)"/>
  <polyline points="32,6 32,32 32,57" stroke="rgba(255,255,255,0.15)" stroke-width="0.5"/>
  <polyline points="8,19 56,19" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
</svg>"""

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding-bottom:20px;margin-bottom:18px;
        border-bottom:1px solid rgba(129,140,248,0.08);">
      <div style="width:62px;height:62px;margin:0 auto 12px;
          filter:drop-shadow(0 0 16px rgba(99,102,241,0.8)) drop-shadow(0 0 32px rgba(99,102,241,0.4));">
        {CUBE_SVG}
      </div>
      <div style="font-weight:900;font-size:17px;letter-spacing:-0.03em;
          background:linear-gradient(120deg,#c7d2fe 0%,#a5f3fc 100%);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">LogiTrack</div>
      <div style="font-size:9px;color:#4f46e5;font-weight:800;letter-spacing:0.2em;
          text-transform:uppercase;margin-top:3px;">PRO</div>
    </div>
    <div style="font-size:8px;color:#1e293b;text-transform:uppercase;letter-spacing:0.14em;
        font-weight:800;margin-bottom:8px;padding-left:4px;">Navigation</div>
    """, unsafe_allow_html=True)

    NAV = [
        ("📊", "Overview",       "overview"),
        ("🚚", "Delivery",       "delivery"),
        ("💰", "Cost & Revenue", "cost"),
        ("🏆", "Suppliers",      "supplier"),
        ("🏭", "Warehouse",      "warehouse"),
    ]

    for icon, label, key in NAV:
        if st.session_state.page == key:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:9px;padding:9px 12px;
                border-radius:12px;margin-bottom:2px;cursor:default;
                background:linear-gradient(135deg,#4f46e5,#7c3aed);
                box-shadow:0 4px 20px rgba(99,102,241,0.45),inset 0 1px 0 rgba(255,255,255,0.15);">
              <span style="font-size:15px;line-height:1;">{icon}</span>
              <span style="color:white;font-weight:700;font-size:13px;flex:1;">{label}</span>
              <span style="color:rgba(255,255,255,0.5);font-size:14px;">›</span>
            </div>""", unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:8px 0 4px;">
      <div style="font-size:10px;color:#1e293b;">Supply Chain Analytics</div>
      <div style="font-size:9px;color:#1e293b;margin-top:2px;">Jan 2024 – Apr 2025</div>
    </div>""", unsafe_allow_html=True)

page = st.session_state.page

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
if page == "overview":
    page_header("Supply Chain Overview")
    filter_bar_start()
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_cat = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="ov_cat")
    with fc2:
        sel_wh  = safe_pills("Warehouse", sorted(df['Warehouse'].unique().tolist()), key="ov_wh")
    filter_bar_end()

    d = df[df['Category'].isin(sel_cat) & df['Warehouse'].isin(sel_wh)]
    conn_f = sqlite3.connect(':memory:')
    d.to_sql('sc', conn_f, index=False, if_exists='replace')

    total=len(d); rev=d['Final_Cost_INR'].sum()
    avg_lead=d['Lead_Time_Days'].mean() if total else 0
    delayed=(d['Order_Status']=='Delayed').sum()
    delivered=(d['Order_Status']=='Delivered').sum()
    rate=delivered/total*100 if total else 0
    rated=d['Quality_Rating'].dropna(); avg_q=rated.mean() if len(rated) else 0

    st.markdown(kpi_row([
        kpi("📦","Total Orders", f"{total:,}",             "filtered records",                          "indigo"),
        kpi("💰","Revenue",      f"₹{rev/1e5:.1f}L",       "final cost INR",                            "cyan"),
        kpi("⏱️","Avg Lead Time",f"{avg_lead:.1f}d",        "order → delivery",                         "green"),
        kpi("🚨","Delayed",      f"{delayed:,}",           f"{delayed/total*100:.0f}% rate" if total else "0%","red"),
        kpi("✅","Delivered",    f"{rate:.0f}%",           f"{delivered} orders",                       "green"),
        kpi("⭐","Avg Quality",  f"{avg_q:.2f}" if avg_q else "N/A","rating / 5.0",                    "yellow"),
    ]), unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        mdf = pd.read_sql("SELECT Month, COUNT(*) AS Orders FROM sc GROUP BY Month ORDER BY Month", conn_f)
        fig = px.area(mdf, x="Month", y="Orders", color_discrete_sequence=["#818cf8"])
        fig.update_traces(fillcolor="rgba(129,140,248,0.12)", line=dict(width=2.5,color="#818cf8"),
            mode="lines+markers", marker=dict(size=5,color="#818cf8"),
            hovertemplate="<b>%{x}</b><br>Orders: <b>%{y}</b><extra></extra>")
        show(fig, title="Monthly Orders Trend", icon="📅")
    with c2:
        sdf = pd.read_sql("SELECT Order_Status, COUNT(*) AS Count FROM sc GROUP BY Order_Status", conn_f)
        fig = px.pie(sdf, values="Count", names="Order_Status", hole=0.52,
                     color="Order_Status", color_discrete_map=STATUS_CLR)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Order Status Split", icon="🥧")

    c3,c4 = st.columns(2)
    with c3:
        cdf = pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Category ORDER BY Rev_K DESC", conn_f)
        fig = px.bar(cdf, x="Category", y="Rev_K", color="Category", color_discrete_sequence=PAL, text="Rev_K")
        fig.update_traces(texttemplate='₹%{text:.0f}K', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=7),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig, title="Revenue by Category (₹K)", icon="💰")
    with c4:
        shdf = pd.read_sql("SELECT Shipping_Mode, COUNT(*) AS Orders FROM sc GROUP BY Shipping_Mode", conn_f)
        fig = px.pie(shdf, values="Orders", names="Shipping_Mode", hole=0.45, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Shipping Mode Share", icon="🚢")

# ── DELIVERY ──────────────────────────────────────────────────────────────────
elif page == "delivery":
    page_header("Delivery Performance")
    filter_bar_start()
    fc1,fc2,fc3 = st.columns([1.4,1.2,1])
    with fc1: sel_status = safe_pills("Status", sorted(df['Order_Status'].unique().tolist()), key="dl_stat")
    with fc2: sel_ship   = safe_pills("Shipping Mode", sorted(df['Shipping_Mode'].unique().tolist()), key="dl_ship")
    with fc3:
        delay_max = int(df['Delay_Days'].max())
        sel_delay = st.slider("Max Delay Days", 0, delay_max, delay_max, key="dl_delay")
    filter_bar_end()

    d = df[df['Order_Status'].isin(sel_status) & df['Shipping_Mode'].isin(sel_ship) & (df['Delay_Days']<=sel_delay)]
    conn_f = sqlite3.connect(':memory:')
    d.to_sql('sc', conn_f, index=False, if_exists='replace')

    total=len(d); delayed=(d['Order_Status']=='Delayed').sum()
    on_time=(d['Order_Status']=='Delivered').sum()
    delay_d=d[d['Delay_Days']>0]['Delay_Days']; avg_delay=delay_d.mean() if len(delay_d) else 0
    in_transit=(d['Order_Status']=='In Transit').sum()

    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{total:,}",            "in selection",                                  "indigo"),
        kpi("🚨","Delayed",     f"{delayed:,}",          f"{delayed/total*100:.1f}% rate" if total else "0%","red"),
        kpi("✅","Delivered",   f"{on_time:,}",          f"{on_time/total*100:.1f}% rate" if total else "0%","green"),
        kpi("⏳","Avg Delay",   f"{avg_delay:.1f}d",     "when delayed",                                  "yellow"),
        kpi("🔄","In Transit",  f"{in_transit:,}",       "pending delivery",                              "cyan"),
    ]), unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Shipping_Mode,
            ROUND(SUM(CASE WHEN Order_Status='Delayed' THEN 1.0 ELSE 0 END)*100/COUNT(*),1) AS Delay_Pct
            FROM sc GROUP BY Shipping_Mode ORDER BY Delay_Pct DESC""", conn_f)
        fig = px.bar(q, x="Shipping_Mode", y="Delay_Pct", color="Shipping_Mode",
                     color_discrete_sequence=["#f43f5e","#f59e0b","#818cf8","#06b6d4"], text="Delay_Pct")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=7),
            hovertemplate="<b>%{x}</b><br>Delay Rate: <b>%{y:.1f}%</b><extra></extra>")
        show(fig, title="Delay Rate by Shipping Mode (%)", icon="📦")
    with c2:
        q2 = pd.read_sql("""SELECT Month,
            SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed,
            COUNT(*) AS Total FROM sc GROUP BY Month ORDER BY Month""", conn_f)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=q2['Month'], y=q2['Total'], name='Total Orders',
            marker_color='rgba(129,140,248,0.2)', marker_cornerradius=4,
            hovertemplate="<b>%{x}</b><br>Total: %{y}<extra></extra>"))
        fig.add_trace(go.Bar(x=q2['Month'], y=q2['Delayed'], name='Delayed',
            marker_color='#f43f5e', marker_cornerradius=4,
            hovertemplate="<b>%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CHART_BASE, height=280, barmode='overlay',
            title=dict(text="<b>📅  Monthly Orders vs Delays</b>", x=0, pad=dict(l=6)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    c3,c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT Category, ROUND(AVG(Lead_Time_Days),1) AS Avg_Lead FROM sc GROUP BY Category", conn_f)
        fig = px.bar(q3, x="Category", y="Avg_Lead", color="Category", color_discrete_sequence=PAL, text="Avg_Lead")
        fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=7),
            hovertemplate="<b>%{x}</b><br>Avg Lead: <b>%{y:.1f} days</b><extra></extra>")
        show(fig, title="Avg Lead Time by Category", icon="⏱️")
    with c4:
        q4 = pd.read_sql("SELECT Category, Order_Status, COUNT(*) AS Count FROM sc GROUP BY Category, Order_Status", conn_f)
        fig = px.bar(q4, x="Category", y="Count", color="Order_Status",
                     color_discrete_map=STATUS_CLR, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Order Status by Category", icon="📊")

# ── COST & REVENUE ────────────────────────────────────────────────────────────
elif page == "cost":
    page_header("Cost & Revenue Analysis")
    filter_bar_start()
    fc1,fc2 = st.columns(2)
    with fc1: sel_cat2 = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="cs_cat")
    with fc2: sel_pay  = safe_pills("Payment Terms", sorted(df['Payment_Terms'].unique().tolist()), key="cs_pay")
    filter_bar_end()

    d = df[df['Category'].isin(sel_cat2) & df['Payment_Terms'].isin(sel_pay)]
    conn_f = sqlite3.connect(':memory:')
    d.to_sql('sc', conn_f, index=False, if_exists='replace')

    total=len(d); rev=d['Final_Cost_INR'].sum(); freight=d['Freight_Cost_INR'].sum()
    avg_disc=d['Discount_Pct'].mean() if total else 0
    avg_unit=d['Unit_Cost_INR'].mean() if total else 0
    net_margin=rev-freight

    st.markdown(kpi_row([
        kpi("💰","Total Revenue",f"₹{rev/1e5:.1f}L",       "final cost INR",                              "cyan"),
        kpi("🚛","Total Freight",f"₹{freight/1e5:.1f}L",   f"{freight/rev*100:.1f}% of rev" if rev else "0%","red"),
        kpi("🏷️","Avg Discount", f"{avg_disc:.1f}%",        "applied to orders",                          "yellow"),
        kpi("📈","Net Margin",   f"₹{net_margin/1e5:.1f}L","revenue minus freight",                       "green"),
        kpi("📦","Avg Unit Cost",f"₹{avg_unit:,.0f}",      "per unit",                                    "indigo"),
    ]), unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Category,
            ROUND(SUM(Final_Cost_INR)/1000,1) AS Revenue_K,
            ROUND(SUM(Freight_Cost_INR)/1000,1) AS Freight_K
            FROM sc GROUP BY Category ORDER BY Revenue_K DESC""", conn_f)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue ₹K', x=q['Category'], y=q['Revenue_K'],
            marker_color='#818cf8', marker_cornerradius=6,
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>"))
        fig.add_trace(go.Bar(name='Freight ₹K', x=q['Category'], y=q['Freight_K'],
            marker_color='#f43f5e', marker_cornerradius=6,
            hovertemplate="<b>%{x}</b><br>Freight: ₹%{y:.0f}K<extra></extra>"))
        fig.update_layout(**CHART_BASE, height=280, barmode='group',
            title=dict(text="<b>💰  Revenue vs Freight by Category (₹K)</b>", x=0, pad=dict(l=6)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with c2:
        q2 = pd.read_sql("SELECT Month, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Month ORDER BY Month", conn_f)
        fig = px.area(q2, x="Month", y="Rev_K", color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fillcolor="rgba(6,182,212,0.1)", line=dict(width=2.5,color="#06b6d4"),
            mode="lines+markers", marker=dict(size=5,color="#06b6d4"),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig, title="Monthly Revenue Trend (₹K)", icon="📈")

    c3,c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("""SELECT Shipping_Mode, ROUND(AVG(Freight_Cost_INR),0) AS Avg_Freight
            FROM sc GROUP BY Shipping_Mode ORDER BY Avg_Freight DESC""", conn_f)
        fig = px.bar(q3, x="Shipping_Mode", y="Avg_Freight", color="Shipping_Mode",
                     color_discrete_sequence=["#f59e0b","#ec4899","#818cf8","#06b6d4"], text="Avg_Freight")
        fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=7),
            hovertemplate="<b>%{x}</b><br>Avg Freight: ₹%{y:,.0f}<extra></extra>")
        show(fig, title="Avg Freight Cost by Shipping Mode", icon="🚢")
    with c4:
        pt = pd.read_sql("SELECT Payment_Terms, COUNT(*) AS Orders FROM sc GROUP BY Payment_Terms", conn_f)
        fig = px.pie(pt, values="Orders", names="Payment_Terms", hole=0.5, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Orders by Payment Terms", icon="💳")

# ── SUPPLIERS ─────────────────────────────────────────────────────────────────
elif page == "supplier":
    page_header("Supplier Performance")
    filter_bar_start()
    fc1,fc2 = st.columns(2)
    with fc1: sel_sup  = safe_pills("Supplier", sorted(df['Supplier_Name'].unique().tolist()), key="sp_sup")
    with fc2: sel_city = safe_pills("City", sorted(df['Supplier_City'].unique().tolist()), key="sp_city")
    filter_bar_end()

    d = df[df['Supplier_Name'].isin(sel_sup) & df['Supplier_City'].isin(sel_city)]
    conn_f = sqlite3.connect(':memory:')
    d.to_sql('sc', conn_f, index=False, if_exists='replace')

    total=len(d); total_sup=d['Supplier_Name'].nunique()
    rated=d['Quality_Rating'].dropna(); avg_q=rated.mean() if len(rated) else 0
    low_q=(rated<3).sum() if len(rated) else 0
    avg_lead=d['Lead_Time_Days'].mean() if total else 0
    top_sup=d.groupby('Supplier_Name')['Final_Cost_INR'].sum().idxmax()[:14] if total else "N/A"

    st.markdown(kpi_row([
        kpi("🏢","Suppliers",   f"{total_sup}",             "active suppliers",  "indigo"),
        kpi("⭐","Avg Quality", f"{avg_q:.2f}" if avg_q else "N/A","rating / 5.0","yellow"),
        kpi("🔴","Low Quality", f"{low_q}",                 "ratings below 3.0", "red"),
        kpi("⏱️","Avg Lead",    f"{avg_lead:.1f}d",          "order to delivery", "cyan"),
        kpi("🥇","Top Supplier",top_sup,                    "by revenue",         "green"),
    ]), unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Supplier_Name ORDER BY Rev_K DESC LIMIT 8""", conn_f)
        fig = px.bar(q, x="Rev_K", y="Supplier_Name", orientation='h',
                     color="Rev_K", color_continuous_scale=["#3730a3","#818cf8","#a5b4fc"], text="Rev_K")
        fig.update_traces(texttemplate='₹%{text:.0f}K', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=6),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:.0f}K<extra></extra>")
        fig.update_coloraxes(showscale=False)
        show(fig, height=300, title="Top 8 Suppliers by Revenue (₹K)", icon="🥇")
    with c2:
        q2 = pd.read_sql("""SELECT Supplier_Name, ROUND(AVG(Quality_Rating),2) AS Avg_Q
            FROM sc WHERE Quality_Rating IS NOT NULL
            GROUP BY Supplier_Name ORDER BY Avg_Q DESC LIMIT 8""", conn_f)
        if len(q2):
            fig = px.bar(q2, x="Avg_Q", y="Supplier_Name", orientation='h', text="Avg_Q",
                         color="Avg_Q", color_continuous_scale=["#f43f5e","#f59e0b","#10b981"], range_color=[1,5])
            fig.update_traces(texttemplate='%{text:.2f} ★', textposition='outside',
                marker_line_width=0, marker=dict(cornerradius=6),
                hovertemplate="<b>%{y}</b><br>Quality: %{x:.2f} / 5.0<extra></extra>")
            fig.update_coloraxes(showscale=False)
            show(fig, height=300, title="Quality Rating by Supplier", icon="⭐")

    c3,c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT Supplier_City, COUNT(*) AS Orders FROM sc GROUP BY Supplier_City ORDER BY Orders DESC", conn_f)
        fig = px.pie(q3, values="Orders", names="Supplier_City", hole=0.45, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Orders by Supplier City", icon="📍")
    with c4:
        q4 = pd.read_sql("""SELECT Supplier_Name, ROUND(AVG(Lead_Time_Days),1) AS Avg_Lead
            FROM sc GROUP BY Supplier_Name ORDER BY Avg_Lead ASC LIMIT 8""", conn_f)
        fig = px.bar(q4, x="Supplier_Name", y="Avg_Lead",
                     color="Avg_Lead", color_continuous_scale=["#10b981","#f59e0b","#f43f5e"], text="Avg_Lead")
        fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=7),
            hovertemplate="<b>%{x}</b><br>Avg Lead: %{y:.1f} days<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=20, tickfont=dict(size=9))
        show(fig, title="Avg Lead Time by Supplier", icon="⏱️")

# ── WAREHOUSE ─────────────────────────────────────────────────────────────────
elif page == "warehouse":
    page_header("Warehouse Operations")
    filter_bar_start()
    fc1,fc2,fc3 = st.columns(3)
    with fc1: sel_wh2   = safe_pills("Warehouse", sorted(df['Warehouse'].unique().tolist()), key="wh_wh")
    with fc2: sel_cat3  = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="wh_cat")
    with fc3: sel_ship2 = safe_pills("Shipping", sorted(df['Shipping_Mode'].unique().tolist()), key="wh_ship")
    filter_bar_end()

    d = df[df['Warehouse'].isin(sel_wh2) & df['Category'].isin(sel_cat3) & df['Shipping_Mode'].isin(sel_ship2)]
    conn_f = sqlite3.connect(':memory:')
    d.to_sql('sc', conn_f, index=False, if_exists='replace')

    total=len(d); wh_count=d['Warehouse'].nunique()
    most_active=d['Warehouse'].value_counts().idxmax().replace("WH-","") if total else "N/A"
    delayed_wh=d[d['Order_Status']=='Delayed']['Warehouse']
    most_delay=delayed_wh.value_counts().idxmax().replace("WH-","") if len(delayed_wh) else "N/A"
    avg_qty=d['Quantity'].mean() if total else 0

    st.markdown(kpi_row([
        kpi("🏭","Warehouses",   f"{wh_count}", "active locations", "indigo"),
        kpi("📦","Total Orders", f"{total:,}",  "filtered",         "cyan"),
        kpi("🏆","Most Active",  most_active,   "by order count",   "green"),
        kpi("🚨","Most Delays",  most_delay,    "by delay count",   "red"),
        kpi("📊","Avg Qty/Order",f"{avg_qty:.1f}","units per order","yellow"),
    ]), unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT REPLACE(Warehouse,'WH-','') AS WH,
            COUNT(*) AS Orders,
            SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed
            FROM sc GROUP BY Warehouse ORDER BY Orders DESC""", conn_f)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Orders', x=q['WH'], y=q['Orders'],
            marker_color='rgba(129,140,248,0.25)', marker_cornerradius=5,
            hovertemplate="<b>WH-%{x}</b><br>Orders: %{y}<extra></extra>"))
        fig.add_trace(go.Bar(name='Delayed', x=q['WH'], y=q['Delayed'],
            marker_color='#f43f5e', marker_cornerradius=5,
            hovertemplate="<b>WH-%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CHART_BASE, height=280, barmode='group',
            title=dict(text="<b>🏭  Orders vs Delays by Warehouse</b>", x=0, pad=dict(l=6)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with c2:
        q2 = pd.read_sql("""SELECT REPLACE(Warehouse,'WH-','') AS WH,
            ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Warehouse ORDER BY Rev_K DESC""", conn_f)
        fig = px.pie(q2, values="Rev_K", names="WH", hole=0.48, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>WH-%{label}</b><br>Revenue: ₹%{value:.0f}K<br>Share: %{percent}<extra></extra>")
        show(fig, title="Revenue by Warehouse (₹K)", icon="💰")

    c3,c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, Category, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Category", conn_f)
        fig = px.bar(q3, x="WH", y="Count", color="Category", color_discrete_sequence=PAL, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>WH-%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Category Mix by Warehouse", icon="📁")
    with c4:
        q4 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, Shipping_Mode, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Shipping_Mode", conn_f)
        fig = px.bar(q4, x="WH", y="Count", color="Shipping_Mode", color_discrete_sequence=PAL, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>WH-%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Shipping Mode by Warehouse", icon="🚚")

st.markdown("""
<div style="text-align:center;color:#0f172a;font-size:10px;margin-top:28px;
    padding-top:12px;border-top:1px solid rgba(129,140,248,0.05);">
  LogiTrack Pro · Supply Chain Analytics · Jan 2024 – Apr 2025
</div>""", unsafe_allow_html=True)

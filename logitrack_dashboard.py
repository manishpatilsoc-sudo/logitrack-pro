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
[data-testid="stSidebarContent"] { padding: 24px 16px !important; }
.block-container { padding-top: 1.8rem !important; padding-bottom: 1rem !important; max-width: 100% !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }

/* Inactive nav buttons */
[data-testid="stSidebarContent"] [data-testid="stButton"] > button {
    background: rgba(255,255,255,0.02) !important;
    border: none !important;
    color: #4b5563 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 12px !important;
    text-align: left !important;
    padding: 10px 14px !important;
    margin-bottom: 3px !important;
    transition: all 0.15s !important;
    justify-content: flex-start !important;
    width: 100% !important;
}
[data-testid="stSidebarContent"] [data-testid="stButton"] > button:hover {
    background: rgba(129,140,248,0.08) !important;
    color: #a5b4fc !important;
}

/* Pills - ALL states */
div[data-testid="stPills"] { gap: 6px !important; flex-wrap: wrap !important; }
div[data-testid="stPills"] button {
    background: transparent !important;
    border: 1px solid rgba(129,140,248,0.22) !important;
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 4px 13px !important;
    border-radius: 20px !important;
    cursor: pointer !important;
    transition: all 0.12s !important;
    line-height: 1.5 !important;
}
div[data-testid="stPills"] button:hover {
    border-color: rgba(129,140,248,0.5) !important;
    color: #a5b4fc !important;
    background: rgba(129,140,248,0.08) !important;
}
div[data-testid="stPills"] button[aria-pressed="true"],
div[data-testid="stPills"] button[aria-selected="true"],
div[data-testid="stPills"] button[data-selected="true"] {
    background: rgba(129,140,248,0.18) !important;
    border-color: rgba(129,140,248,0.7) !important;
    color: #a5b4fc !important;
    font-weight: 700 !important;
    box-shadow: 0 0 12px rgba(129,140,248,0.25) !important;
}
div[data-testid="stPills"] label,
div[data-testid="stPills"] p {
    font-size: 9px !important;
    color: #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 800 !important;
    margin-bottom: 6px !important;
}

/* Chart containers - glow cards */
[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.025), rgba(255,255,255,0.01)) !important;
    border: 1px solid rgba(129,140,248,0.12) !important;
    border-radius: 16px !important;
    box-shadow: 0 0 30px rgba(129,140,248,0.08), 0 4px 24px rgba(0,0,0,0.6) !important;
    padding: 6px !important;
    overflow: hidden !important;
    margin-bottom: 4px !important;
}

/* Slider */
[data-testid="stSlider"] [role="slider"] { background: #818cf8 !important; }
[data-testid="stSlider"] [data-testid="stSliderThumb"] { background: #818cf8 !important; }

/* Divider */
hr { border-color: rgba(129,140,248,0.06) !important; margin: 14px 0 !important; }
[data-testid="stDataFrame"] > div { border-radius: 12px !important; overflow: hidden !important; }
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
CB = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b", family="Inter,-apple-system,sans-serif", size=11),
    margin=dict(l=12, r=12, t=44, b=12),
    title_font=dict(color="#c7d2fe", size=13, family="Inter", weight="bold"),
    legend=dict(font=dict(color="#64748b", size=10), bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#475569",size=10),
               showline=False, zeroline=False, title=None),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#475569",size=10),
               showline=False, zeroline=False, title=None),
    hoverlabel=dict(
        bgcolor="#08081a",
        bordercolor="rgba(129,140,248,0.5)",
        font=dict(color="#e2e8f0", size=12, family="Inter"),
    ),
    hovermode="x unified",
)

def kpi(icon, label, value, sub, color):
    g = GLOW.get(color, "#818cf8")
    return f"""
    <div style="flex:1 1 145px;min-width:130px;
        background:linear-gradient(145deg,rgba(255,255,255,0.04),rgba(255,255,255,0.01));
        border:1px solid {g}30;border-radius:18px;padding:20px 18px;
        position:relative;overflow:hidden;
        box-shadow:0 0 50px {g}22,0 4px 28px rgba(0,0,0,0.7),inset 0 1px 0 rgba(255,255,255,0.06);">
      <div style="position:absolute;top:-30px;right:-30px;width:90px;height:90px;border-radius:50%;
          background:radial-gradient(circle,{g}40,transparent 70%);pointer-events:none;"></div>
      <div style="position:absolute;bottom:-22px;left:-22px;width:65px;height:65px;border-radius:50%;
          background:radial-gradient(circle,{g}18,transparent 70%);pointer-events:none;"></div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
        <span style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;">{label}</span>
        <div style="background:{g}20;border-radius:8px;padding:7px;font-size:13px;
            box-shadow:0 0 16px {g}40;">{icon}</div>
      </div>
      <div style="font-size:28px;font-weight:900;color:#f8fafc;line-height:1;letter-spacing:-0.02em;">{value}</div>
      <div style="font-size:11px;color:#475569;margin-top:7px;font-weight:500;">{sub}</div>
    </div>"""

def kpi_row(cards):
    return '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">' + ''.join(cards) + '</div>'

def page_header(title):
    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:5px;height:30px;background:linear-gradient(180deg,#818cf8,#4f46e5);
            border-radius:3px;flex-shrink:0;"></div>
        <div style="font-size:26px;font-weight:900;letter-spacing:-0.02em;
            background:linear-gradient(135deg,#e2e8f0 0%,#a5b4fc 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2;">
          {title}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def filter_bar_start():
    st.markdown("""
    <div style="background:rgba(129,140,248,0.03);border:1px solid rgba(129,140,248,0.1);
        border-radius:14px;padding:14px 20px 12px;margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
        <span style="font-size:12px;">⚡</span>
        <span style="font-size:9px;color:#818cf8;font-weight:800;text-transform:uppercase;
            letter-spacing:0.16em;">Filters</span>
        <div style="flex:1;height:1px;background:rgba(129,140,248,0.12);margin-left:6px;"></div>
      </div>""", unsafe_allow_html=True)

def filter_bar_end():
    st.markdown("</div>", unsafe_allow_html=True)

def safe_pills(label, options, key=None):
    all_opts = ["All"] + list(options)
    sel = st.pills(label, options=all_opts, selection_mode="multi", default=["All"], key=key)
    if not sel or "All" in sel:
        return list(options)
    return sel

def show(fig, height=278, title="", icon="", yaxis_title=None):
    updates = dict(**CB, height=height)
    if title:
        updates["title"] = dict(text=f"<b>{icon}  {title}</b>", x=0, pad=dict(l=8, t=6))
    if yaxis_title is None:
        updates["yaxis"] = dict(**CB["yaxis"], title=None)
    fig.update_layout(**updates)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

if "page" not in st.session_state:
    st.session_state.page = "overview"

CUBE_SVG = """<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" width="60" height="60">
  <defs>
    <linearGradient id="tf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a5b4fc"/><stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
    <linearGradient id="lf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#3730a3"/>
    </linearGradient>
    <linearGradient id="rf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#06b6d4"/><stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
  </defs>
  <polygon points="32,6 56,19 32,32 8,19" fill="url(#tf)" opacity="0.95"/>
  <polygon points="8,19 32,32 32,57 8,44" fill="url(#lf)"/>
  <polygon points="32,32 56,19 56,44 32,57" fill="url(#rf)"/>
  <polyline points="32,6 32,57" stroke="rgba(255,255,255,0.15)" stroke-width="0.5"/>
  <polyline points="8,19 56,19" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
</svg>"""

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding-bottom:20px;margin-bottom:16px;
        border-bottom:1px solid rgba(129,140,248,0.08);">
      <div style="width:60px;height:60px;margin:0 auto 10px;
          filter:drop-shadow(0 0 18px rgba(99,102,241,0.9)) drop-shadow(0 0 36px rgba(99,102,241,0.4));">
        {CUBE_SVG}
      </div>
      <div style="font-weight:900;font-size:17px;letter-spacing:-0.03em;
          background:linear-gradient(120deg,#c7d2fe 0%,#a5f3fc 100%);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">LogiTrack</div>
      <div style="font-size:9px;color:#4f46e5;font-weight:800;letter-spacing:0.22em;
          text-transform:uppercase;margin-top:3px;">PRO</div>
    </div>
    <div style="font-size:8px;color:#1e293b;text-transform:uppercase;letter-spacing:0.14em;
        font-weight:800;margin-bottom:10px;padding-left:2px;">Navigation</div>
    """, unsafe_allow_html=True)

    NAV = [
        ("📊", "Overview",       "overview"),
        ("🚚", "Delivery",       "delivery"),
        ("💰", "Cost & Revenue", "cost"),
        ("🏆", "Suppliers",      "supplier"),
        ("🏭", "Warehouse",      "warehouse"),
    ]

    for em, label, key in NAV:
        if st.session_state.page == key:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;
                border-radius:12px;margin-bottom:3px;cursor:default;
                background:linear-gradient(135deg,#4f46e5,#7c3aed);
                box-shadow:0 4px 20px rgba(99,102,241,0.5),inset 0 1px 0 rgba(255,255,255,0.15);">
              <span style="font-size:15px;line-height:1;">{em}</span>
              <span style="color:white;font-weight:700;font-size:13px;flex:1;">{label}</span>
              <span style="color:rgba(255,255,255,0.6);font-size:16px;font-weight:300;">›</span>
            </div>""", unsafe_allow_html=True)
        else:
            if st.button(f"{em}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:6px 0;">
      <div style="font-size:10px;color:#1e293b;">Supply Chain Analytics</div>
      <div style="font-size:9px;color:#1e293b;margin-top:2px;">Jan 2024 – Apr 2025</div>
    </div>""", unsafe_allow_html=True)

page = st.session_state.page

# ══ OVERVIEW ══════════════════════════════════════════════════════════════════
if page == "overview":
    page_header("Supply Chain Overview")
    filter_bar_start()
    c1, c2 = st.columns(2)
    with c1: sel_cat = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="ov_cat")
    with c2: sel_wh  = safe_pills("Warehouse", sorted(df['Warehouse'].unique().tolist()), key="ov_wh")
    filter_bar_end()

    d = df[df['Category'].isin(sel_cat) & df['Warehouse'].isin(sel_wh)]
    con = sqlite3.connect(':memory:'); d.to_sql('sc', con, index=False, if_exists='replace')

    n=len(d); rev=d['Final_Cost_INR'].sum()
    al=d['Lead_Time_Days'].mean() if n else 0
    dl=(d['Order_Status']=='Delayed').sum(); dv=(d['Order_Status']=='Delivered').sum()
    rt=dv/n*100 if n else 0; rr=d['Quality_Rating'].dropna(); aq=rr.mean() if len(rr) else 0

    st.markdown(kpi_row([
        kpi("📦","Total Orders", f"{n:,}",           "filtered records",                        "indigo"),
        kpi("💰","Revenue",      f"₹{rev/1e5:.1f}L", "final cost INR",                          "cyan"),
        kpi("⏱️","Avg Lead Time",f"{al:.1f}d",        "order → delivery",                       "green"),
        kpi("🚨","Delayed",      f"{dl:,}",          f"{dl/n*100:.0f}% rate" if n else "0%",    "red"),
        kpi("✅","Delivered",    f"{rt:.0f}%",       f"{dv} orders",                             "green"),
        kpi("⭐","Avg Quality",  f"{aq:.2f}" if aq else "N/A","rating / 5.0",                  "yellow"),
    ]), unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        m = pd.read_sql("SELECT Month, COUNT(*) AS Orders FROM sc GROUP BY Month ORDER BY Month", con)
        fig = px.area(m, x="Month", y="Orders", color_discrete_sequence=["#818cf8"])
        fig.update_traces(fillcolor="rgba(129,140,248,0.12)", line=dict(width=2.5,color="#818cf8"),
            mode="lines+markers", marker=dict(size=5,color="#818cf8",line=dict(color="#c7d2fe",width=1)),
            hovertemplate="<b>%{x}</b><br>Orders: <b>%{y}</b><extra></extra>")
        show(fig, title="Monthly Orders Trend", icon="📅")
    with r1c2:
        s = pd.read_sql("SELECT Order_Status, COUNT(*) AS Count FROM sc GROUP BY Order_Status", con)
        fig = px.pie(s, values="Count", names="Order_Status", hole=0.52,
                     color="Order_Status", color_discrete_map=STATUS_CLR)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Order Status Split", icon="🥧")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        c = pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev FROM sc GROUP BY Category ORDER BY Rev DESC", con)
        fig = px.bar(c, x="Category", y="Rev", color="Category", color_discrete_sequence=PAL, text="Rev")
        fig.update_traces(texttemplate='₹%{text:.0f}K', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig, title="Revenue by Category (₹K)", icon="💰")
    with r2c2:
        sh = pd.read_sql("SELECT Shipping_Mode, COUNT(*) AS Orders FROM sc GROUP BY Shipping_Mode", con)
        fig = px.pie(sh, values="Orders", names="Shipping_Mode", hole=0.45, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Shipping Mode Share", icon="🚢")

# ══ DELIVERY ══════════════════════════════════════════════════════════════════
elif page == "delivery":
    page_header("Delivery Performance")
    filter_bar_start()
    fc1, fc2, fc3 = st.columns([1.4,1.2,1])
    with fc1: sel_s = safe_pills("Status", sorted(df['Order_Status'].unique().tolist()), key="dl_s")
    with fc2: sel_m = safe_pills("Shipping Mode", sorted(df['Shipping_Mode'].unique().tolist()), key="dl_m")
    with fc3:
        dmax = int(df['Delay_Days'].max())
        sdel = st.slider("Max Delay Days", 0, dmax, dmax, key="dl_d")
    filter_bar_end()

    d = df[df['Order_Status'].isin(sel_s) & df['Shipping_Mode'].isin(sel_m) & (df['Delay_Days']<=sdel)]
    con = sqlite3.connect(':memory:'); d.to_sql('sc', con, index=False, if_exists='replace')

    n=len(d); dl=(d['Order_Status']=='Delayed').sum(); dv=(d['Order_Status']=='Delivered').sum()
    dd=d[d['Delay_Days']>0]['Delay_Days']; ad=dd.mean() if len(dd) else 0
    it=(d['Order_Status']=='In Transit').sum()

    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{n:,}",           "in selection",                              "indigo"),
        kpi("🚨","Delayed",     f"{dl:,}",          f"{dl/n*100:.1f}% rate" if n else "0%",      "red"),
        kpi("✅","Delivered",   f"{dv:,}",          f"{dv/n*100:.1f}% rate" if n else "0%",      "green"),
        kpi("⏳","Avg Delay",   f"{ad:.1f}d",       "when delayed",                              "yellow"),
        kpi("🔄","In Transit",  f"{it:,}",          "pending delivery",                          "cyan"),
    ]), unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        q = pd.read_sql("""SELECT Shipping_Mode,
            ROUND(SUM(CASE WHEN Order_Status='Delayed' THEN 1.0 ELSE 0 END)*100/COUNT(*),1) AS Pct
            FROM sc GROUP BY Shipping_Mode ORDER BY Pct DESC""", con)
        fig = px.bar(q, x="Shipping_Mode", y="Pct", color="Shipping_Mode",
                     color_discrete_sequence=["#f43f5e","#f59e0b","#818cf8","#06b6d4"], text="Pct")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Delay Rate: <b>%{y:.1f}%</b><extra></extra>")
        show(fig, title="Delay Rate by Shipping Mode (%)", icon="📦")
    with r1c2:
        q2 = pd.read_sql("""SELECT Month,
            SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed,
            COUNT(*) AS Total FROM sc GROUP BY Month ORDER BY Month""", con)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=q2['Month'], y=q2['Total'], name='Total Orders',
            marker_color='rgba(129,140,248,0.22)', marker_cornerradius=4,
            hovertemplate="<b>%{x}</b><br>Total: %{y}<extra></extra>"))
        fig.add_trace(go.Bar(x=q2['Month'], y=q2['Delayed'], name='Delayed',
            marker_color='#f43f5e', marker_cornerradius=4,
            hovertemplate="<b>%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CB, height=278, barmode='overlay',
            title=dict(text="<b>📅  Monthly Orders vs Delays</b>", x=0, pad=dict(l=8)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        q3 = pd.read_sql("SELECT Category, ROUND(AVG(Lead_Time_Days),1) AS Lead FROM sc GROUP BY Category", con)
        fig = px.bar(q3, x="Category", y="Lead", color="Category", color_discrete_sequence=PAL, text="Lead")
        fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Avg Lead: <b>%{y:.1f} days</b><extra></extra>")
        show(fig, title="Avg Lead Time by Category (days)", icon="⏱️")
    with r2c2:
        q4 = pd.read_sql("SELECT Category, Order_Status, COUNT(*) AS Count FROM sc GROUP BY Category, Order_Status", con)
        fig = px.bar(q4, x="Category", y="Count", color="Order_Status",
                     color_discrete_map=STATUS_CLR, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Order Status by Category", icon="📊")

# ══ COST & REVENUE ════════════════════════════════════════════════════════════
elif page == "cost":
    page_header("Cost & Revenue Analysis")
    filter_bar_start()
    fc1, fc2 = st.columns(2)
    with fc1: sel_c = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="cs_c")
    with fc2: sel_p = safe_pills("Payment Terms", sorted(df['Payment_Terms'].unique().tolist()), key="cs_p")
    filter_bar_end()

    d = df[df['Category'].isin(sel_c) & df['Payment_Terms'].isin(sel_p)]
    con = sqlite3.connect(':memory:'); d.to_sql('sc', con, index=False, if_exists='replace')

    n=len(d); rv=d['Final_Cost_INR'].sum(); fr=d['Freight_Cost_INR'].sum()
    ad=d['Discount_Pct'].mean() if n else 0
    au=d['Unit_Cost_INR'].mean() if n else 0
    nm=rv-fr

    st.markdown(kpi_row([
        kpi("💰","Total Revenue",f"₹{rv/1e5:.1f}L",      "final cost INR",                            "cyan"),
        kpi("🚛","Total Freight",f"₹{fr/1e5:.1f}L",      f"{fr/rv*100:.1f}% of rev" if rv else "0%", "red"),
        kpi("🏷️","Avg Discount", f"{ad:.1f}%",           "applied to orders",                         "yellow"),
        kpi("📈","Net Margin",   f"₹{nm/1e5:.1f}L",      "revenue minus freight",                     "green"),
        kpi("📦","Avg Unit Cost",f"₹{au:,.0f}",          "per unit",                                  "indigo"),
    ]), unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        q = pd.read_sql("""SELECT Category,
            ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev,
            ROUND(SUM(Freight_Cost_INR)/1000,1) AS Frt
            FROM sc GROUP BY Category ORDER BY Rev DESC""", con)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue ₹K', x=q['Category'], y=q['Rev'],
            marker_color='#818cf8', marker_cornerradius=7,
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>"))
        fig.add_trace(go.Bar(name='Freight ₹K', x=q['Category'], y=q['Frt'],
            marker_color='#f43f5e', marker_cornerradius=7,
            hovertemplate="<b>%{x}</b><br>Freight: ₹%{y:.0f}K<extra></extra>"))
        fig.update_layout(**CB, height=278, barmode='group',
            title=dict(text="<b>💰  Revenue vs Freight (₹K)</b>", x=0, pad=dict(l=8)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with r1c2:
        q2 = pd.read_sql("SELECT Month, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev FROM sc GROUP BY Month ORDER BY Month", con)
        fig = px.area(q2, x="Month", y="Rev", color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fillcolor="rgba(6,182,212,0.1)", line=dict(width=2.5,color="#06b6d4"),
            mode="lines+markers", marker=dict(size=5,color="#06b6d4"),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig, title="Monthly Revenue Trend (₹K)", icon="📈")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        q3 = pd.read_sql("SELECT Shipping_Mode, ROUND(AVG(Freight_Cost_INR),0) AS Avg FROM sc GROUP BY Shipping_Mode ORDER BY Avg DESC", con)
        fig = px.bar(q3, x="Shipping_Mode", y="Avg", color="Shipping_Mode",
                     color_discrete_sequence=["#f59e0b","#ec4899","#818cf8","#06b6d4"], text="Avg")
        fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Avg Freight: ₹%{y:,.0f}<extra></extra>")
        show(fig, title="Avg Freight Cost by Shipping Mode", icon="🚢")
    with r2c2:
        pt = pd.read_sql("SELECT Payment_Terms, COUNT(*) AS Orders FROM sc GROUP BY Payment_Terms", con)
        fig = px.pie(pt, values="Orders", names="Payment_Terms", hole=0.5, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Orders by Payment Terms", icon="💳")

# ══ SUPPLIERS ═════════════════════════════════════════════════════════════════
elif page == "supplier":
    page_header("Supplier Performance")
    filter_bar_start()
    fc1, fc2 = st.columns(2)
    with fc1: sel_s = safe_pills("Supplier", sorted(df['Supplier_Name'].unique().tolist()), key="sp_s")
    with fc2: sel_c = safe_pills("City", sorted(df['Supplier_City'].unique().tolist()), key="sp_c")
    filter_bar_end()

    d = df[df['Supplier_Name'].isin(sel_s) & df['Supplier_City'].isin(sel_c)]
    con = sqlite3.connect(':memory:'); d.to_sql('sc', con, index=False, if_exists='replace')

    n=len(d); ts=d['Supplier_Name'].nunique()
    rr=d['Quality_Rating'].dropna(); aq=rr.mean() if len(rr) else 0
    lq=(rr<3).sum() if len(rr) else 0
    al=d['Lead_Time_Days'].mean() if n else 0
    tp=d.groupby('Supplier_Name')['Final_Cost_INR'].sum().idxmax()[:14] if n else "N/A"

    st.markdown(kpi_row([
        kpi("🏢","Suppliers",   f"{ts}",                  "active suppliers",   "indigo"),
        kpi("⭐","Avg Quality", f"{aq:.2f}" if aq else "N/A","rating / 5.0",   "yellow"),
        kpi("🔴","Low Quality", f"{lq}",                  "ratings below 3.0",  "red"),
        kpi("⏱️","Avg Lead",    f"{al:.1f}d",              "order to delivery",  "cyan"),
        kpi("🥇","Top Supplier",tp,                       "by revenue",          "green"),
    ]), unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        q = pd.read_sql("SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev FROM sc GROUP BY Supplier_Name ORDER BY Rev DESC LIMIT 8", con)
        fig = px.bar(q, x="Rev", y="Supplier_Name", orientation='h',
                     color="Rev", color_continuous_scale=["#3730a3","#818cf8","#a5b4fc"], text="Rev")
        fig.update_traces(texttemplate='₹%{text:.0f}K', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=6),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:.0f}K<extra></extra>")
        fig.update_coloraxes(showscale=False)
        show(fig, height=300, title="Top 8 Suppliers by Revenue (₹K)", icon="🥇")
    with r1c2:
        q2 = pd.read_sql("SELECT Supplier_Name, ROUND(AVG(Quality_Rating),2) AS Q FROM sc WHERE Quality_Rating IS NOT NULL GROUP BY Supplier_Name ORDER BY Q DESC LIMIT 8", con)
        if len(q2):
            fig = px.bar(q2, x="Q", y="Supplier_Name", orientation='h', text="Q",
                         color="Q", color_continuous_scale=["#f43f5e","#f59e0b","#10b981"], range_color=[1,5])
            fig.update_traces(texttemplate='%{text:.2f} ★', textposition='outside',
                marker_line_width=0, marker=dict(cornerradius=6),
                hovertemplate="<b>%{y}</b><br>Quality: %{x:.2f} / 5.0<extra></extra>")
            fig.update_coloraxes(showscale=False)
            show(fig, height=300, title="Quality Rating by Supplier", icon="⭐")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        q3 = pd.read_sql("SELECT Supplier_City, COUNT(*) AS Orders FROM sc GROUP BY Supplier_City ORDER BY Orders DESC", con)
        fig = px.pie(q3, values="Orders", names="Supplier_City", hole=0.45, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig, title="Orders by Supplier City", icon="📍")
    with r2c2:
        q4 = pd.read_sql("SELECT Supplier_Name, ROUND(AVG(Lead_Time_Days),1) AS Lead FROM sc GROUP BY Supplier_Name ORDER BY Lead ASC LIMIT 8", con)
        fig = px.bar(q4, x="Supplier_Name", y="Lead",
                     color="Lead", color_continuous_scale=["#10b981","#f59e0b","#f43f5e"], text="Lead")
        fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside',
            marker_line_width=0, marker=dict(cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Avg Lead: %{y:.1f} days<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=20, tickfont=dict(size=9))
        show(fig, title="Avg Lead Time by Supplier", icon="⏱️")

# ══ WAREHOUSE ═════════════════════════════════════════════════════════════════
elif page == "warehouse":
    page_header("Warehouse Operations")
    filter_bar_start()
    fc1, fc2, fc3 = st.columns(3)
    with fc1: sel_w = safe_pills("Warehouse", sorted(df['Warehouse'].unique().tolist()), key="wh_w")
    with fc2: sel_c = safe_pills("Category", sorted(df['Category'].unique().tolist()), key="wh_c")
    with fc3: sel_s = safe_pills("Shipping", sorted(df['Shipping_Mode'].unique().tolist()), key="wh_s")
    filter_bar_end()

    d = df[df['Warehouse'].isin(sel_w) & df['Category'].isin(sel_c) & df['Shipping_Mode'].isin(sel_s)]
    con = sqlite3.connect(':memory:'); d.to_sql('sc', con, index=False, if_exists='replace')

    n=len(d); wc=d['Warehouse'].nunique()
    ma=d['Warehouse'].value_counts().idxmax().replace("WH-","") if n else "N/A"
    dw=d[d['Order_Status']=='Delayed']['Warehouse']
    md=dw.value_counts().idxmax().replace("WH-","") if len(dw) else "N/A"
    aq=d['Quantity'].mean() if n else 0

    st.markdown(kpi_row([
        kpi("🏭","Warehouses",   f"{wc}",    "active locations", "indigo"),
        kpi("📦","Total Orders", f"{n:,}",   "filtered",         "cyan"),
        kpi("🏆","Most Active",  ma,         "by order count",   "green"),
        kpi("🚨","Most Delays",  md,         "by delay count",   "red"),
        kpi("📊","Avg Qty/Order",f"{aq:.1f}","units per order",  "yellow"),
    ]), unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        q = pd.read_sql("""SELECT REPLACE(Warehouse,'WH-','') AS WH,
            COUNT(*) AS Orders,
            SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed
            FROM sc GROUP BY Warehouse ORDER BY Orders DESC""", con)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Orders', x=q['WH'], y=q['Orders'],
            marker_color='rgba(129,140,248,0.25)', marker_cornerradius=5,
            hovertemplate="<b>WH-%{x}</b><br>Orders: %{y}<extra></extra>"))
        fig.add_trace(go.Bar(name='Delayed', x=q['WH'], y=q['Delayed'],
            marker_color='#f43f5e', marker_cornerradius=5,
            hovertemplate="<b>WH-%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CB, height=278, barmode='group',
            title=dict(text="<b>🏭  Orders vs Delays by Warehouse</b>", x=0, pad=dict(l=8)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with r1c2:
        q2 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev FROM sc GROUP BY Warehouse ORDER BY Rev DESC", con)
        fig = px.pie(q2, values="Rev", names="WH", hole=0.48, color_discrete_sequence=PAL)
        fig.update_traces(textfont_size=11, marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>WH-%{label}</b><br>Revenue: ₹%{value:.0f}K<br>Share: %{percent}<extra></extra>")
        show(fig, title="Revenue by Warehouse (₹K)", icon="💰")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        q3 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, Category, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Category", con)
        fig = px.bar(q3, x="WH", y="Count", color="Category", color_discrete_sequence=PAL, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>WH-%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Category Mix by Warehouse", icon="📁")
    with r2c2:
        q4 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, Shipping_Mode, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Shipping_Mode", con)
        fig = px.bar(q4, x="WH", y="Count", color="Shipping_Mode", color_discrete_sequence=PAL, barmode="stack")
        fig.update_traces(marker_line_width=0,
            hovertemplate="<b>WH-%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig, title="Shipping Mode by Warehouse", icon="🚚")

st.markdown("""
<div style="text-align:center;color:#0f172a;font-size:10px;margin-top:28px;
    padding-top:12px;border-top:1px solid rgba(129,140,248,0.05);">
  LogiTrack Pro · Supply Chain Analytics · Jan 2024 – Apr 2025
</div>""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="LogiTrack Pro · Supply Chain",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*,*::before,*::after{font-family:'Inter',-apple-system,sans-serif!important;box-sizing:border-box;}
.stApp{background:#030312!important;color:#e2e8f0!important;}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
  width:210px!important;min-width:210px!important;max-width:210px!important;
  background:linear-gradient(180deg,#060618 0%,#04040f 100%)!important;
  border-right:1px solid rgba(129,140,248,0.08)!important;}
[data-testid="stSidebarContent"]{padding:16px 10px!important;}

[data-testid="stSidebarCollapseButton"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
button[kind="header"]{display:none!important;}

.block-container{padding-top:2.2rem!important;padding-bottom:1rem!important;max-width:100%!important;}
#MainMenu,footer,[data-testid="stToolbar"],.viewerBadge_container__1QSob{display:none!important;visibility:hidden!important;}

/* ── NAV BUTTONS ── */
[data-testid="stSidebarContent"] [data-testid="stButton"]>button{
  background:rgba(255,255,255,0.02)!important;border:none!important;
  color:#4b5563!important;font-weight:500!important;font-size:12px!important;
  border-radius:10px!important;text-align:left!important;
  padding:8px 10px!important;margin-bottom:2px!important;
  width:100%!important;justify-content:flex-start!important;transition:all 0.15s!important;}
[data-testid="stSidebarContent"] [data-testid="stButton"]>button:hover{
  background:rgba(129,140,248,0.1)!important;color:#a5b4fc!important;}

/* ── PILLS – very compact ── */
[data-testid="stPills"]{gap:3px!important;flex-wrap:wrap!important;row-gap:3px!important;}
[data-testid="stPills"] span,
[data-testid="stPills"] button,
[data-testid="stPills"] span[role="checkbox"],
[data-testid="stPills"] span[role="radio"]{
  background:transparent!important;border:1px solid rgba(129,140,248,0.18)!important;
  color:#64748b!important;font-size:8px!important;font-weight:500!important;
  padding:1px 6px!important;border-radius:20px!important;cursor:pointer!important;
  transition:all 0.12s!important;line-height:1.4!important;
  min-height:0!important;height:auto!important;}
[data-testid="stPills"] span[role="checkbox"][aria-checked="true"],
[data-testid="stPills"] span[role="radio"][aria-checked="true"],
[data-testid="stPills"] span[aria-selected="true"],
[data-testid="stPills"] button[aria-selected="true"]{
  background:rgba(129,140,248,0.15)!important;
  border-color:rgba(129,140,248,0.65)!important;
  color:#a5b4fc!important;font-weight:700!important;
  box-shadow:0 0 8px rgba(129,140,248,0.2)!important;}
[data-testid="stPills"] label,
[data-testid="stPills"] p{
  font-size:7px!important;color:#2d3748!important;
  text-transform:uppercase!important;letter-spacing:0.12em!important;font-weight:800!important;
  margin-bottom:2px!important;margin-top:0!important;}

/* ── CHART CARDS – glow (overflow:hidden HATA DIYA – charts wapas aayenge) ── */
@keyframes chart-glow{
  0%,100%{box-shadow:0 0 20px rgba(129,140,248,0.08),0 0 40px rgba(129,140,248,0.04),0 6px 24px rgba(0,0,0,0.55);}
  50%{box-shadow:0 0 35px rgba(129,140,248,0.16),0 0 70px rgba(129,140,248,0.07),0 6px 24px rgba(0,0,0,0.55);}
}
[data-testid="stPlotlyChart"]>div{
  background:linear-gradient(145deg,rgba(255,255,255,0.025),rgba(255,255,255,0.008))!important;
  border:1px solid rgba(129,140,248,0.12)!important;
  border-radius:16px!important;
  animation:chart-glow 4s ease-in-out infinite!important;
  padding:2px!important;}
[data-testid="stPlotlyChart"] iframe,
[data-testid="stPlotlyChart"] .js-plotly-plot{
  border-radius:14px!important;overflow:visible!important;}

/* ── SLIDER ── */
[data-testid="stSlider"] [role="slider"]{background:#818cf8!important;}
hr{border-color:rgba(129,140,248,0.06)!important;margin:12px 0!important;}

/* ── MAIN AREA BUTTONS ── */
[data-testid="stMainBlockContainer"] [data-testid="stButton"]>button{
  background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;
  color:white!important;border:none!important;border-radius:10px!important;
  font-weight:700!important;font-size:13px!important;
  box-shadow:0 4px 20px rgba(99,102,241,0.4)!important;}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(129,140,248,0.2);border-radius:4px;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_csv("supply_chain_2024_25.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["MonthSort"]  = df["Order_Date"].dt.strftime("%Y-%m")
    df["Month"]      = df["Order_Date"].dt.strftime("%b '%y")
    return df

df = load_data()

PAL = ["#818cf8","#06b6d4","#10b981","#f59e0b","#ec4899","#f43f5e","#a78bfa","#22d3ee"]
STATUS_CLR = {
    "Delivered":"#10b981","In Transit":"#3b82f6",
    "Delayed":"#f43f5e","Cancelled":"#6b7280","Pending":"#f59e0b"
}
GLOW = {
    "indigo":"#818cf8","cyan":"#06b6d4","green":"#10b981",
    "red":"#f43f5e","yellow":"#f59e0b","gray":"#6b7280","pink":"#ec4899"
}

def chart_layout(height=300, title="", icon="", hovermode="closest"):
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        font=dict(color="#64748b", family="Inter,-apple-system,sans-serif", size=11),
        margin=dict(l=14, r=14, t=52, b=48),
        title=dict(
            text=f"<b>{icon}  {title}</b>" if title else "",
            x=0.01, y=0.97,
            font=dict(color="#c7d2fe", size=13, family="Inter"),
            pad=dict(l=0, t=0)
        ),
        legend=dict(
            font=dict(color="#94a3b8", size=8),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.0,
            xanchor="left", x=0.0,
            itemsizing="constant",
            itemwidth=24,
            tracegroupgap=2,
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(color="#475569", size=9),
            showline=False, zeroline=False,
            title_text="",
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikecolor="rgba(255,255,255,0.85)",
            spikedash="solid",
            spikethickness=1.5,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(color="#475569", size=9),
            showline=False, zeroline=False,
            title_text="",
        ),
        hoverlabel=dict(
            bgcolor="#0a0a1f",
            bordercolor="rgba(129,140,248,0.5)",
            font=dict(color="#e2e8f0", size=12, family="Inter"),
            align="left",
            namelength=-1,
        ),
        hovermode=hovermode,
        transition=dict(duration=600, easing="cubic-in-out"),
    )

def show(fig, height=300, title="", icon="", hovermode="closest", tickangle=None):
    fig.update_layout(**chart_layout(height, title, icon, hovermode))
    if tickangle is not None:
        fig.update_xaxes(tickangle=tickangle)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def kpi(icon, label, value, sub, color):
    g = GLOW.get(color, "#818cf8")
    return f"""
<div style="flex:1 1 145px;min-width:130px;position:relative;overflow:hidden;
  background:linear-gradient(145deg,rgba(255,255,255,0.035),rgba(255,255,255,0.01));
  border:1px solid {g}30;border-radius:18px;padding:20px 18px;
  box-shadow:0 0 40px {g}18,0 0 80px {g}08,0 6px 28px rgba(0,0,0,0.7),inset 0 1px 0 rgba(255,255,255,0.06);">
  <div style="position:absolute;top:-30px;right:-30px;width:90px;height:90px;border-radius:50%;
    background:radial-gradient(circle,{g}40,transparent 68%);pointer-events:none;"></div>
  <div style="position:absolute;bottom:-20px;left:-20px;width:65px;height:65px;border-radius:50%;
    background:radial-gradient(circle,{g}18,transparent 68%);pointer-events:none;"></div>
  <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;">
    <span style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.13em;font-weight:700;line-height:1.4;">{label}</span>
    <div style="background:{g}20;border:1px solid {g}30;border-radius:9px;padding:6px 7px;
      font-size:14px;line-height:1;box-shadow:0 0 14px {g}35;margin-left:8px;flex-shrink:0;">{icon}</div>
  </div>
  <div style="font-size:38px;font-weight:900;color:#f8fafc;line-height:1;letter-spacing:-0.03em;margin-bottom:6px;">{value}</div>
  <div style="font-size:11px;color:#475569;font-weight:500;">{sub}</div>
</div>"""

def kpi_row(cards):
    return '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">' + ''.join(cards) + '</div>'

def page_header(title):
    st.markdown(f"""
<div style="margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid rgba(129,140,248,0.06);">
  <div style="display:flex;align-items:center;gap:11px;">
    <div style="width:5px;height:28px;background:linear-gradient(180deg,#a5b4fc,#4f46e5);border-radius:3px;flex-shrink:0;
      box-shadow:0 0 12px rgba(129,140,248,0.6);"></div>
    <div style="font-size:24px;font-weight:900;letter-spacing:-0.025em;color:#e2e8f0;line-height:1.2;">
      {title}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

def fbar_open():
    st.markdown("""
<div style="background:rgba(129,140,248,0.03);border:1px solid rgba(129,140,248,0.1);
  border-radius:12px;padding:10px 16px 8px;margin-bottom:18px;">
  <div style="display:flex;align-items:center;gap:7px;margin-bottom:8px;">
    <span style="font-size:11px;line-height:1;">⚡</span>
    <span style="font-size:8px;color:#818cf8;font-weight:800;text-transform:uppercase;letter-spacing:0.14em;">Filters</span>
    <div style="flex:1;height:1px;background:rgba(129,140,248,0.12);margin-left:4px;"></div>
  </div>""", unsafe_allow_html=True)

def fbar_close():
    st.markdown("</div>", unsafe_allow_html=True)

def pills(label, options, key):
    opts = ["All"] + [str(o) for o in sorted(options)]
    sel = st.pills(label, options=opts, selection_mode="multi", default=["All"], key=key)
    if not sel or "All" in sel:
        return list(options)
    return sel

CUBE = """<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" width="64" height="64">
  <defs>
    <linearGradient id="gt" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#c7d2fe"/><stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
    <linearGradient id="gl" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#312e81"/>
    </linearGradient>
    <linearGradient id="gr" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0ea5e9"/><stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>
  <polygon points="32,5 57,19 32,33 7,19" fill="url(#gt)" opacity="0.97"/>
  <polygon points="7,19 32,33 32,58 7,44" fill="url(#gl)"/>
  <polygon points="32,33 57,19 57,44 32,58" fill="url(#gr)"/>
  <polyline points="32,5 32,58" stroke="rgba(255,255,255,0.12)" stroke-width="0.5"/>
  <polyline points="7,19 57,19" stroke="rgba(255,255,255,0.18)" stroke-width="0.5"/>
</svg>"""

if "page" not in st.session_state:
    st.session_state.page = "overview"

PAGES = [
    ("📊", "Overview",       "overview"),
    ("🚚", "Delivery",       "delivery"),
    ("💰", "Cost & Revenue", "cost"),
    ("🏆", "Suppliers",      "supplier"),
    ("🏭", "Warehouse",      "warehouse"),
]

with st.sidebar:
    st.markdown(f"""
<div style="text-align:center;padding-bottom:18px;margin-bottom:16px;
  border-bottom:1px solid rgba(129,140,248,0.07);">
  <div style="width:56px;height:56px;margin:0 auto 10px;
    filter:drop-shadow(0 0 16px rgba(99,102,241,0.9)) drop-shadow(0 0 32px rgba(99,102,241,0.5));">
    {CUBE}
  </div>
  <div style="font-weight:900;font-size:16px;letter-spacing:-0.03em;
    background:linear-gradient(120deg,#c7d2fe 0%,#a5f3fc 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">LogiTrack</div>
  <div style="font-size:8px;color:#4f46e5;font-weight:800;letter-spacing:0.22em;
    text-transform:uppercase;margin-top:2px;">PRO</div>
</div>
<div style="font-size:7px;color:#1e293b;text-transform:uppercase;letter-spacing:0.15em;
  font-weight:800;margin-bottom:6px;padding-left:4px;">Navigation</div>
""", unsafe_allow_html=True)

    for icon, label, key in PAGES:
        if st.session_state.page == key:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;padding:9px 11px;
  border-radius:10px;margin-bottom:3px;
  background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);
  box-shadow:0 4px 20px rgba(99,102,241,0.5),inset 0 1px 0 rgba(255,255,255,0.15);">
  <span style="font-size:14px;line-height:1;">{icon}</span>
  <span style="color:#fff;font-weight:700;font-size:12px;flex:1;">{label}</span>
  <span style="color:rgba(255,255,255,0.45);font-size:15px;font-weight:300;">›</span>
</div>""", unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown("""<hr>
<div style="text-align:center;padding:4px 0 2px;">
  <div style="font-size:9px;color:#1e293b;font-weight:500;">Supply Chain Analytics</div>
  <div style="font-size:8px;color:#0f172a;margin-top:2px;">Jan 2024 – Apr 2025</div>
</div>""", unsafe_allow_html=True)

page = st.session_state.page


# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "overview":
    page_header("Supply Chain Overview")

    fbar_open()
    c1, c2 = st.columns(2)
    with c1:
        sel_cat = pills("Category", df["Category"].unique(), "ov_cat")
    with c2:
        sel_wh  = pills("Warehouse", df["Warehouse"].unique(), "ov_wh")
    fbar_close()

    d = df[df["Category"].isin(sel_cat) & df["Warehouse"].isin(sel_wh)]
    con = sqlite3.connect(":memory:")
    d.to_sql("sc", con, index=False, if_exists="replace")

    n       = len(d)
    rev     = d["Final_Cost_INR"].sum()
    avg_lt  = d["Lead_Time_Days"].mean() if n else 0
    delayed = (d["Order_Status"] == "Delayed").sum()
    dlvrd   = (d["Order_Status"] == "Delivered").sum()
    rated   = d["Quality_Rating"].dropna()
    avg_q   = rated.mean() if len(rated) else 0

    st.markdown(kpi_row([
        kpi("📦", "TOTAL ORDERS",   f"{n:,}",                   "filtered records",                              "indigo"),
        kpi("💰", "REVENUE",        f"₹{rev/1e5:.1f}L",          "final cost INR",                                "cyan"),
        kpi("⏱️", "AVG LEAD TIME",  f"{avg_lt:.1f}d",             "order → delivery",                             "green"),
        kpi("🚨", "DELAYED ORDERS", f"{delayed:,}",              f"{delayed/n*100:.0f}% delay rate" if n else "0%","red"),
        kpi("✅", "DELIVERED",      f"{dlvrd/n*100:.0f}%",       f"{dlvrd} orders",                               "green"),
        kpi("⭐", "AVG QUALITY",    f"{avg_q:.2f}" if avg_q else "–", "rating / 5.0",                            "yellow"),
    ]), unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        mdf = pd.read_sql("""SELECT Month, MonthSort, COUNT(*) AS Orders
            FROM sc GROUP BY Month, MonthSort ORDER BY MonthSort""", con)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=mdf["Month"], y=mdf["Orders"],
            mode="lines+markers",
            line=dict(color="#818cf8", width=2.5, shape="spline"),
            marker=dict(size=5, color="#818cf8",
                        line=dict(width=2, color="#0a0a1f"), symbol="circle"),
            fill="tozeroy",
            fillcolor="rgba(129,140,248,0.16)",
            name="Orders",
            hovertemplate="<b>%{x}</b><br>Orders: <b>%{y}</b><extra></extra>",
        ))
        show(fig, height=300, title="Monthly Orders Trend", icon="📅", hovermode="x unified", tickangle=45)

    with c2:
        sdf = pd.read_sql("SELECT Order_Status, COUNT(*) AS Count FROM sc GROUP BY Order_Status", con)
        fig = px.pie(sdf, values="Count", names="Order_Status", hole=0.54,
                     color="Order_Status", color_discrete_map=STATUS_CLR)
        fig.update_traces(
            textinfo="none",
            marker=dict(line=dict(color="#030312", width=2.5)),
            hovertemplate="<b>%{label}</b><br>Orders: <b>%{value}</b><br>Share: <b>%{percent:.1%}</b><extra></extra>",
        )
        show(fig, height=300, title="Order Status Split", icon="🥧")

    c3, c4 = st.columns(2)
    with c3:
        cdf = pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Category ORDER BY Rev_K DESC", con)
        fig = px.bar(cdf, x="Category", y="Rev_K",
                     color="Category", color_discrete_sequence=PAL, text="Rev_K")
        fig.update_traces(
            texttemplate="₹%{text:.0f}K", textposition="outside",
            marker_line_width=0, marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        )
        fig.update_layout(showlegend=False)
        show(fig, height=290, title="Revenue by Category (₹K)", icon="💰", tickangle=30)

    with c4:
        mrev = pd.read_sql("""SELECT Month, MonthSort, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Month, MonthSort ORDER BY MonthSort""", con)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=mrev["Month"], y=mrev["Rev_K"],
            mode="lines+markers",
            line=dict(color="#06b6d4", width=2.5, shape="spline"),
            marker=dict(size=5, color="#06b6d4", line=dict(width=2, color="#0a0a1f")),
            fill="tozeroy", fillcolor="rgba(6,182,212,0.15)",
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        show(fig, height=290, title="Monthly Revenue (₹K)", icon="📈", hovermode="x unified", tickangle=45)


# ═══════════════════════════════════════════════════════════════════════════════
# DELIVERY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "delivery":
    page_header("Delivery Performance")

    fbar_open()
    c1, c2, c3 = st.columns([1.5, 1.5, 1])
    with c1:
        sel_stat = pills("Status",        df["Order_Status"].unique(),  "dl_stat")
    with c2:
        sel_ship = pills("Shipping Mode", df["Shipping_Mode"].unique(), "dl_ship")
    with c3:
        dmax = int(df["Delay_Days"].max())
        sel_delay = st.slider("Max Delay Days", 0, dmax, dmax, key="dl_delay")
    fbar_close()

    d = df[df["Order_Status"].isin(sel_stat) & df["Shipping_Mode"].isin(sel_ship) & (df["Delay_Days"] <= sel_delay)]
    con = sqlite3.connect(":memory:")
    d.to_sql("sc", con, index=False, if_exists="replace")

    n          = len(d)
    delayed    = (d["Order_Status"] == "Delayed").sum()
    on_time    = (d["Order_Status"] == "Delivered").sum()
    in_transit = (d["Order_Status"] == "In Transit").sum()
    dd         = d[d["Delay_Days"] > 0]["Delay_Days"]
    avg_delay  = dd.mean() if len(dd) else 0

    st.markdown(kpi_row([
        kpi("📦", "TOTAL ORDERS", f"{n:,}",                 "in selection",                                        "indigo"),
        kpi("🚨", "DELAYED",      f"{delayed:,}",            f"{delayed/n*100:.1f}% rate" if n else "0%",           "red"),
        kpi("✅", "DELIVERED",    f"{on_time:,}",            f"{on_time/n*100:.1f}% on-time" if n else "0%",        "green"),
        kpi("⏳", "AVG DELAY",    f"{avg_delay:.1f}d",        "when delayed",                                       "yellow"),
        kpi("🔄", "IN TRANSIT",   f"{in_transit:,}",          "pending delivery",                                   "cyan"),
    ]), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Shipping_Mode,
            ROUND(SUM(CASE WHEN Order_Status='Delayed' THEN 1.0 ELSE 0 END)*100/COUNT(*),1) AS Pct
            FROM sc GROUP BY Shipping_Mode ORDER BY Pct DESC""", con)
        fig = px.bar(q, x="Shipping_Mode", y="Pct", color="Shipping_Mode",
                     color_discrete_sequence=["#f43f5e","#f59e0b","#818cf8","#06b6d4"], text="Pct")
        fig.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside",
            marker_line_width=0, marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Delay Rate: <b>%{y:.1f}%</b><extra></extra>",
        )
        fig.update_layout(showlegend=False)
        show(fig, height=290, title="Delay Rate by Shipping Mode", icon="📦", tickangle=20)

    with c2:
        q2 = pd.read_sql("""SELECT Month, MonthSort,
            SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed,
            COUNT(*) AS Total FROM sc GROUP BY Month, MonthSort ORDER BY MonthSort""", con)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=q2["Month"], y=q2["Total"], name="Total",
            marker_color="rgba(129,140,248,0.22)", marker_cornerradius=5,
            hovertemplate="<b>%{x}</b><br>Total: <b>%{y}</b><extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=q2["Month"], y=q2["Delayed"], name="Delayed",
            marker_color="#f43f5e", marker_cornerradius=5,
            hovertemplate="<b>%{x}</b><br>Delayed: <b>%{y}</b><extra></extra>",
        ))
        fig.update_layout(
            **chart_layout(290, "Monthly Orders vs Delays", "📅", "x unified"),
            barmode="group"
        )
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    c3, c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT Category, ROUND(AVG(Lead_Time_Days),1) AS AvgLT FROM sc GROUP BY Category ORDER BY AvgLT", con)
        fig = px.bar(q3, x="Category", y="AvgLT", color="Category",
                     color_discrete_sequence=PAL, text="AvgLT")
        fig.update_traces(
            texttemplate="%{text:.1f}d", textposition="outside",
            marker_line_width=0, marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Avg Lead: <b>%{y:.1f} days</b><extra></extra>",
        )
        fig.update_layout(showlegend=False)
        show(fig, height=290, title="Avg Lead Time by Category", icon="⏱️", tickangle=30)

    with c4:
        q4 = pd.read_sql("SELECT Category, Order_Status, COUNT(*) AS Count FROM sc GROUP BY Category, Order_Status", con)
        fig = px.bar(q4, x="Category", y="Count", color="Order_Status",
                     color_discrete_map=STATUS_CLR, barmode="stack")
        fig.update_traces(
            marker_line_width=0,
            hovertemplate="<b>%{x}</b> – %{fullData.name}<br>Count: <b>%{y}</b><extra></extra>",
        )
        show(fig, height=290, title="Order Status by Category", icon="📊", tickangle=30)


# ═══════════════════════════════════════════════════════════════════════════════
# COST & REVENUE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "cost":
    page_header("Cost & Revenue Analysis")

    fbar_open()
    c1, c2 = st.columns(2)
    with c1:
        sel_cat = pills("Category",      df["Category"].unique(),      "cs_cat")
    with c2:
        sel_pay = pills("Payment Terms", df["Payment_Terms"].unique(), "cs_pay")
    fbar_close()

    d = df[df["Category"].isin(sel_cat) & df["Payment_Terms"].isin(sel_pay)]
    con = sqlite3.connect(":memory:")
    d.to_sql("sc", con, index=False, if_exists="replace")

    n        = len(d)
    rev      = d["Final_Cost_INR"].sum()
    freight  = d["Freight_Cost_INR"].sum()
    avg_disc = d["Discount_Pct"].mean() if n else 0
    avg_unit = d["Unit_Cost_INR"].mean() if n else 0

    st.markdown(kpi_row([
        kpi("💰", "TOTAL REVENUE", f"₹{rev/1e5:.1f}L",           "final cost INR",                                "cyan"),
        kpi("🚛", "TOTAL FREIGHT", f"₹{freight/1e5:.1f}L",        f"{freight/rev*100:.1f}% of rev" if rev else "–","red"),
        kpi("🏷️", "AVG DISCOUNT",  f"{avg_disc:.1f}%",             "applied to orders",                            "yellow"),
        kpi("📈", "NET MARGIN",    f"₹{(rev-freight)/1e5:.1f}L",   "revenue − freight",                            "green"),
        kpi("📦", "AVG UNIT COST", f"₹{avg_unit:,.0f}",             "per unit",                                    "indigo"),
    ]), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Category,
            ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K,
            ROUND(SUM(Freight_Cost_INR)/1000,1) AS Frgt_K
            FROM sc GROUP BY Category ORDER BY Rev_K DESC""", con)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Revenue ₹K", x=q["Category"], y=q["Rev_K"],
            marker_color="#818cf8", marker_cornerradius=7,
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        fig.add_trace(go.Bar(
            name="Freight ₹K", x=q["Category"], y=q["Frgt_K"],
            marker_color="#f43f5e", marker_cornerradius=7,
            hovertemplate="<b>%{x}</b><br>Freight: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        fig.update_layout(**chart_layout(300, "Revenue vs Freight by Category (₹K)", "💰"), barmode="group")
        fig.update_xaxes(tickangle=30, tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        q2 = pd.read_sql("""SELECT Month, MonthSort, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Month, MonthSort ORDER BY MonthSort""", con)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=q2["Month"], y=q2["Rev_K"],
            mode="lines+markers",
            line=dict(color="#06b6d4", width=2.5, shape="spline"),
            marker=dict(size=5, color="#06b6d4", line=dict(width=2, color="#0a0a1f")),
            fill="tozeroy", fillcolor="rgba(6,182,212,0.15)",
            hovertemplate="<b>%{x}</b><br>Revenue: <b>₹%{y:.0f}K</b><extra></extra>",
        ))
        show(fig, height=300, title="Monthly Revenue Trend (₹K)", icon="📈", hovermode="x unified", tickangle=45)

    c3, c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT Shipping_Mode, ROUND(AVG(Freight_Cost_INR),0) AS AvgF FROM sc GROUP BY Shipping_Mode ORDER BY AvgF DESC", con)
        fig = px.bar(q3, x="Shipping_Mode", y="AvgF", color="Shipping_Mode",
                     color_discrete_sequence=["#f59e0b","#ec4899","#818cf8","#06b6d4"], text="AvgF")
        fig.update_traces(
            texttemplate="₹%{text:,.0f}", textposition="outside",
            marker_line_width=0, marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Avg Freight: <b>₹%{y:,.0f}</b><extra></extra>",
        )
        fig.update_layout(showlegend=False)
        show(fig, height=290, title="Avg Freight by Shipping Mode", icon="🚢", tickangle=20)

    with c4:
        pt = pd.read_sql("SELECT Payment_Terms, COUNT(*) AS Orders FROM sc GROUP BY Payment_Terms", con)
        fig = px.pie(pt, values="Orders", names="Payment_Terms", hole=0.5, color_discrete_sequence=PAL)
        fig.update_traces(
            textinfo="none",
            marker=dict(line=dict(color="#030312", width=2.5)),
            hovertemplate="<b>%{label}</b><br>Orders: <b>%{value}</b><br>Share: <b>%{percent:.1%}</b><extra></extra>",
        )
        show(fig, height=290, title="Orders by Payment Terms", icon="💳")


# ═══════════════════════════════════════════════════════════════════════════════
# SUPPLIERS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "supplier":
    page_header("Supplier Performance")

    fbar_open()
    c1, c2 = st.columns(2)
    with c1:
        sel_sup  = pills("Supplier", df["Supplier_Name"].unique(), "sp_sup")
    with c2:
        sel_city = pills("City",     df["Supplier_City"].unique(), "sp_city")
    fbar_close()

    d = df[df["Supplier_Name"].isin(sel_sup) & df["Supplier_City"].isin(sel_city)]
    con = sqlite3.connect(":memory:")
    d.to_sql("sc", con, index=False, if_exists="replace")

    n        = len(d)
    n_sup    = d["Supplier_Name"].nunique()
    rated    = d["Quality_Rating"].dropna()
    avg_q    = rated.mean() if len(rated) else 0
    low_q    = (rated < 3).sum()
    avg_lt   = d["Lead_Time_Days"].mean() if n else 0
    top_sup  = d.groupby("Supplier_Name")["Final_Cost_INR"].sum().idxmax()[:14] if n else "N/A"

    st.markdown(kpi_row([
        kpi("🏢", "SUPPLIERS",    f"{n_sup}",                     "active suppliers",    "indigo"),
        kpi("⭐", "AVG QUALITY",  f"{avg_q:.2f}" if avg_q else "–", "rating / 5.0",      "yellow"),
        kpi("🔴", "LOW QUALITY",  f"{low_q}",                     "ratings below 3.0",   "red"),
        kpi("⏱️", "AVG LEAD",     f"{avg_lt:.1f}d",                "order → delivery",   "cyan"),
        kpi("🥇", "TOP SUPPLIER", top_sup,                         "by total revenue",    "green"),
    ]), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        q = pd.read_sql("""SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Supplier_Name ORDER BY Rev_K DESC LIMIT 8""", con)
        fig = px.bar(q, x="Rev_K", y="Supplier_Name", orientation="h",
                     color="Rev_K",
                     color_continuous_scale=["#312e81","#4f46e5","#818cf8","#c7d2fe"],
                     text="Rev_K")
        fig.update_traces(
            texttemplate="₹%{text:.0f}K", textposition="outside",
            marker_line_width=0, marker_cornerradius=6,
            hovertemplate="<b>%{y}</b><br>Revenue: <b>₹%{x:.0f}K</b><extra></extra>",
        )
        fig.update_coloraxes(showscale=False)
        show(fig, height=310, title="Top 8 Suppliers by Revenue", icon="🥇")

    with c2:
        q2 = pd.read_sql("""SELECT Supplier_Name, ROUND(AVG(Quality_Rating),2) AS AvgQ
            FROM sc WHERE Quality_Rating IS NOT NULL
            GROUP BY Supplier_Name ORDER BY AvgQ DESC LIMIT 8""", con)
        if len(q2):
            fig = px.bar(q2, x="AvgQ", y="Supplier_Name", orientation="h", text="AvgQ",
                         color="AvgQ", color_continuous_scale=["#f43f5e","#f59e0b","#10b981"],
                         range_color=[1, 5])
            fig.update_traces(
                texttemplate="%{text:.2f} ★", textposition="outside",
                marker_line_width=0, marker_cornerradius=6,
                hovertemplate="<b>%{y}</b><br>Quality: <b>%{x:.2f} / 5.0</b><extra></extra>",
            )
            fig.update_coloraxes(showscale=False)
            show(fig, height=310, title="Quality Rating by Supplier", icon="⭐")

    c3, c4 = st.columns(2)
    with c3:
        q3 = pd.read_sql("SELECT Supplier_City, COUNT(*) AS Orders FROM sc GROUP BY Supplier_City ORDER BY Orders DESC", con)
        fig = px.pie(q3, values="Orders", names="Supplier_City", hole=0.48, color_discrete_sequence=PAL)
        fig.update_traces(
            textinfo="none",
            marker=dict(line=dict(color="#030312", width=2.5)),
            hovertemplate="<b>%{label}</b><br>Orders: <b>%{value}</b><br>Share: <b>%{percent:.1%}</b><extra></extra>",
        )
        show(fig, height=290, title="Orders by Supplier City", icon="📍")

    with c4:
        q4 = pd.read_sql("""SELECT Supplier_Name, ROUND(AVG(Lead_Time_Days),1) AS AvgLT
            FROM sc GROUP BY Supplier_Name ORDER BY AvgLT ASC LIMIT 8""", con)
        fig = px.bar(q4, x="Supplier_Name", y="AvgLT",
                     color="AvgLT",
                     color_continuous_scale=["#10b981","#f59e0b","#f43f5e"],
                     text="AvgLT")
        fig.update_traces(
            texttemplate="%{text:.1f}d", textposition="outside",
            marker_line_width=0, marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Avg Lead: <b>%{y:.1f} days</b><extra></extra>",
        )
        fig.update_coloraxes(showscale=False)
        show(fig, height=290, title="Avg Lead Time by Supplier", icon="⏱️", tickangle=45)


# ═══════════════════════════════════════════════════════════════════════════════
# WAREHOUSE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "warehouse":
    page_header("Warehouse Operations")

    fbar_open()
    c1, c2, c3 = st.columns(3)
    with c1:
        sel_wh   = pills("Warehouse", df["Warehouse"].unique(),     "wh_wh")
    with c2:
        sel_cat  = pills("Category",  df["Category"].unique(),      "wh_cat")
    with c3:
        sel_ship = pills("Shipping",  df["Shipping_Mode"].unique(), "wh_ship")
    fbar_close()

    d = df[df["Warehouse"].isin(sel_wh) & df["Category"].isin(sel_cat) & df["Shipping_Mode"].isin(sel_ship)]
    con = sqlite3.connect(":memory:")
    d.to_sql("sc", con, index=False, if_exists="replace")

    n           = len(d)
    n_wh        = d["Warehouse"].nunique()
    most_active = d["Warehouse"].value_counts().idxmax().replace("WH-","") if n else "–"
    dl_wh       = d[d["Order_Status"] == "Delayed"]["Warehouse"]
    most_delay  = dl_wh.value_counts().idxmax().replace("WH-","") if len(dl_wh) else "–"
    avg_qty     = d["Quantity"].mean() if n else 0

    st.markdown(kpi_row([
        kpi("🏭", "WAREHOUSES",    f"{n_wh}",         "active locations",  "indigo"),
        kpi("📦", "TOTAL ORDERS",  f"{n:,}",           "filtered orders",   "cyan"),
        kpi("🏆", "MOST ACTIVE",   most_active,        "by order count",    "green"),
        kpi("🚨", "MOST DELAYS",   most_delay,         "by delay count",    "red"),
        kpi("📊", "AVG QTY/ORDER", f"{avg_qty:.1f}",   "units per order",   "yellow"),
    ]), unsafe_allow_html=True)

    q = pd.read_sql("""SELECT REPLACE(Warehouse,'WH-','') AS WH,
        COUNT(*) AS Orders,
        SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed
        FROM sc GROUP BY Warehouse ORDER BY Orders DESC""", con)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Total Orders", x=q["WH"], y=q["Orders"],
        marker_color="rgba(129,140,248,0.30)", marker_cornerradius=8,
        hovertemplate="<b>WH-%{x}</b><br>Total Orders: <b>%{y}</b><extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Delayed", x=q["WH"], y=q["Delayed"],
        marker_color="#f43f5e", marker_cornerradius=8,
        hovertemplate="<b>WH-%{x}</b><br>Delayed: <b>%{y}</b><extra></extra>",
    ))
    fig.update_layout(
        **chart_layout(300, "Orders vs Delays by Warehouse", "🏭", "closest"),
        barmode="group"
    )
    fig.update_xaxes(tickangle=30, tickfont=dict(size=10))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2)
    with c1:
        q2 = pd.read_sql("""SELECT REPLACE(Warehouse,'WH-','') AS WH,
            ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K
            FROM sc GROUP BY Warehouse ORDER BY Rev_K DESC""", con)
        fig = px.pie(q2, values="Rev_K", names="WH", hole=0.5, color_discrete_sequence=PAL)
        fig.update_traces(
            textinfo="none",
            marker=dict(line=dict(color="#030312", width=2.5)),
            hovertemplate="<b>WH-%{label}</b><br>Revenue: <b>₹%{value:.0f}K</b><br>Share: <b>%{percent:.1%}</b><extra></extra>",
        )
        show(fig, height=300, title="Revenue by Warehouse (₹K)", icon="💰")

    with c2:
        q3 = pd.read_sql("SELECT REPLACE(Warehouse,'WH-','') AS WH, Category, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Category", con)
        fig = px.bar(q3, x="WH", y="Count", color="Category",
                     color_discrete_sequence=PAL, barmode="stack")
        fig.update_traces(
            marker_line_width=0,
            hovertemplate="<b>WH-%{x}</b> – %{fullData.name}<br>Count: <b>%{y}</b><extra></extra>",
        )
        show(fig, height=300, title="Category Mix by Warehouse", icon="📁", tickangle=30)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#0f172a;font-size:10px;margin-top:28px;
  padding-top:12px;border-top:1px solid rgba(129,140,248,0.05);">
  LogiTrack Pro · Supply Chain Analytics · Jan 2024 – Apr 2025
</div>""", unsafe_allow_html=True)

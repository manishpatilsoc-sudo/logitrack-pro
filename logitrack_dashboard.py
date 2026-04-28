import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="LogiTrack Pro", page_icon="📦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{font-family:'Inter',-apple-system,sans-serif!important}
.stApp{background:#030312!important;color:#e2e8f0!important}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#060618,#04040f)!important;border-right:1px solid rgba(129,140,248,0.08)!important}
.block-container{padding-top:1.4rem!important;max-width:100%!important}
#MainMenu,footer,header{visibility:hidden!important}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] button{
  background:rgba(255,255,255,0.02)!important;border:none!important;
  color:#4b5563!important;border-radius:12px!important;
  font-size:13px!important;font-weight:500!important;margin-bottom:3px!important;
}
section[data-testid="stSidebar"] button:hover{background:rgba(129,140,248,0.1)!important;color:#a5b4fc!important}

/* Pills */
[data-testid="stPillsOption"]{
  background:transparent!important;
  border:1px solid rgba(129,140,248,0.22)!important;
  color:#475569!important;font-size:10px!important;
  border-radius:20px!important;padding:3px 11px!important;
}
[data-testid="stPillsOption"][aria-selected="true"]{
  background:rgba(129,140,248,0.18)!important;
  border-color:rgba(129,140,248,0.7)!important;
  color:#818cf8!important;font-weight:700!important;
  box-shadow:0 2px 8px rgba(129,140,248,0.25)!important;
}
[data-testid="stPills"] label{
  font-size:8px!important;color:#475569!important;
  text-transform:uppercase!important;letter-spacing:0.12em!important;font-weight:800!important;
}

/* Filter bar background */
[data-testid="stPills"]{margin-bottom:2px!important}

/* Main buttons */
.stButton>button{
  background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;
  color:white!important;border:none!important;border-radius:8px!important;font-weight:700!important;
}
hr{border:none!important;border-top:1px solid rgba(129,140,248,0.08)!important;margin:14px 0!important}

/* Slider */
[data-testid="stSlider"] [role="slider"]{background:#818cf8!important}

/* Selectbox */
div[data-baseweb="select"]>div{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(129,140,248,0.15)!important;border-radius:10px!important}
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
CHART = dict(
    template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b",family="Inter,sans-serif",size=11),
    margin=dict(l=10,r=10,t=40,b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10,color="#64748b")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10,color="#475569")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10,color="#475569")),
    hoverlabel=dict(bgcolor="#0c0c22",bordercolor="rgba(129,140,248,0.3)",font=dict(color="#e2e8f0",size=12)),
)
GLOW={"indigo":"#818cf8","cyan":"#06b6d4","green":"#10b981","red":"#f43f5e","yellow":"#f59e0b","pink":"#ec4899"}

def kpi(icon,label,value,sub,color):
    g=GLOW.get(color,"#818cf8")
    return f"""
    <div style="flex:1 1 145px;min-width:120px;
      background:linear-gradient(145deg,rgba(255,255,255,0.03),rgba(255,255,255,0.01));
      border:1px solid {g}28;border-radius:18px;padding:20px 16px;
      position:relative;overflow:hidden;
      box-shadow:0 0 40px {g}16,0 4px 24px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05);">
      <div style="position:absolute;top:-26px;right:-26px;width:78px;height:78px;border-radius:50%;
        background:radial-gradient(circle,{g}32,transparent 70%);pointer-events:none"></div>
      <div style="position:absolute;bottom:-18px;left:-18px;width:58px;height:58px;border-radius:50%;
        background:radial-gradient(circle,{g}14,transparent 70%);pointer-events:none"></div>
      <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:13px">
        <span style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;line-height:1.4">{label}</span>
        <div style="background:{g}18;border-radius:8px;padding:6px;font-size:13px;line-height:1;box-shadow:0 0 10px {g}28">{icon}</div>
      </div>
      <div style="font-size:28px;font-weight:900;color:#f8fafc;line-height:1;letter-spacing:-0.02em">{value}</div>
      <div style="font-size:11px;color:#475569;margin-top:6px">{sub}</div>
    </div>"""

def kpi_row(c): return f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;">{"".join(c)}</div>'

def pg_title(t):
    st.markdown(f'<div style="font-size:22px;font-weight:900;letter-spacing:-0.02em;margin-bottom:14px;background:linear-gradient(120deg,#c7d2fe,#a5f3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent">{t}</div>',unsafe_allow_html=True)

def fbar_label(txt):
    st.markdown(f'<div style="display:flex;align-items:center;gap:7px;margin-bottom:4px"><span style="font-size:9px;color:#818cf8;font-weight:800;text-transform:uppercase;letter-spacing:0.12em">⚡ {txt}</span><div style="flex:1;height:1px;background:rgba(129,140,248,0.1)"></div></div>',unsafe_allow_html=True)

def show(fig,h=285,title="",icon=""):
    if title:
        fig.update_layout(**CHART,height=h,
            title=dict(text=f"<b style='color:#c7d2fe'>{icon}  {title}</b>",x=0,pad=dict(l=2,t=2)))
    else:
        fig.update_layout(**CHART,height=h)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

def safe_pills(label,opts,key):
    s=st.pills(label,options=opts,selection_mode="multi",default=opts,key=key)
    return s if s else opts

if "page" not in st.session_state:
    st.session_state.page="overview"

CUBE="""<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" width="58" height="58">
<defs>
<linearGradient id="t" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#a5b4fc"/><stop offset="100%" stop-color="#818cf8"/></linearGradient>
<linearGradient id="l" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#3730a3"/></linearGradient>
<linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#06b6d4"/><stop offset="100%" stop-color="#0284c7"/></linearGradient>
</defs>
<polygon points="32,6 56,19 32,32 8,19" fill="url(#t)" opacity="0.95"/>
<polygon points="8,19 32,32 32,57 8,44" fill="url(#l)"/>
<polygon points="32,32 56,19 56,44 32,57" fill="url(#r)"/>
<polyline points="32,6 32,57" stroke="rgba(255,255,255,0.15)" stroke-width="0.5"/>
<polyline points="8,19 56,19" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
</svg>"""

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 20px;border-bottom:1px solid rgba(129,140,248,0.08);margin-bottom:16px">
      <div style="filter:drop-shadow(0 0 16px rgba(99,102,241,0.8)) drop-shadow(0 0 32px rgba(99,102,241,0.35));margin-bottom:10px">{CUBE}</div>
      <div style="font-size:17px;font-weight:900;letter-spacing:-0.03em;background:linear-gradient(120deg,#c7d2fe,#a5f3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent">LogiTrack</div>
      <div style="font-size:8px;color:#4f46e5;font-weight:800;letter-spacing:0.2em;text-transform:uppercase;margin-top:2px">PRO</div>
    </div>
    <div style="font-size:8px;color:#1e293b;text-transform:uppercase;letter-spacing:0.14em;font-weight:800;margin-bottom:10px;padding-left:4px">Navigation</div>
    """,unsafe_allow_html=True)
    for icon,label,key in [("📊","Overview","overview"),("🚚","Delivery","delivery"),("💰","Cost & Revenue","cost"),("🏆","Suppliers","supplier"),("🏭","Warehouse","warehouse")]:
        if st.session_state.page==key:
            st.markdown(f"""<div style="display:flex;align-items:center;gap:9px;padding:10px 13px;border-radius:12px;margin-bottom:3px;
              background:linear-gradient(135deg,#4f46e5,#7c3aed);
              box-shadow:0 4px 20px rgba(99,102,241,0.4),inset 0 1px 0 rgba(255,255,255,0.15)">
              <span style="font-size:15px">{icon}</span>
              <span style="color:white;font-weight:700;font-size:13px;flex:1">{label}</span>
              <span style="color:rgba(255,255,255,0.5);font-size:12px">›</span>
            </div>""",unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {label}",key=f"nav_{key}",use_container_width=True):
                st.session_state.page=key; st.rerun()

page=st.session_state.page

# ══ OVERVIEW ══════════════════════════════════════════════════════════════════
if page=="overview":
    pg_title("📊 Supply Chain Overview")
    fbar_label("Filters")
    c1,c2=st.columns(2)
    with c1: sel_cat=safe_pills("Category",sorted(df['Category'].unique().tolist()),"ov_cat")
    with c2: sel_wh=safe_pills("Warehouse",sorted(df['Warehouse'].unique().tolist()),"ov_wh")
    d=df[df['Category'].isin(sel_cat)&df['Warehouse'].isin(sel_wh)]
    conn_f=sqlite3.connect(':memory:'); d.to_sql('sc',conn_f,index=False,if_exists='replace')
    N=len(d); rev=d['Final_Cost_INR'].sum(); al=d['Lead_Time_Days'].mean() if N else 0
    dld=(d['Order_Status']=='Delayed').sum(); dlv=(d['Order_Status']=='Delivered').sum()
    rt=dlv/N*100 if N else 0; rr=d['Quality_Rating'].dropna(); aq=rr.mean() if len(rr) else 0
    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{N:,}","filtered records","indigo"),
        kpi("💰","Revenue",f"₹{rev/1e5:.1f}L","final cost INR","cyan"),
        kpi("⏱️","Avg Lead Time",f"{al:.1f}d","order → delivery","green"),
        kpi("🚨","Delayed Orders",f"{dld:,}",f"{dld/N*100:.0f}% delay rate" if N else "0%","red"),
        kpi("✅","Delivered",f"{rt:.0f}%",f"{dlv} orders","green"),
        kpi("⭐","Avg Quality",f"{aq:.2f}" if aq else "N/A","rating / 5.0","yellow"),
    ]),unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    r1,r2=st.columns(2)
    with r1:
        m=pd.read_sql("SELECT Month,COUNT(*) AS Orders FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=px.area(m,x="Month",y="Orders",color_discrete_sequence=["#818cf8"])
        fig.update_traces(fillcolor="rgba(129,140,248,0.1)",line_width=2.5,
            hovertemplate="<b>%{x}</b><br>Orders: %{y}<extra></extra>")
        show(fig,title="Monthly Orders Trend",icon="📅")
    with r2:
        s=pd.read_sql("SELECT Order_Status,COUNT(*) AS Count FROM sc GROUP BY Order_Status",conn_f)
        fig=px.pie(s,values="Count",names="Order_Status",hole=0.52,
                   color="Order_Status",color_discrete_map=STATUS_CLR)
        fig.update_traces(marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
        show(fig,title="Order Status Split",icon="🥧")
    r3,r4=st.columns(2)
    with r3:
        c=pd.read_sql("SELECT Category,ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Category ORDER BY Rev_K DESC",conn_f)
        fig=px.bar(c,x="Category",y="Rev_K",color="Category",color_discrete_sequence=PAL,text="Rev_K")
        fig.update_traces(texttemplate='₹%{text:.0f}K',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig,title="Revenue by Category (₹K)",icon="💰")
    with r4:
        sh=pd.read_sql("SELECT Shipping_Mode,COUNT(*) AS Orders FROM sc GROUP BY Shipping_Mode",conn_f)
        fig=px.pie(sh,values="Orders",names="Shipping_Mode",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>%{percent}<extra></extra>")
        show(fig,title="Shipping Mode Share",icon="🚚")

# ══ DELIVERY ══════════════════════════════════════════════════════════════════
elif page=="delivery":
    pg_title("🚚 Delivery Performance & Delays")
    fbar_label("Filters")
    c1,c2,c3=st.columns([1.3,1.3,1])
    with c1: sel_s=safe_pills("Status",sorted(df['Order_Status'].unique().tolist()),"dl_s")
    with c2: sel_sh=safe_pills("Shipping",sorted(df['Shipping_Mode'].unique().tolist()),"dl_sh")
    with c3: sel_d=st.slider("Max Delay Days",0,int(df['Delay_Days'].max()),int(df['Delay_Days'].max()))
    d=df[df['Order_Status'].isin(sel_s)&df['Shipping_Mode'].isin(sel_sh)&(df['Delay_Days']<=sel_d)]
    conn_f=sqlite3.connect(':memory:'); d.to_sql('sc',conn_f,index=False,if_exists='replace')
    N=len(d); dld=(d['Order_Status']=='Delayed').sum(); dlv=(d['Order_Status']=='Delivered').sum()
    dd=d[d['Delay_Days']>0]['Delay_Days']; ad=dd.mean() if len(dd) else 0
    it=(d['Order_Status']=='In Transit').sum()
    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{N:,}","in selection","indigo"),
        kpi("🚨","Delayed",f"{dld:,}",f"{dld/N*100:.1f}% rate" if N else "0%","red"),
        kpi("✅","Delivered",f"{dlv:,}",f"{dlv/N*100:.1f}% rate" if N else "0%","green"),
        kpi("⏳","Avg Delay",f"{ad:.1f}d","when delayed","yellow"),
        kpi("🔄","In Transit",f"{it:,}","pending","cyan"),
    ]),unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    r1,r2=st.columns(2)
    with r1:
        q=pd.read_sql("SELECT Shipping_Mode,ROUND(SUM(CASE WHEN Order_Status='Delayed' THEN 1.0 ELSE 0 END)*100/COUNT(*),1) AS Pct FROM sc GROUP BY Shipping_Mode ORDER BY Pct DESC",conn_f)
        fig=px.bar(q,x="Shipping_Mode",y="Pct",color="Shipping_Mode",color_discrete_sequence=PAL,text="Pct")
        fig.update_traces(texttemplate='%{text:.1f}%',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>")
        show(fig,title="Delay Rate by Shipping Mode",icon="📦")
    with r2:
        q2=pd.read_sql("SELECT Month,SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed,COUNT(*) AS Total FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(x=q2['Month'],y=q2['Total'],name='Total',marker_color='rgba(129,140,248,0.2)',
            hovertemplate="<b>%{x}</b><br>Total: %{y}<extra></extra>"))
        fig.add_trace(go.Scatter(x=q2['Month'],y=q2['Delayed'],name='Delayed',mode='lines+markers',
            line=dict(color='#f43f5e',width=2.5),marker_size=6,
            hovertemplate="<b>%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CHART,height=285,title=dict(text="<b style='color:#c7d2fe'>📅  Monthly Orders vs Delays</b>",x=0,pad=dict(l=2)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    r3,r4=st.columns(2)
    with r3:
        q3=pd.read_sql("SELECT Category,ROUND(AVG(Lead_Time_Days),1) AS AL FROM sc GROUP BY Category",conn_f)
        fig=px.bar(q3,x="Category",y="AL",color="Category",color_discrete_sequence=PAL,text="AL")
        fig.update_traces(texttemplate='%{text:.1f}d',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Avg Lead: %{y:.1f} days<extra></extra>")
        show(fig,title="Avg Lead Time by Category",icon="⏱️")
    with r4:
        q4=pd.read_sql("SELECT Category,Order_Status,COUNT(*) AS Count FROM sc GROUP BY Category,Order_Status",conn_f)
        fig=px.bar(q4,x="Category",y="Count",color="Order_Status",color_discrete_map=STATUS_CLR,barmode="stack")
        fig.update_traces(marker_line_width=0,hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig,title="Order Status by Category",icon="📊")

# ══ COST ══════════════════════════════════════════════════════════════════════
elif page=="cost":
    pg_title("💰 Cost & Revenue Analysis")
    fbar_label("Filters")
    c1,c2=st.columns(2)
    with c1: sel_c=safe_pills("Category",sorted(df['Category'].unique().tolist()),"cs_c")
    with c2: sel_p=safe_pills("Payment",sorted(df['Payment_Terms'].unique().tolist()),"cs_p")
    d=df[df['Category'].isin(sel_c)&df['Payment_Terms'].isin(sel_p)]
    conn_f=sqlite3.connect(':memory:'); d.to_sql('sc',conn_f,index=False,if_exists='replace')
    rv=d['Final_Cost_INR'].sum(); fr=d['Freight_Cost_INR'].sum()
    ad=d['Discount_Pct'].mean() if len(d) else 0; au=d['Unit_Cost_INR'].mean() if len(d) else 0
    st.markdown(kpi_row([
        kpi("💰","Total Revenue",f"₹{rv/1e5:.1f}L","final cost INR","cyan"),
        kpi("🚛","Total Freight",f"₹{fr/1e5:.1f}L",f"{fr/rv*100:.1f}% of rev" if rv else "0%","red"),
        kpi("🏷️","Avg Discount",f"{ad:.1f}%","applied to orders","yellow"),
        kpi("📈","Net Margin",f"₹{(rv-fr)/1e5:.1f}L","rev minus freight","green"),
        kpi("📦","Avg Unit Cost",f"₹{au:,.0f}","per unit","indigo"),
        kpi("🔖","Orders",f"{len(d):,}","filtered","pink"),
    ]),unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    r1,r2=st.columns(2)
    with r1:
        q=pd.read_sql("SELECT Category,ROUND(SUM(Final_Cost_INR)/1000,1) AS RK,ROUND(SUM(Freight_Cost_INR)/1000,1) AS FK FROM sc GROUP BY Category ORDER BY RK DESC",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(name='Revenue ₹K',x=q['Category'],y=q['RK'],marker_color='#818cf8',
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>"))
        fig.add_trace(go.Bar(name='Freight ₹K',x=q['Category'],y=q['FK'],marker_color='#f43f5e',
            hovertemplate="<b>%{x}</b><br>Freight: ₹%{y:.0f}K<extra></extra>"))
        fig.update_layout(**CHART,height=285,barmode='group',title=dict(text="<b style='color:#c7d2fe'>💰  Revenue vs Freight by Category</b>",x=0,pad=dict(l=2)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r2:
        q2=pd.read_sql("SELECT Month,ROUND(SUM(Final_Cost_INR)/1000,1) AS RK FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=px.area(q2,x="Month",y="RK",color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fillcolor="rgba(6,182,212,0.1)",line_width=2.5,
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:.0f}K<extra></extra>")
        show(fig,title="Monthly Revenue Trend (₹K)",icon="📈")
    r3,r4=st.columns(2)
    with r3:
        q3=pd.read_sql("SELECT Shipping_Mode,ROUND(AVG(Freight_Cost_INR),0) AS AF FROM sc GROUP BY Shipping_Mode ORDER BY AF DESC",conn_f)
        fig=px.bar(q3,x="Shipping_Mode",y="AF",color="Shipping_Mode",color_discrete_sequence=PAL,text="AF")
        fig.update_traces(texttemplate='₹%{text:,.0f}',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Avg Freight: ₹%{y:,.0f}<extra></extra>")
        show(fig,title="Avg Freight by Shipping Mode",icon="🚢")
    with r4:
        pt=pd.read_sql("SELECT Payment_Terms,COUNT(*) AS Orders FROM sc GROUP BY Payment_Terms",conn_f)
        fig=px.pie(pt,values="Orders",names="Payment_Terms",hole=0.5,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>%{percent}<extra></extra>")
        show(fig,title="Orders by Payment Terms",icon="💳")

# ══ SUPPLIER ══════════════════════════════════════════════════════════════════
elif page=="supplier":
    pg_title("🏆 Supplier Performance")
    fbar_label("Filters")
    c1,c2=st.columns(2)
    with c1: sel_s=safe_pills("Supplier",sorted(df['Supplier_Name'].unique().tolist()),"sp_s")
    with c2: sel_c=safe_pills("City",sorted(df['Supplier_City'].unique().tolist()),"sp_c")
    d=df[df['Supplier_Name'].isin(sel_s)&df['Supplier_City'].isin(sel_c)]
    conn_f=sqlite3.connect(':memory:'); d.to_sql('sc',conn_f,index=False,if_exists='replace')
    ts=d['Supplier_Name'].nunique(); rr=d['Quality_Rating'].dropna()
    aq=rr.mean() if len(rr) else 0; lq=(rr<3).sum() if len(rr) else 0
    al=d['Lead_Time_Days'].mean() if len(d) else 0
    tp=d.groupby('Supplier_Name')['Final_Cost_INR'].sum().idxmax()[:13] if len(d) else "N/A"
    st.markdown(kpi_row([
        kpi("🏢","Suppliers",f"{ts}","active","indigo"),
        kpi("⭐","Avg Quality",f"{aq:.2f}" if aq else "N/A","out of 5.0","yellow"),
        kpi("🔴","Low Quality",f"{lq}","below 3.0","red"),
        kpi("⏱️","Avg Lead",f"{al:.1f}d","order to delivery","cyan"),
        kpi("🥇","Top Supplier",tp,"by revenue","green"),
    ]),unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    r1,r2=st.columns(2)
    with r1:
        q=pd.read_sql("SELECT Supplier_Name,ROUND(SUM(Final_Cost_INR)/1000,1) AS RK FROM sc GROUP BY Supplier_Name ORDER BY RK DESC LIMIT 10",conn_f)
        fig=px.bar(q,x="RK",y="Supplier_Name",orientation='h',color="RK",
                   color_continuous_scale=["#3730a3","#818cf8","#a5b4fc"],text="RK")
        fig.update_traces(texttemplate='₹%{text:.0f}K',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:.0f}K<extra></extra>")
        fig.update_coloraxes(showscale=False)
        show(fig,340,title="Top 10 Suppliers by Revenue",icon="🥇")
    with r2:
        q2=pd.read_sql("SELECT Supplier_Name,ROUND(AVG(Quality_Rating),2) AS AQ FROM sc WHERE Quality_Rating IS NOT NULL GROUP BY Supplier_Name ORDER BY AQ DESC LIMIT 10",conn_f)
        if len(q2):
            fig=px.bar(q2,x="AQ",y="Supplier_Name",orientation='h',color="AQ",
                       color_continuous_scale="RdYlGn",range_color=[1,5],text="AQ")
            fig.update_traces(texttemplate='%{text:.2f}★',textposition='outside',marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>Quality: %{x:.2f}★<extra></extra>")
            fig.update_coloraxes(showscale=False)
            show(fig,340,title="Quality Rating by Supplier",icon="⭐")
    r3,r4=st.columns(2)
    with r3:
        q3=pd.read_sql("SELECT Supplier_City,COUNT(*) AS Orders FROM sc GROUP BY Supplier_City ORDER BY Orders DESC",conn_f)
        fig=px.pie(q3,values="Orders",names="Supplier_City",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Orders: %{value}<br>%{percent}<extra></extra>")
        show(fig,title="Orders by Supplier City",icon="📍")
    with r4:
        q4=pd.read_sql("SELECT Supplier_Name,ROUND(AVG(Lead_Time_Days),1) AS AL FROM sc GROUP BY Supplier_Name ORDER BY AL ASC LIMIT 10",conn_f)
        fig=px.bar(q4,x="Supplier_Name",y="AL",color="AL",
                   color_continuous_scale="RdYlGn_r",text="AL")
        fig.update_traces(texttemplate='%{text:.1f}d',textposition='outside',marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Avg Lead: %{y:.1f} days<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=22,tickfont=dict(size=9))
        show(fig,title="Avg Lead Time by Supplier",icon="⏱️")

# ══ WAREHOUSE ══════════════════════════════════════════════════════════════════
elif page=="warehouse":
    pg_title("🏭 Warehouse Operations")
    fbar_label("Filters")
    c1,c2,c3=st.columns(3)
    with c1: sel_w=safe_pills("Warehouse",sorted(df['Warehouse'].unique().tolist()),"wh_w")
    with c2: sel_c=safe_pills("Category",sorted(df['Category'].unique().tolist()),"wh_c")
    with c3: sel_s=safe_pills("Shipping",sorted(df['Shipping_Mode'].unique().tolist()),"wh_s")
    d=df[df['Warehouse'].isin(sel_w)&df['Category'].isin(sel_c)&df['Shipping_Mode'].isin(sel_s)]
    conn_f=sqlite3.connect(':memory:'); d.to_sql('sc',conn_f,index=False,if_exists='replace')
    N=len(d); wc=d['Warehouse'].nunique()
    ma=d['Warehouse'].value_counts().idxmax().replace("WH-","") if N else "N/A"
    dw=d[d['Order_Status']=='Delayed']['Warehouse']
    md=dw.value_counts().idxmax().replace("WH-","") if len(dw) else "N/A"
    aq=d['Quantity'].mean() if N else 0
    st.markdown(kpi_row([
        kpi("🏭","Warehouses",f"{wc}","active locations","indigo"),
        kpi("📦","Total Orders",f"{N:,}","filtered","cyan"),
        kpi("🏆","Most Active",ma,"by order count","green"),
        kpi("🚨","Most Delays",md,"by delay count","red"),
        kpi("📊","Avg Qty",f"{aq:.1f}","units per order","yellow"),
    ]),unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    r1,r2=st.columns(2)
    with r1:
        q=pd.read_sql("SELECT Warehouse,COUNT(*) AS Orders,SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed FROM sc GROUP BY Warehouse ORDER BY Orders DESC",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(x=q['Warehouse'],y=q['Orders'],name='Total',marker_color='rgba(129,140,248,0.25)',
            hovertemplate="<b>%{x}</b><br>Total Orders: %{y}<extra></extra>"))
        fig.add_trace(go.Bar(x=q['Warehouse'],y=q['Delayed'],name='Delayed',marker_color='#f43f5e',
            hovertemplate="<b>%{x}</b><br>Delayed: %{y}<extra></extra>"))
        fig.update_layout(**CHART,height=285,barmode='group',title=dict(text="<b style='color:#c7d2fe'>🏭  Orders vs Delays by Warehouse</b>",x=0,pad=dict(l=2)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r2:
        q2=pd.read_sql("SELECT Warehouse,ROUND(SUM(Final_Cost_INR)/1000,1) AS RK FROM sc GROUP BY Warehouse ORDER BY RK DESC",conn_f)
        fig=px.pie(q2,values="RK",names="Warehouse",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#030312",width=2)),
            hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:.0f}K<br>%{percent}<extra></extra>")
        show(fig,title="Revenue by Warehouse",icon="💰")
    r3,r4=st.columns(2)
    with r3:
        q3=pd.read_sql("SELECT Warehouse,Category,COUNT(*) AS Count FROM sc GROUP BY Warehouse,Category",conn_f)
        fig=px.bar(q3,x="Warehouse",y="Count",color="Category",color_discrete_sequence=PAL,barmode="stack")
        fig.update_traces(marker_line_width=0,hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig,title="Category Mix by Warehouse",icon="📁")
    with r4:
        q4=pd.read_sql("SELECT Warehouse,Shipping_Mode,COUNT(*) AS Count FROM sc GROUP BY Warehouse,Shipping_Mode",conn_f)
        fig=px.bar(q4,x="Warehouse",y="Count",color="Shipping_Mode",color_discrete_sequence=PAL,barmode="stack")
        fig.update_traces(marker_line_width=0,hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        show(fig,title="Shipping Mode by Warehouse",icon="🚚")

st.markdown('<div style="text-align:center;color:#0f172a;font-size:10px;margin-top:20px;padding-top:10px;border-top:1px solid rgba(129,140,248,0.06)">LogiTrack Pro · Supply Chain Analytics</div>',unsafe_allow_html=True)

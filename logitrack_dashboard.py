import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="LogiTrack Pro", page_icon="📦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #080c1a !important; color: #e2e8f0 !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0a0e1f,#060812) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
}
.block-container { padding-top: 1.5rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.1) !important;
    color: #64748b !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-bottom: 3px !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(99,102,241,0.12) !important;
    color: #a5b4fc !important;
}
.stButton > button {
    background: linear-gradient(135deg,#6366f1,#7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
}
span[data-baseweb="tag"] {
    background: rgba(99,102,241,0.2) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 20px !important; color: #a5b4fc !important;
    font-size: 11px !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
    border-radius: 10px !important;
}
button[data-baseweb="tab"] { color: #475569 !important; background: transparent !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}
hr { border: none !important; border-top: 1px solid rgba(99,102,241,0.1) !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_csv('supply_chain_2024_25.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    return df

df = load_data()

PAL = ["#6366f1","#06b6d4","#22c55e","#f59e0b","#ec4899","#ef4444","#8b5cf6","#14b8a6"]
STATUS_CLR = {"Delivered":"#22c55e","In Transit":"#3b82f6","Delayed":"#ef4444","Cancelled":"#6b7280","Pending":"#f59e0b"}
CHART = dict(
    template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b", family="Inter,sans-serif", size=11),
    margin=dict(l=10,r=10,t=38,b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10,color="#64748b")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10,color="#475569")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10,color="#475569")),
)

GLOW = {"indigo":"#6366f1","cyan":"#06b6d4","green":"#22c55e","red":"#ef4444","yellow":"#f59e0b","pink":"#ec4899"}

def kpi(icon, label, value, sub, color):
    g = GLOW.get(color, "#6366f1")
    return f"""
    <div style="flex:1 1 150px;min-width:130px;
        background:linear-gradient(135deg,#0f1225,#141830);
        border:1px solid {g}30; border-radius:16px; padding:18px 16px;
        position:relative; overflow:hidden;
        box-shadow:0 0 30px {g}15,0 4px 20px rgba(0,0,0,0.5);">
      <div style="position:absolute;top:-20px;right:-20px;width:70px;height:70px;border-radius:50%;
          background:radial-gradient(circle,{g}30,transparent 70%);pointer-events:none;"></div>
      <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;">
        <span style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;">{label}</span>
        <span style="font-size:18px;">{icon}</span>
      </div>
      <div style="font-size:28px;font-weight:900;color:#f1f5f9;letter-spacing:-0.02em;line-height:1;">{value}</div>
      <div style="font-size:11px;color:#475569;margin-top:6px;">{sub}</div>
      <div style="position:absolute;bottom:0;left:0;right:0;height:2px;
          background:linear-gradient(90deg,{g}80,transparent);"></div>
    </div>"""

def kpi_row(cards):
    return f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;">{"".join(cards)}</div>'

def show(fig, h=300):
    fig.update_layout(**CHART, height=h)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def page_header(icon, title, sub):
    st.markdown(f"""
    <div style="margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(99,102,241,0.1);">
      <div style="font-size:22px;font-weight:900;letter-spacing:-0.02em;
          background:linear-gradient(120deg,#c7d2fe,#a5f3fc);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{icon} {title}</div>
      <div style="font-size:12px;color:#475569;margin-top:4px;">{sub}</div>
    </div>""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "overview"

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:14px 0 18px;border-bottom:1px solid rgba(99,102,241,0.12);margin-bottom:16px;">
      <div style="font-size:34px;filter:drop-shadow(0 0 10px rgba(99,102,241,0.8));">📦</div>
      <div style="font-size:17px;font-weight:900;background:linear-gradient(120deg,#c7d2fe,#a5f3fc);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:6px;">LogiTrack</div>
      <div style="font-size:8px;color:#6366f1;font-weight:800;letter-spacing:0.2em;text-transform:uppercase;margin-top:2px;">PRO</div>
    </div>
    <div style="font-size:9px;color:#1e293b;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:8px;">Navigation</div>
    """, unsafe_allow_html=True)

    pages = {
        "📊  Overview":          "overview",
        "🚚  Delivery & Delays": "delivery",
        "💰  Cost Analysis":     "cost",
        "🏆  Supplier Analysis": "supplier",
        "🏭  Warehouse Ops":     "warehouse",
        "🗃️  SQL Explorer":     "raw",
    }
    for label, key in pages.items():
        active = st.session_state.page == key
        if active:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:10px;
                margin-bottom:3px;background:linear-gradient(135deg,rgba(99,102,241,0.25),rgba(124,58,237,0.2));
                border:1px solid rgba(99,102,241,0.4);box-shadow:0 0 20px rgba(99,102,241,0.2);">
              <span style="font-size:14px;">{label.split()[0]}</span>
              <span style="color:#c7d2fe;font-weight:700;font-size:13px;">{"  ".join(label.split()[1:])}</span>
            </div>""", unsafe_allow_html=True)
        else:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:9px;color:#1e293b;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:8px;">Filters</div>', unsafe_allow_html=True)

    page = st.session_state.page

    if page == "overview":
        sel_cat = st.multiselect("Category", sorted(df['Category'].unique()), default=list(df['Category'].unique()))
        sel_wh  = st.multiselect("Warehouse", sorted(df['Warehouse'].unique()), default=list(df['Warehouse'].unique()))
        d = df[df['Category'].isin(sel_cat) & df['Warehouse'].isin(sel_wh)]
    elif page == "delivery":
        sel_status = st.multiselect("Order Status", sorted(df['Order_Status'].unique()), default=list(df['Order_Status'].unique()))
        sel_ship   = st.multiselect("Shipping Mode", sorted(df['Shipping_Mode'].unique()), default=list(df['Shipping_Mode'].unique()))
        sel_delay  = st.slider("Max Delay Days", 0, int(df['Delay_Days'].max()), int(df['Delay_Days'].max()))
        d = df[df['Order_Status'].isin(sel_status) & df['Shipping_Mode'].isin(sel_ship) & (df['Delay_Days'] <= sel_delay)]
    elif page == "cost":
        sel_cat2 = st.multiselect("Category", sorted(df['Category'].unique()), default=list(df['Category'].unique()))
        sel_pay  = st.multiselect("Payment Terms", sorted(df['Payment_Terms'].unique()), default=list(df['Payment_Terms'].unique()))
        d = df[df['Category'].isin(sel_cat2) & df['Payment_Terms'].isin(sel_pay)]
    elif page == "supplier":
        sel_sup  = st.multiselect("Supplier", sorted(df['Supplier_Name'].unique()), default=list(df['Supplier_Name'].unique()))
        sel_city = st.multiselect("City", sorted(df['Supplier_City'].unique()), default=list(df['Supplier_City'].unique()))
        d = df[df['Supplier_Name'].isin(sel_sup) & df['Supplier_City'].isin(sel_city)]
    elif page == "warehouse":
        sel_wh2  = st.multiselect("Warehouse", sorted(df['Warehouse'].unique()), default=list(df['Warehouse'].unique()))
        sel_cat3 = st.multiselect("Category", sorted(df['Category'].unique()), default=list(df['Category'].unique()))
        sel_ship2= st.multiselect("Shipping Mode", sorted(df['Shipping_Mode'].unique()), default=list(df['Shipping_Mode'].unique()))
        d = df[df['Warehouse'].isin(sel_wh2) & df['Category'].isin(sel_cat3) & df['Shipping_Mode'].isin(sel_ship2)]
    else:
        sel_stat3 = st.multiselect("Status", sorted(df['Order_Status'].unique()), default=list(df['Order_Status'].unique()))
        sel_cat4  = st.multiselect("Category", sorted(df['Category'].unique()), default=list(df['Category'].unique()))
        d = df[df['Order_Status'].isin(sel_stat3) & df['Category'].isin(sel_cat4)]

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()
    st.markdown(f"""
    <div style="text-align:center;margin-top:8px;">
      <div style="font-size:22px;font-weight:900;color:#6366f1;">{len(d):,}</div>
      <div style="font-size:10px;color:#475569;">records selected</div>
    </div>""", unsafe_allow_html=True)

conn_f = sqlite3.connect(':memory:')
d.to_sql('sc', conn_f, index=False, if_exists='replace')

if page == "overview":
    page_header("📊", "Supply Chain Overview", "SmartLogistics Co. · Jan 2024 – Apr 2025 · Full operations summary")
    total=len(d); rev=d['Final_Cost_INR'].sum(); avg_lead=d['Lead_Time_Days'].mean() if total else 0
    delayed=(d['Order_Status']=='Delayed').sum(); delivered=(d['Order_Status']=='Delivered').sum()
    rate=delivered/total*100 if total else 0; rated=d['Quality_Rating'].dropna(); avg_q=rated.mean() if len(rated) else 0
    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{total:,}","filtered records","indigo"),
        kpi("💰","Revenue",f"₹{rev/1e5:.1f}L","final cost INR","cyan"),
        kpi("⏱️","Avg Lead Time",f"{avg_lead:.1f}d","order → delivery","green"),
        kpi("🚨","Delayed",f"{delayed:,}",f"{delayed/total*100:.0f}% of total" if total else "0%","red"),
        kpi("✅","Delivery Rate",f"{rate:.0f}%",f"{delivered} delivered","green"),
        kpi("⭐","Avg Quality",f"{avg_q:.2f}" if avg_q else "N/A","out of 5.0","yellow"),
    ]), unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        mdf=pd.read_sql("SELECT Month, COUNT(*) AS Orders FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=px.line(mdf,x="Month",y="Orders",title="📅 Monthly Orders Trend",markers=True,color_discrete_sequence=["#6366f1"])
        fig.update_traces(fill='tozeroy',fillcolor='rgba(99,102,241,0.08)',line_width=2.5,marker_size=5)
        show(fig)
    with c2:
        sdf=pd.read_sql("SELECT Order_Status, COUNT(*) AS Count FROM sc GROUP BY Order_Status",conn_f)
        fig=px.pie(sdf,values="Count",names="Order_Status",title="🥧 Order Status Distribution",hole=0.5,color="Order_Status",color_discrete_map=STATUS_CLR)
        fig.update_traces(marker=dict(line=dict(color="#080c1a",width=2)))
        show(fig)
    c3,c4=st.columns(2)
    with c3:
        cdf=pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Category ORDER BY Rev_K DESC",conn_f)
        fig=px.bar(cdf,x="Category",y="Rev_K",title="💰 Revenue by Category (₹K)",color="Category",color_discrete_sequence=PAL,text="Rev_K")
        fig.update_traces(texttemplate='₹%{text:.0f}K',textposition='outside',marker_line_width=0)
        show(fig)
    with c4:
        shdf=pd.read_sql("SELECT Shipping_Mode, COUNT(*) AS Orders FROM sc GROUP BY Shipping_Mode",conn_f)
        fig=px.pie(shdf,values="Orders",names="Shipping_Mode",title="🚚 Shipping Mode Share",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#080c1a",width=2)))
        show(fig)

elif page == "delivery":
    page_header("🚚","Delivery Performance & Delays","On-time rate · Delay root causes · Shipping analysis")
    total=len(d); delayed=(d['Order_Status']=='Delayed').sum(); on_time=(d['Order_Status']=='Delivered').sum()
    delay_d=d[d['Delay_Days']>0]['Delay_Days']; avg_delay=delay_d.mean() if len(delay_d) else 0
    in_transit=(d['Order_Status']=='In Transit').sum()
    st.markdown(kpi_row([
        kpi("📦","Total Orders",f"{total:,}","in selection","indigo"),
        kpi("🚨","Delayed",f"{delayed:,}",f"{delayed/total*100:.1f}% rate" if total else "0%","red"),
        kpi("✅","Delivered",f"{on_time:,}",f"{on_time/total*100:.1f}% rate" if total else "0%","green"),
        kpi("⏳","Avg Delay",f"{avg_delay:.1f}d","when delayed","yellow"),
        kpi("🔄","In Transit",f"{in_transit:,}","pending delivery","cyan"),
    ]), unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        q=pd.read_sql("SELECT Shipping_Mode, ROUND(SUM(CASE WHEN Order_Status='Delayed' THEN 1.0 ELSE 0 END)*100/COUNT(*),1) AS Delay_Pct FROM sc GROUP BY Shipping_Mode ORDER BY Delay_Pct DESC",conn_f)
        fig=px.bar(q,x="Shipping_Mode",y="Delay_Pct",title="🚚 Delay Rate by Shipping Mode (%)",color="Shipping_Mode",color_discrete_sequence=PAL,text="Delay_Pct")
        fig.update_traces(texttemplate='%{text:.1f}%',textposition='outside',marker_line_width=0)
        show(fig)
    with c2:
        q2=pd.read_sql("SELECT Month, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed, COUNT(*) AS Total FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(x=q2['Month'],y=q2['Total'],name='Total Orders',marker_color='rgba(99,102,241,0.2)'))
        fig.add_trace(go.Scatter(x=q2['Month'],y=q2['Delayed'],name='Delayed',mode='lines+markers',line=dict(color='#ef4444',width=2.5),marker_size=6))
        fig.update_layout(title="📅 Monthly Orders vs Delays",**CHART,height=300)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    c3,c4=st.columns(2)
    with c3:
        q3=pd.read_sql("SELECT Category, ROUND(AVG(Lead_Time_Days),1) AS Avg_Lead FROM sc GROUP BY Category",conn_f)
        fig=px.bar(q3,x="Category",y="Avg_Lead",title="⏱️ Avg Lead Time by Category",color="Category",color_discrete_sequence=PAL,text="Avg_Lead")
        fig.update_traces(texttemplate='%{text:.1f}d',textposition='outside',marker_line_width=0)
        show(fig)
    with c4:
        q4=pd.read_sql("SELECT Category, Order_Status, COUNT(*) AS Count FROM sc GROUP BY Category, Order_Status",conn_f)
        fig=px.bar(q4,x="Category",y="Count",color="Order_Status",title="📊 Status by Category",color_discrete_map=STATUS_CLR,barmode="stack")
        fig.update_traces(marker_line_width=0)
        show(fig)

elif page == "cost":
    page_header("💰","Cost & Revenue Analysis","Freight costs · Discount leakage · Margin breakdown")
    rev=d['Final_Cost_INR'].sum(); freight=d['Freight_Cost_INR'].sum()
    avg_disc=d['Discount_Pct'].mean() if len(d) else 0; avg_unit=d['Unit_Cost_INR'].mean() if len(d) else 0
    net_margin=rev-freight
    st.markdown(kpi_row([
        kpi("💰","Total Revenue",f"₹{rev/1e5:.1f}L","final cost INR","cyan"),
        kpi("🚛","Total Freight",f"₹{freight/1e5:.1f}L",f"{freight/rev*100:.1f}% of rev" if rev else "0%","red"),
        kpi("🏷️","Avg Discount",f"{avg_disc:.1f}%","applied to orders","yellow"),
        kpi("📈","Net Margin",f"₹{net_margin/1e5:.1f}L","rev minus freight","green"),
        kpi("📦","Avg Unit Cost",f"₹{avg_unit:,.0f}","per unit","indigo"),
        kpi("🔖","Orders",f"{len(d):,}","filtered","pink"),
    ]), unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        q=pd.read_sql("SELECT Category, ROUND(SUM(Final_Cost_INR)/1000,1) AS Revenue_K, ROUND(SUM(Freight_Cost_INR)/1000,1) AS Freight_K FROM sc GROUP BY Category ORDER BY Revenue_K DESC",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(name='Revenue (₹K)',x=q['Category'],y=q['Revenue_K'],marker_color='#6366f1'))
        fig.add_trace(go.Bar(name='Freight (₹K)',x=q['Category'],y=q['Freight_K'],marker_color='#ef4444'))
        fig.update_layout(title="💰 Revenue vs Freight by Category",barmode='group',**CHART,height=300)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        q2=pd.read_sql("SELECT Month, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Month ORDER BY Month",conn_f)
        fig=px.area(q2,x="Month",y="Rev_K",title="📈 Monthly Revenue Trend (₹K)",color_discrete_sequence=["#06b6d4"])
        fig.update_traces(fillcolor='rgba(6,182,212,0.08)',line_width=2.5)
        show(fig)
    c3,c4=st.columns(2)
    with c3:
        q3=pd.read_sql("SELECT Shipping_Mode, ROUND(AVG(Freight_Cost_INR),0) AS Avg_Freight FROM sc GROUP BY Shipping_Mode ORDER BY Avg_Freight DESC",conn_f)
        fig=px.bar(q3,x="Shipping_Mode",y="Avg_Freight",title="🚚 Avg Freight by Shipping Mode (₹)",color="Shipping_Mode",color_discrete_sequence=PAL,text="Avg_Freight")
        fig.update_traces(texttemplate='₹%{text:,.0f}',textposition='outside',marker_line_width=0)
        show(fig)
    with c4:
        pt=pd.read_sql("SELECT Payment_Terms, COUNT(*) AS Orders FROM sc GROUP BY Payment_Terms",conn_f)
        fig=px.pie(pt,values="Orders",names="Payment_Terms",title="💳 Orders by Payment Terms",hole=0.5,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#080c1a",width=2)))
        show(fig)

elif page == "supplier":
    page_header("🏆","Supplier Performance Analysis","Quality ratings · Lead times · Revenue leaders")
    total_sup=d['Supplier_Name'].nunique(); rated=d['Quality_Rating'].dropna()
    avg_q=rated.mean() if len(rated) else 0; low_q=(rated<3).sum() if len(rated) else 0
    avg_lead=d['Lead_Time_Days'].mean() if len(d) else 0
    top_sup=d.groupby('Supplier_Name')['Final_Cost_INR'].sum().idxmax()[:12] if len(d) else "N/A"
    st.markdown(kpi_row([
        kpi("🏢","Suppliers",f"{total_sup}","active suppliers","indigo"),
        kpi("⭐","Avg Quality",f"{avg_q:.2f}" if avg_q else "N/A","out of 5.0","yellow"),
        kpi("🔴","Low Quality",f"{low_q}","ratings below 3.0","red"),
        kpi("⏱️","Avg Lead",f"{avg_lead:.1f}d","order to delivery","cyan"),
        kpi("🥇","Top Supplier",top_sup,"by revenue","green"),
    ]), unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        q=pd.read_sql("SELECT Supplier_Name, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Supplier_Name ORDER BY Rev_K DESC LIMIT 10",conn_f)
        fig=px.bar(q,x="Rev_K",y="Supplier_Name",orientation='h',title="🥇 Top 10 Suppliers by Revenue (₹K)",color="Rev_K",color_continuous_scale="Purples",text="Rev_K")
        fig.update_traces(texttemplate='₹%{text:.0f}K',textposition='outside',marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        show(fig,350)
    with c2:
        q2=pd.read_sql("SELECT Supplier_Name, ROUND(AVG(Quality_Rating),2) AS Avg_Q FROM sc WHERE Quality_Rating IS NOT NULL GROUP BY Supplier_Name ORDER BY Avg_Q DESC LIMIT 10",conn_f)
        if len(q2):
            fig=px.bar(q2,x="Avg_Q",y="Supplier_Name",orientation='h',title="⭐ Avg Quality Rating by Supplier",color="Avg_Q",color_continuous_scale="RdYlGn",range_color=[1,5],text="Avg_Q")
            fig.update_traces(texttemplate='%{text:.2f}★',textposition='outside',marker_line_width=0)
            fig.update_coloraxes(showscale=False)
            show(fig,350)
    c3,c4=st.columns(2)
    with c3:
        q3=pd.read_sql("SELECT Supplier_City, COUNT(*) AS Orders FROM sc GROUP BY Supplier_City ORDER BY Orders DESC",conn_f)
        fig=px.pie(q3,values="Orders",names="Supplier_City",title="📍 Orders by Supplier City",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#080c1a",width=2)))
        show(fig)
    with c4:
        q4=pd.read_sql("SELECT Supplier_Name, ROUND(AVG(Lead_Time_Days),1) AS Avg_Lead FROM sc GROUP BY Supplier_Name ORDER BY Avg_Lead ASC LIMIT 10",conn_f)
        fig=px.bar(q4,x="Supplier_Name",y="Avg_Lead",title="⏱️ Avg Lead Time by Supplier",color="Avg_Lead",color_continuous_scale="RdYlGn_r",text="Avg_Lead")
        fig.update_traces(texttemplate='%{text:.1f}d',textposition='outside',marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=25,tickfont=dict(size=9))
        show(fig)

elif page == "warehouse":
    page_header("🏭","Warehouse Operations","Load distribution · Delay hotspots · Revenue by location")
    total=len(d); wh_count=d['Warehouse'].nunique()
    most_active=d['Warehouse'].value_counts().idxmax().replace("WH-","") if total else "N/A"
    delay_wh=d[d['Order_Status']=='Delayed']['Warehouse']
    most_delay=delay_wh.value_counts().idxmax().replace("WH-","") if len(delay_wh) else "N/A"
    avg_qty=d['Quantity'].mean() if total else 0
    st.markdown(kpi_row([
        kpi("🏭","Warehouses",f"{wh_count}","active locations","indigo"),
        kpi("📦","Total Orders",f"{total:,}","filtered","cyan"),
        kpi("🏆","Most Active",most_active,"by order count","green"),
        kpi("🚨","Most Delays",most_delay,"by delay count","red"),
        kpi("📊","Avg Qty",f"{avg_qty:.1f}","units per order","yellow"),
    ]), unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        q=pd.read_sql("SELECT Warehouse, COUNT(*) AS Orders, SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed FROM sc GROUP BY Warehouse ORDER BY Orders DESC",conn_f)
        fig=go.Figure()
        fig.add_trace(go.Bar(name='Total Orders',x=q['Warehouse'],y=q['Orders'],marker_color='rgba(99,102,241,0.3)'))
        fig.add_trace(go.Bar(name='Delayed',x=q['Warehouse'],y=q['Delayed'],marker_color='#ef4444'))
        fig.update_layout(title="🏭 Orders vs Delays by Warehouse",barmode='group',**CHART,height=300)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        q2=pd.read_sql("SELECT Warehouse, ROUND(SUM(Final_Cost_INR)/1000,1) AS Rev_K FROM sc GROUP BY Warehouse ORDER BY Rev_K DESC",conn_f)
        fig=px.pie(q2,values="Rev_K",names="Warehouse",title="💰 Revenue by Warehouse",hole=0.45,color_discrete_sequence=PAL)
        fig.update_traces(marker=dict(line=dict(color="#080c1a",width=2)))
        show(fig)
    c3,c4=st.columns(2)
    with c3:
        q3=pd.read_sql("SELECT Warehouse, Category, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Category",conn_f)
        fig=px.bar(q3,x="Warehouse",y="Count",color="Category",title="📁 Category Mix by Warehouse",color_discrete_sequence=PAL,barmode="stack")
        fig.update_traces(marker_line_width=0)
        show(fig)
    with c4:
        q4=pd.read_sql("SELECT Warehouse, Shipping_Mode, COUNT(*) AS Count FROM sc GROUP BY Warehouse, Shipping_Mode",conn_f)
        fig=px.bar(q4,x="Warehouse",y="Count",color="Shipping_Mode",title="🚚 Shipping Mode by Warehouse",color_discrete_sequence=PAL,barmode="stack")
        fig.update_traces(marker_line_width=0)
        show(fig)

elif page == "raw":
    page_header("🗃️","Raw Data & SQL Explorer","Browse records · Custom SQL queries · Export data")
    tab1,tab2=st.tabs(["  📋  Order Table  ","  🔍  SQL Explorer  "])
    with tab1:
        st.markdown(f'<div style="margin-bottom:10px;"><span style="font-size:20px;font-weight:900;color:#6366f1;">{len(d):,}</span> <span style="font-size:12px;color:#475569;">records selected</span></div>',unsafe_allow_html=True)
        status_icons={"Delivered":"🟢","In Transit":"🔵","Delayed":"🔴","Cancelled":"⚫","Pending":"🟡"}
        d_show=d.copy()
        d_show['Order_Status']=d_show['Order_Status'].map(lambda x:f"{status_icons.get(x,'')} {x}")
        d_show['Quality_Rating']=d_show['Quality_Rating'].apply(lambda x:f"⭐ {x:.1f}" if pd.notna(x) and x>0 else "—")
        d_show['Final_Cost_INR']=d_show['Final_Cost_INR'].apply(lambda x:f"₹{x:,.0f}")
        cols=['Order_ID','Order_Date','Supplier_Name','Category','Warehouse','Shipping_Mode','Quantity','Final_Cost_INR','Lead_Time_Days','Order_Status','Quality_Rating']
        st.dataframe(d_show[cols].rename(columns={'Order_ID':'Order','Order_Date':'Date','Supplier_Name':'Supplier','Warehouse':'WH','Shipping_Mode':'Mode','Quantity':'Qty','Final_Cost_INR':'Revenue','Lead_Time_Days':'Lead','Order_Status':'Status','Quality_Rating':'Quality'}),use_container_width=True,height=440)
        st.download_button("⬇️ Export Filtered CSV",d[cols].to_csv(index=False),"logitrack_data.csv","text/csv",use_container_width=True)
    with tab2:
        st.markdown('<div style="font-size:12px;color:#475569;margin-bottom:8px;">Table name: <code style="color:#a5b4fc;background:rgba(99,102,241,0.12);padding:2px 7px;border-radius:5px;">sc</code></div>',unsafe_allow_html=True)
        default_q="""SELECT Category,\n    COUNT(*) AS Orders,\n    ROUND(SUM(Final_Cost_INR)/1000, 1) AS Revenue_K,\n    ROUND(AVG(Lead_Time_Days), 1) AS Avg_Lead,\n    SUM(CASE WHEN Order_Status='Delayed' THEN 1 ELSE 0 END) AS Delayed\nFROM sc\nGROUP BY Category\nORDER BY Revenue_K DESC"""
        user_q=st.text_area("SQL Query",value=default_q,height=170)
        if st.button("▶️  Run Query",use_container_width=True):
            try:
                result=pd.read_sql(user_q,conn_f)
                st.success(f"✅ {len(result)} rows returned")
                st.dataframe(result,use_container_width=True)
            except Exception as e:
                st.error(f"❌ SQL Error: {e}")

st.markdown('<div style="text-align:center;color:#1e293b;font-size:11px;margin-top:20px;padding-top:12px;border-top:1px solid rgba(99,102,241,0.08);">LogiTrack Pro · Supply Chain Analytics · SmartLogistics Co.</div>',unsafe_allow_html=True)

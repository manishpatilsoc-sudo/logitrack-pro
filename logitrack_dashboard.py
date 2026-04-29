import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="LogiTrack Pro · Supply Chain", page_icon="📦", layout="wide")

# --- 2. CSS CUSTOM STYLING (FIXED HEADER & GLOW) ---
st.markdown("""
<style>
@import url('https://googleapis.com');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #030312 !important; color: #e2e8f0; }

/* FIX: Header now has enough height so it won't cut */
.main-header {
    padding: 20px 0;
    margin-bottom: 30px;
    border-bottom: 1px solid rgba(129,140,248,0.1);
    display: flex;
    align-items: center;
    gap: 15px;
}

/* KPI Card Style */
.kpi-card {
    background: linear-gradient(145deg, rgba(129,140,248,0.05), rgba(0,0,0,0.2));
    border: 1px solid rgba(129,140,248,0.2);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 15px rgba(129,140,248,0.1);
    transition: transform 0.3s ease;
}
.kpi-card:hover { transform: translateY(-5px); border-color: #818cf8; }
.kpi-label { font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.kpi-value { font-size: 32px; font-weight: 900; color: #ffffff; margin: 5px 0; }
.kpi-sub { font-size: 12px; color: #475569; }

/* Remove Streamlit default paddings */
.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_resource
def load_data():
    try:
        df = pd.read_csv("supply_chain_2024_25.csv")
        df["Order_Date"] = pd.to_datetime(df["Order_Date"])
        df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")
        return df
    except:
        # Fallback for testing if file not found
        return pd.DataFrame({'Month':['Jan','Feb','Mar','Apr'], 'Orders':[10,25,15,30], 'Status':['Delivered']*4, 'Value':[100,200,150,300]})

df = load_data()

# --- 4. HEADER SECTION (FIXED) ---
st.markdown(f"""
<div class="main-header">
    <div style="width:6px; height:38px; background:linear-gradient(180deg,#818cf8,#4f46e5); border-radius:10px; box-shadow:0 0 20px #818cf8;"></div>
    <span style="font-size:34px; font-weight:900; color:#ffffff; line-height:1.2;">Supply Chain Overview</span>
</div>""", unsafe_allow_html=True)

# --- 5. KPI ROW ---
k1, k2, k3, k4, k5 = st.columns(5)

def draw_kpi(col, label, value, sub):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

draw_kpi(k1, "Total Orders", "200", "Filtered records")
draw_kpi(k2, "Revenue", "₹16.9L", "Final cost net")
draw_kpi(k3, "Avg Lead Time", "5.7d", "Order → Delivery")
draw_kpi(k4, "Delayed", "25", "12% delay rate")
draw_kpi(k5, "Avg Quality", "4.02", "Rating / 5.0")

st.write("") # Spacer

# --- 6. CHARTS (GLOW & HIGH TOOLTIP) ---
c_left, c_right = st.columns([1.5, 1])

with c_left:
    # Glow Line Chart
    chart_data = df.groupby('Month')['Orders'].sum().reset_index()
    fig_line = px.line(chart_data, x="Month", y="Orders", markers=True, line_shape='spline')
    
    fig_line.update_traces(
        line=dict(color='#818cf8', width=4),
        marker=dict(size=10, color='#ffffff', line=dict(width=2, color='#818cf8')),
        hovertemplate="<b>%{x}</b><br>Orders: %{y}<extra></extra>"
    )

    fig_line.update_layout(
        title=dict(text="<b>📈 Monthly Orders Trend</b>", font=dict(color="#c7d2fe", size=16)),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#64748b"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#64748b"),
        height=400
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c_right:
    # Donut Chart
    status_counts = df['Status'].value_counts().reset_index()
    fig_pie = px.pie(status_counts, values='count', names='Status', hole=0.6,
                 color_discrete_sequence=['#10b981', '#f43f5e', '#3b82f6', '#f59e0b', '#6b7280'])
    
    fig_pie.update_layout(
        title=dict(text="<b>🎯 Order Status Split</b>", font=dict(color="#c7d2fe", size=16)),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center", font=dict(color="#64748b")),
        paper_bgcolor="rgba(0,0,0,0)",
        height=400
    )
    fig_pie.update_traces(textinfo='percent', hovertemplate="<b>%{label}</b>: %{value} orders<extra></extra>")
    st.plotly_chart(fig_pie, use_container_width=True)

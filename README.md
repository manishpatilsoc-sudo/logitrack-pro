<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>

# 📦 LogiTrack Pro
### Supply Chain Analytics Dashboard

**[🚀 Live Demo](https://manishpatil-logitrack-pro.streamlit.app)** · **[📄 Project Summary](docs/project_summary.md)** · **[📘 Setup Guide](reports/LogiTrack_Pro_Guide.pdf)**

</div>

---

## 🎯 The Story Behind This Project

SmartLogistics Co. was losing money — but nobody knew exactly where or why.

Orders were getting delayed. Freight costs were high. Some suppliers kept delivering
poor quality products. Some warehouses were overloaded while others sat idle.

The management had data — **200 orders, 24 columns, 16 months** — but it was
sitting in a raw CSV file with no way to make sense of it.

**I built LogiTrack Pro to change that.**

---

## 💡 4 Business Problems Solved

| # | Problem | Insight Found |
|---|---------|--------------|
| 1 | Why are orders getting delayed? | Air shipping has 18% delay rate — highest of all modes |
| 2 | Where is revenue leaking? | Freight = 22% of total revenue on average |
| 3 | Which suppliers are unreliable? | 3 suppliers consistently score below 3/5 quality |
| 4 | Which warehouse needs attention? | WH-Mumbai handles 31% of orders but has most delays |

---

## ✨ Dashboard Features

- **5 Interactive Pages** — Overview, Delivery, Cost & Revenue, Suppliers, Warehouse
- **Glow KPI Cards** — 6 metrics per page with color-coded glow effects
- **12+ SQL Queries** — All data powered by in-memory SQLite
- **Interactive Charts** — Hover tooltips, zoom, pan via Plotly
- **Page-specific Filters** — Different slicers on each page
- **Dark Professional Theme** — Indigo/cyan color palette

---

## 🛠️ Tech Stack

```
Python 3.10+
├── streamlit      → Web app (no HTML needed)
├── pandas         → Data manipulation
├── plotly         → Interactive charts
└── sqlite3        → In-memory SQL (built into Python)
```

---

## 📁 Project Structure

```
logitrack-pro/
├── logitrack_dashboard.py     ← Main dashboard
├── requirements.txt           ← Python dependencies
├── data/
│   └── supply_chain_2024_25.csv   ← Dataset (200 rows, 24 cols)
├── docs/
│   └── project_summary.md     ← Business problem & insights
├── reports/
│   └── LogiTrack_Pro_Guide.pdf    ← Setup & deployment guide
└── assets/
    └── screenshots/           ← Dashboard screenshots
```

---

## 🚀 Run Locally

```bash
# Install dependencies
pip install streamlit pandas plotly

# Run dashboard
streamlit run logitrack_dashboard.py
```

Opens at: **http://localhost:8501**

---

## 🌐 Deploy Free (Streamlit Cloud)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → Select this repo
4. Main file: `logitrack_dashboard.py`
5. Click **Deploy!**

---

## 📊 Dataset Overview

| Column | Description |
|--------|-------------|
| Order_ID | Unique order identifier |
| Order_Date | Date order was placed |
| Supplier_Name / City | Supplier details |
| Category | Electronics, Machinery, Raw Material, Consumables, Chemicals |
| Warehouse | Mumbai, Delhi, Chennai, Bangalore, Pune |
| Shipping_Mode | Road, Rail, Air, Sea |
| Final_Cost_INR | Total order value |
| Freight_Cost_INR | Shipping cost |
| Lead_Time_Days | Days from order to delivery |
| Delay_Days | Days delayed (0 = on time) |
| Order_Status | Delivered, In Transit, Delayed, Cancelled, Pending |
| Quality_Rating | 1–5 rating (delivered orders only) |

---

## 👨‍💻 Author

**Manish Patil**
📧 manishpatil.soc@gmail.com
🔗 Supply Chain Analytics | Power BI | Python

---

*Built with Python · Streamlit · Plotly · SQLite · Pandas*

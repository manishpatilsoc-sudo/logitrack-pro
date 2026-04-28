# LogiTrack Pro — Project Summary

## About This Project

**LogiTrack Pro** is an interactive Supply Chain Analytics Dashboard built using
Python, Streamlit, Plotly, and SQLite. This project was developed to solve real
business problems faced by SmartLogistics Co. — a mid-size logistics company
managing 200+ orders across 5 warehouses, 10+ suppliers, and 4 shipping modes.

---

## The Business Problem

SmartLogistics Co. was struggling with 4 critical issues:

### Problem 1: Delivery Delays
- 13% of all orders were getting delayed
- No visibility into WHICH shipping mode or warehouse was causing delays
- Management had no way to track delay trends over time

### Problem 2: Cost Leakage
- Freight costs were eating into margins but nobody knew exactly how much
- Discount patterns were unclear — were discounts helping or hurting?
- No category-wise cost breakdown existed

### Problem 3: Supplier Inconsistency
- Quality ratings varied wildly between suppliers (1.8 to 4.9 out of 5)
- Some suppliers had 3x longer lead times than others
- No single view to compare all suppliers at once

### Problem 4: Warehouse Imbalance
- Some warehouses were overloaded (Mumbai, Delhi)
- Others were underutilized
- Delay rates differed significantly by warehouse location

---

## The Solution

I built **LogiTrack Pro** — a 5-page interactive dashboard that turns raw
supply chain data into actionable business insights in real time.

### Dashboard Pages:
1. **Overview** — Complete KPI summary with monthly trends
2. **Delivery** — Delay analysis by shipping mode, category, and time
3. **Cost & Revenue** — Freight ratios, margins, and payment analysis
4. **Suppliers** — Quality ratings, lead times, top performers
5. **Warehouse** — Load distribution and delay hotspots

---

## Key Insights Discovered

| Insight | Finding |
|---------|---------|
| Delay Rate | Air shipping has the highest delay rate (18%) |
| Cost | Freight is 22% of total revenue on average |
| Quality | 3 suppliers consistently score below 3/5 |
| Warehouse | WH-Mumbai handles 31% of all orders |
| Lead Time | Electronics category has 2x longer lead time vs Consumables |

---

## Technical Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core programming language |
| Streamlit | Web app framework (no HTML needed) |
| Plotly | Interactive charts with hover tooltips |
| SQLite3 | In-memory SQL queries (12+ queries) |
| Pandas | Data manipulation and filtering |

---

## Dataset

- **Source**: SmartLogistics Co. internal data (simulated)
- **Period**: January 2024 – April 2025 (16 months)
- **Size**: 200 orders, 24 columns
- **Categories**: Electronics, Machinery, Raw Material, Consumables, Chemicals
- **Warehouses**: Mumbai, Delhi, Chennai, Bangalore, Pune

---

## Author

**Manish Patil**
Email: manishpatil.soc@gmail.com
Domain: Supply Chain Analytics | Power BI | Python

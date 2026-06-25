import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="RetailMind Analytics",
    page_icon="📊",
    layout="wide"
)

load_css()

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_data.csv")

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎛 Dashboard Filters")

year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)

country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["Country"].unique().tolist())
)

filtered_df = df.copy()

if year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == year
    ]

if country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == country
    ]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class='hero'>

<div class='hero-title'>
📊 RetailMind Analytics
</div>

<div class='hero-subtitle'>
Customer Intelligence Platform<br>
Transforming Customer Data Into Business Intelligence
</div>

</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTER SUMMARY
# ==================================================

st.markdown(f"""
<div class='insight-box'>

<b>Current Filters</b><br><br>

📅 Year : {year}<br>
🌍 Country : {country}

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# KPI METRICS
# ==================================================

total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Invoice"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
avg_order_value = total_sales / total_orders

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Revenue</div>
        <div class='metric-value'>${total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Orders</div>
        <div class='metric-value'>{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Customers</div>
        <div class='metric-value'>{total_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Avg Order Value</div>
        <div class='metric-value'>${avg_order_value:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==================================================
# REVENUE TREND
# ==================================================

col1, col2 = st.columns(2)

with col1:

    monthly_sales = (
        filtered_df
        .groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="📈 Monthly Revenue Trend"
    )

    fig1.update_layout(
    template="plotly_dark",
    height=450,
    title_x=0.3
)
    

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==================================================
# TOP COUNTRIES
# ==================================================

with col2:

    top_countries = (
        filtered_df
        .groupby("Country")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_countries,
        x="Country",
        y="Sales",
        title="🌍 Top Countries by Revenue"
    )

    fig2.update_layout(
    template="plotly_dark",
    height=450,
    title_x=0.3
)
    

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# TOP PRODUCTS
# ==================================================

top_products = (
    filtered_df
    .groupby("Description")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Sales",
    y="Description",
    orientation="h",
    title="🏆 Top Products"
)

fig3.update_layout(
    template="plotly_dark",
    height=500,
    title_x=0.35
)


st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==================================================
# HEATMAP
# ==================================================

st.subheader("🔥 Revenue by Month Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Sales",
        index="Month",
        columns="Year",
        aggfunc="sum"
    )
)

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="Blues"
)

fig_heatmap.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ==================================================
# DOWNLOAD BUTTON
# ==================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ==================================================
# EXECUTIVE INSIGHTS
# ==================================================

st.subheader("📖 Executive Insights")

top_country = (
    filtered_df
    .groupby("Country")["Sales"]
    .sum()
    .idxmax()
)

top_product = (
    filtered_df
    .groupby("Description")["Sales"]
    .sum()
    .idxmax()
)
top_country_sales = (
    filtered_df
    .groupby("Country")["Sales"]
    .sum()
    .max()
)

st.markdown(f"""
<div class='insight-box'>

<h3>📖 Executive Summary</h3>

🌍 <b>Top Revenue Country:</b> {top_country}<br><br>

💰 <b>Country Revenue:</b> ${top_country_sales:,.0f}<br><br>

🏆 <b>Best Selling Product:</b> {top_product}<br><br>

👥 <b>Active Customers:</b> {total_customers:,}<br><br>

📈 <b>Total Revenue:</b> ${total_sales:,.0f}<br><br>

🛒 <b>Total Orders:</b> {total_orders:,}

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='insight-box'>
<h3>📖 Executive Summary</h3>
🌍 <b>Top Revenue Country:</b> {top_country}<br><br>
💰 <b>Country Revenue:</b> ${top_country_sales:,.0f}<br><br>
🏆 <b>Best Selling Product:</b> {top_product}<br><br>
👥 <b>Active Customers:</b> {total_customers:,}<br><br>
📈 <b>Total Revenue:</b> ${total_sales:,.0f}<br><br>
🛒 <b>Total Orders:</b> {total_orders:,}
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📈",
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
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("📊 EDA Filters")

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].unique().tolist())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["Month"].unique().tolist())
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

if month != "All":
    filtered_df = filtered_df[
        filtered_df["Month"] == month
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
📈 Exploratory Data Analysis
</div>

<div class='hero-subtitle'>
Discover Hidden Patterns, Customer Behaviour & Product Insights
</div>

</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTER SUMMARY
# ==================================================

st.markdown(f"""
<div class='insight-box'>

<h4>🎯 Current Analysis Scope</h4>

📅 Year : {year}<br><br>

🌍 Country : {country}<br><br>

🗓️ Month : {month}

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# SMART ANALYTICS CARDS
# ==================================================

highest_sales_product = (
    filtered_df.groupby("Description")["Sales"]
    .sum()
    .idxmax()
)

highest_sales_month = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .idxmax()
)

top_country = (
    filtered_df.groupby("Country")["Sales"]
    .sum()
    .idxmax()
)

avg_quantity = round(
    filtered_df["Quantity"].mean(),
    2
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "🏆 Top Product",
        highest_sales_product[:20]
    )

with c2:
    st.metric(
        "🌍 Top Country",
        top_country
    )

with c3:
    st.metric(
        "📅 Best Month",
        highest_sales_month
    )

with c4:
    st.metric(
        "🛒 Avg Quantity",
        avg_quantity
    )

st.divider()

# ==================================================
# CUSTOMER BEHAVIOUR ANALYSIS
# ==================================================

st.subheader("🔍 Customer Purchase Behaviour")

fig_scatter = px.scatter(
    filtered_df.sample(
        min(5000, len(filtered_df))
    ),
    x="Quantity",
    y="Sales",
    color="Country",
    title="Quantity vs Sales Relationship",
    opacity=0.7
)

fig_scatter.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ==================================================
# MONTHLY SHOPPING PATTERN
# ==================================================

st.subheader("📈 Monthly Shopping Pattern")

monthly_orders = (
    filtered_df.groupby("Month")["Invoice"]
    .nunique()
    .reset_index()
)

fig_area = px.area(
    monthly_orders,
    x="Month",
    y="Invoice",
    title="Orders Trend Across Months"
)

fig_area.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_area,
    use_container_width=True
)

# ==================================================
# PRODUCT EXPLORER
# ==================================================

st.subheader("📦 Product Explorer")

product_view = st.radio(
    "Choose Analysis",
    ["Top Products", "Bottom Products"],
    horizontal=True
)

if product_view == "Top Products":

    product_data = (
        filtered_df.groupby("Description")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

else:

    product_data = (
        filtered_df.groupby("Description")["Sales"]
        .sum()
        .sort_values(ascending=True)
        .head(15)
        .reset_index()
    )

fig_products = px.bar(
    product_data,
    x="Sales",
    y="Description",
    orientation="h",
    title=product_view
)

fig_products.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)
# ==================================================
# COUNTRY MARKET ANALYSIS
# ==================================================

st.subheader("🌍 Country Market Analysis")

country_sales = (
    filtered_df
    .groupby("Country")["Sales"]
    .sum()
    .reset_index()
)

fig_treemap = px.treemap(
    country_sales,
    path=["Country"],
    values="Sales",
    color="Sales",
    color_continuous_scale="Viridis",
    title="Country Revenue Contribution"
)

fig_treemap.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_treemap,
    use_container_width=True
)

# ==================================================
# DISTRIBUTION LAB
# ==================================================

st.subheader("🧪 Distribution Lab")

tab1, tab2, tab3 = st.tabs(
    [
        "Sales Distribution",
        "Quantity Distribution",
        "Price Distribution"
    ]
)

with tab1:

    fig_sales = px.histogram(
        filtered_df,
        x="Sales",
        nbins=50,
        title="Sales Distribution"
    )

    fig_sales.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

with tab2:

    fig_quantity = px.histogram(
        filtered_df,
        x="Quantity",
        nbins=50,
        title="Quantity Distribution"
    )

    fig_quantity.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True
    )

with tab3:

    fig_price = px.histogram(
        filtered_df,
        x="Price",
        nbins=50,
        title="Price Distribution"
    )

    fig_price.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

# ==================================================
# CORRELATION STUDIO
# ==================================================

st.subheader("🔥 Correlation Studio")

corr_df = filtered_df[
    ["Quantity", "Price", "Sales"]
].corr()

fig_corr = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)

fig_corr.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# ==================================================
# SMART FINDINGS
# ==================================================

st.subheader("💡 Smart Findings")

highest_sales_month = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .idxmax()
)

best_country = (
    filtered_df
    .groupby("Country")["Sales"]
    .sum()
    .idxmax()
)

best_product = (
    filtered_df
    .groupby("Description")["Sales"]
    .sum()
    .idxmax()
)

avg_order_value = round(
    filtered_df["Sales"].mean(),
    2
)

st.markdown(f"""
<div class='insight-box'>

<h3>📖 Automated Business Findings</h3>

📅 <b>Best Performing Month:</b> {highest_sales_month}<br><br>

🌍 <b>Strongest Market:</b> {best_country}<br><br>

🏆 <b>Most Purchased Product:</b> {best_product}<br><br>

💰 <b>Average Transaction Value:</b> ${avg_order_value:,.2f}<br><br>

📈 <b>Observation:</b><br>
Countries with higher order volumes contribute significantly to total revenue.

</div>
""", unsafe_allow_html=True)

# ==================================================
# DATA EXPLORER
# ==================================================

st.subheader("📋 Dataset Explorer")

search_product = st.text_input(
    "Search Product"
)

display_df = filtered_df.copy()

if search_product:

    display_df = display_df[
        display_df["Description"]
        .astype(str)
        .str.contains(
            search_product,
            case=False,
            na=False
        )
    ]

st.dataframe(
    display_df.head(500),
    use_container_width=True
)

# ==================================================
# DOWNLOAD DATA
# ==================================================

st.subheader("⬇ Download Center")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download EDA Dataset",
    data=csv,
    file_name="eda_filtered_data.csv",
    mime="text/csv"
)
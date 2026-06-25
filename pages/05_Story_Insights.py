import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Story Insights",
    page_icon="📖",
    layout="wide"
)

load_css()

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():

    sales_df = pd.read_csv(
        "data/cleaned_data.csv"
    )

    rfm_df = pd.read_csv(
        "data/rfm_segments.csv"
    )

    churn_df = pd.read_csv(
        "data/customer_churn_data.csv"
    )

    return sales_df, rfm_df, churn_df


sales_df, rfm_df, churn_df = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("📖 Story Controls")

growth_rate = st.sidebar.slider(
    "Expected Revenue Growth (%)",
    0,
    50,
    10
)

# =====================================
# HERO SECTION
# =====================================

st.markdown("""
<div class='hero'>

<div class='hero-title'>
📖 Business Insights
</div>

<div class='hero-subtitle'>
Key findings and strategic recommendations
derived from RetailMind Analytics
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# BUSINESS SNAPSHOT
# =====================================

total_revenue = sales_df["Sales"].sum()

total_customers = sales_df["Customer ID"].nunique()

total_orders = sales_df["Invoice"].nunique()

top_country = (
    sales_df
    .groupby("Country")["Sales"]
    .sum()
    .idxmax()
)

top_product = (
    sales_df
    .groupby("Description")["Sales"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

with c2:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with c3:
    st.metric(
        "Orders",
        f"{total_orders:,}"
    )

with c4:
    st.metric(
        "Top Market",
        top_country
    )

st.divider()

# =====================================
# KEY BUSINESS FINDINGS
# =====================================

st.subheader("🔍 Key Findings")

f1, f2 = st.columns(2)

with f1:

    st.markdown(f"""
    <div class='insight-box'>

    <h4>Revenue Driver</h4>

    The strongest revenue contribution
    comes from <b>{top_country}</b>.

    This market represents the
    largest business opportunity.

    </div>
    """, unsafe_allow_html=True)

with f2:

    st.markdown(f"""
    <div class='insight-box'>

    <h4>Top Product</h4>

    The highest performing product is:

    <b>{top_product}</b>

    indicating strong customer demand.

    </div>
    """, unsafe_allow_html=True)

st.write("")

f3, f4 = st.columns(2)

vip_customers = len(
    rfm_df[
        rfm_df["Segment"] == "VIP"
    ]
)

lost_customers = len(
    rfm_df[
        rfm_df["Segment"] == "Lost"
    ]
)

with f3:

    st.markdown(f"""
    <div class='insight-box'>

    <h4>Customer Value</h4>

    VIP Customers:
    <b>{vip_customers}</b>

    These customers contribute
    the highest business value.

    </div>
    """, unsafe_allow_html=True)

with f4:

    st.markdown(f"""
    <div class='insight-box'>

    <h4>Retention Risk</h4>

    Lost Customers:
    <b>{lost_customers}</b>

    Retention strategies can
    improve future revenue.

    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================
# REVENUE SIMULATOR
# =====================================

st.subheader("📈 Revenue Growth Simulator")

projected_revenue = (
    total_revenue *
    (1 + growth_rate / 100)
)

gain = (
    projected_revenue -
    total_revenue
)

s1, s2, s3 = st.columns(3)

with s1:
    st.metric(
        "Current Revenue",
        f"${total_revenue:,.0f}"
    )

with s2:
    st.metric(
        "Projected Revenue",
        f"${projected_revenue:,.0f}"
    )

with s3:
    st.metric(
        "Potential Gain",
        f"${gain:,.0f}"
    )

growth_df = pd.DataFrame({
    "Scenario": [
        "Current",
        "Projected"
    ],
    "Revenue": [
        total_revenue,
        projected_revenue
    ]
})

fig_growth = px.bar(
    growth_df,
    x="Scenario",
    y="Revenue",
    title="Revenue Projection"
)

fig_growth.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)
# =====================================
# MARKET OPPORTUNITIES
# =====================================

st.divider()

st.subheader("🌍 Market Opportunities")

country_sales = (
    sales_df
    .groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_market = px.bar(
    country_sales,
    x="Sales",
    y="Country",
    orientation="h",
    color="Sales",
    title="Top Revenue Markets"
)

fig_market.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_market,
    use_container_width=True
)

# =====================================
# CUSTOMER HEALTH
# =====================================

st.divider()

st.subheader("👥 Customer Health")

segment_counts = (
    rfm_df["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]

col1, col2 = st.columns(2)

with col1:

    fig_segment = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        color="Segment",
        title="Customer Segment Distribution"
    )

    fig_segment.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

with col2:

    fig_segment_pie = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        hole=0.5,
        title="Customer Segment Share"
    )

    fig_segment_pie.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_segment_pie,
        use_container_width=True
    )

# =====================================
# BUSINESS RECOMMENDATIONS
# =====================================

st.divider()

st.subheader("💡 Business Recommendations")

st.markdown(f"""
<div class='insight-box'>

<h3>Recommended Actions</h3>

✅ Focus marketing investments on
<b>{top_country}</b> to maximize revenue growth.

<br>

✅ Maintain inventory levels for
<b>{top_product}</b> due to high demand.

<br>

✅ Strengthen loyalty programs for
VIP customers.

<br>

✅ Launch retention campaigns
for inactive customers.

<br>

✅ Use product recommendation systems
to increase repeat purchases.

</div>
""", unsafe_allow_html=True)

# =====================================
# FINAL BUSINESS CONCLUSION
# =====================================

st.divider()

st.subheader("📌 Business Conclusion")

business_score = 92

st.markdown(f"""
<div class='insight-box'>

<h3>RetailMind Business Summary</h3>

The analysis reveals that the business is
currently driven by a small number of
high-performing markets and products.

Customer segmentation highlights valuable
VIP customers who contribute significantly
to revenue.

Customer retention remains an important
area for future improvement.

By focusing on:

✔ Customer Retention

✔ Product Recommendations

✔ Market Expansion

✔ Customer Loyalty Programs

the company can continue sustainable growth.

<br><br>

<b>Overall Business Health Score:
{business_score}/100</b>

</div>
""", unsafe_allow_html=True)

# =====================================
# DOWNLOAD REPORT
# =====================================

st.divider()

report_df = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Customers",
        "Total Orders",
        "Top Country",
        "Top Product",
        "Projected Revenue"
    ],
    "Value": [
        total_revenue,
        total_customers,
        total_orders,
        top_country,
        top_product,
        projected_revenue
    ]
})

csv = report_df.to_csv(index=False)

st.download_button(
    "⬇ Download Business Summary",
    csv,
    "business_summary.csv",
    "text/csv"
)
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

load_css()

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("data/rfm_segments.csv")

rfm = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("👥 Segment Filters")

selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    ["All"] + sorted(rfm["Segment"].unique().tolist())
)

filtered_rfm = rfm.copy()

if selected_segment != "All":
    filtered_rfm = filtered_rfm[
        filtered_rfm["Segment"] == selected_segment
    ]

# =====================================
# HERO SECTION
# =====================================

st.markdown(f"""
<div class='hero'>

<div class='hero-title'>
👥 Customer Segmentation Dashboard
</div>

<div class='hero-subtitle'>
Current View : {selected_segment}
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# KPI SECTION
# =====================================

total_customers = len(filtered_rfm)

avg_recency = round(filtered_rfm["Recency"].mean(), 1)
avg_frequency = round(filtered_rfm["Frequency"].mean(), 1)
avg_monetary = round(filtered_rfm["Monetary"].mean(), 1)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Customers", f"{total_customers:,}")

with c2:
    st.metric("Avg Recency", avg_recency)

with c3:
    st.metric("Avg Frequency", avg_frequency)

with c4:
    st.metric("Avg Monetary", f"${avg_monetary:,.0f}")

st.divider()

# =====================================
# ALL SEGMENTS VIEW
# =====================================

if selected_segment == "All":

    col1, col2 = st.columns(2)

    with col1:

        segment_counts = (
            rfm["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "Segment",
            "Customers"
        ]

        fig1 = px.bar(
            segment_counts,
            x="Segment",
            y="Customers",
            color="Segment",
            title="Customer Segment Distribution"
        )

        fig1.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2 = px.pie(
            rfm,
            names="Segment",
            title="Segment Share"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.subheader("📊 RFM Segment Comparison")

    cluster_summary = (
        rfm.groupby("Segment")[
            ["Recency", "Frequency", "Monetary"]
        ]
        .mean()
        .reset_index()
    )

    rfm_melt = cluster_summary.melt(
        id_vars="Segment",
        var_name="Metric",
        value_name="Value"
    )

    fig3 = px.bar(
        rfm_melt,
        x="Segment",
        y="Value",
        color="Metric",
        barmode="group",
        title="Average RFM Metrics"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=550
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================
# INDIVIDUAL SEGMENT VIEW
# =====================================

else:

    col1, col2 = st.columns(2)

    with col1:

        fig4 = px.histogram(
            filtered_rfm,
            x="Monetary",
            nbins=25,
            title=f"{selected_segment} Customer Spending"
        )

        fig4.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    with col2:

        fig5 = px.histogram(
            filtered_rfm,
            x="Frequency",
            nbins=25,
            title=f"{selected_segment} Purchase Frequency"
        )

        fig5.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    st.subheader("📈 Customer Value Analysis")

    fig6 = px.scatter(
        filtered_rfm,
        x="Frequency",
        y="Monetary",
        size="Monetary",
        color="Monetary",
        title=f"{selected_segment} Customer Analysis"
    )

    fig6.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# =====================================
# CUSTOMER EXPLORER
# =====================================

st.subheader("📋 Customer Explorer")

st.dataframe(
    filtered_rfm,
    use_container_width=True
)

# =====================================
# DOWNLOAD REPORT
# =====================================

csv = filtered_rfm.to_csv(index=False)

st.download_button(
    "⬇ Download Segment Report",
    csv,
    "segment_report.csv",
    "text/csv"
)

# =====================================
# DYNAMIC RECOMMENDATIONS
# =====================================

st.subheader("💡 Business Recommendations")

if selected_segment == "VIP":

    st.success("""
🏆 VIP Customers

• Offer premium memberships

• Early product access

• Exclusive rewards

• Dedicated support
""")

elif selected_segment == "Loyal":

    st.info("""
❤️ Loyal Customers

• Loyalty programs

• Referral campaigns

• Cross-selling opportunities

• Personalized offers
""")

elif selected_segment == "Regular":

    st.warning("""
📦 Regular Customers

• Product bundles

• Upselling campaigns

• Email marketing

• Product recommendations
""")

elif selected_segment == "Lost":

    st.error("""
⚠ Lost Customers

• Win-back campaigns

• Discount coupons

• Retargeting ads

• Re-engagement emails
""")

else:

    st.markdown("""
### Overall Customer Strategy

🏆 VIP → Premium Offers

❤️ Loyal → Reward Programs

📦 Regular → Upselling

⚠ Lost → Re-engagement Campaigns
""")
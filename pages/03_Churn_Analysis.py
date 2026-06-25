import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

st.set_page_config(
    page_title="Churn Analysis",
    page_icon="⚠️",
    layout="wide"
)

load_css()

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("data/customer_churn_data.csv")

df = load_data()

# =====================================
# SIDEBAR FILTER
# =====================================

st.sidebar.header("⚠️ Churn Filters")

status = st.sidebar.selectbox(
    "Customer Status",
    ["All", "Retained", "Churned"]
)

filtered_df = df.copy()

if status == "Retained":
    filtered_df = filtered_df[filtered_df["Churn"] == 0]

elif status == "Churned":
    filtered_df = filtered_df[filtered_df["Churn"] == 1]

# =====================================
# HERO SECTION
# =====================================

st.markdown(f"""
<div class='hero'>

<div class='hero-title'>
⚠️ Customer Churn Analysis
</div>

<div class='hero-subtitle'>
Current View : {status}
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# KPI SECTION
# =====================================

total_customers = len(filtered_df)

churn_customers = len(
    filtered_df[filtered_df["Churn"] == 1]
)

retained_customers = len(
    filtered_df[filtered_df["Churn"] == 0]
)

churn_rate = (
    churn_customers / total_customers * 100
    if total_customers > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with c2:
    st.metric(
        "Churned",
        f"{churn_customers:,}"
    )

with c3:
    st.metric(
        "Retained",
        f"{retained_customers:,}"
    )

with c4:
    st.metric(
        "Churn Rate",
        f"{churn_rate:.1f}%"
    )

st.divider()

# =====================================
# CHURN DISTRIBUTION
# =====================================

col1, col2 = st.columns(2)

with col1:

    churn_counts = (
        filtered_df["Churn"]
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Status",
        "Customers"
    ]

    churn_counts["Status"] = churn_counts["Status"].map({
        0: "Retained",
        1: "Churned"
    })

    fig1 = px.bar(
        churn_counts,
        x="Status",
        y="Customers",
        color="Status",
        title="Customer Status Distribution"
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

    pie_df = churn_counts.copy()

    fig2 = px.pie(
        pie_df,
        names="Status",
        values="Customers",
        title="Churn Percentage"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================
# CUSTOMER VALUE ANALYSIS
# =====================================

if "Monetary" in filtered_df.columns:

    st.subheader("💰 Customer Value Analysis")

    fig3 = px.box(
        filtered_df,
        x="Churn",
        y="Monetary",
        color="Churn",
        title="Customer Value Comparison"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================
# CUSTOMER TABLE
# =====================================

st.subheader("📋 Customer Explorer")

st.dataframe(
    filtered_df.head(500),
    use_container_width=True
)

# =====================================
# DOWNLOAD REPORT
# =====================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Churn Report",
    csv,
    "churn_report.csv",
    "text/csv"
)

# =====================================
# BUSINESS INSIGHTS
# =====================================

st.subheader("💡 Churn Risk Insights")

if churn_rate > 50:

    st.error("""
🚨 High Churn Risk

• More than half of customers have churned.

• Immediate retention campaigns required.

• Offer discounts and loyalty incentives.

• Focus on customer satisfaction.
""")

elif churn_rate > 30:

    st.warning("""
⚠ Moderate Churn Risk

• Customer churn is noticeable.

• Strengthen retention programs.

• Launch targeted marketing campaigns.

• Improve customer engagement.
""")

else:

    st.success("""
✅ Healthy Customer Base

• Strong customer retention.

• Continue loyalty initiatives.

• Focus on customer experience.

• Monitor churn regularly.
""")
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Recommendation System",
    page_icon="🛍",
    layout="wide"
)

load_css()

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():

    customer_product_matrix = pd.read_csv(
        "data/customer_product_matrix.csv",
        index_col=0
    )

    similarity_df = pd.read_csv(
        "data/customer_similarity.csv",
        index_col=0
    )

    return customer_product_matrix, similarity_df


customer_product_matrix, similarity_df = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("🛍 Recommendation Controls")

customer_id = st.sidebar.selectbox(
    "Select Customer",
    customer_product_matrix.index.tolist()
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    5,
    20,
    10
)

# =====================================
# HERO
# =====================================

st.markdown(f"""
<div class='hero'>

<div class='hero-title'>
🛍 Product Recommendation Engine
</div>

<div class='hero-subtitle'>
Personalized product recommendations
based on customer purchasing behaviour
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# CUSTOMER SUMMARY
# =====================================

st.subheader("👤 Customer Analysis")

customer_products = (
    customer_product_matrix
    .loc[customer_id]
)

customer_products = customer_products[
    customer_products > 0
]

products_bought = len(customer_products)

total_quantity = int(
    customer_products.sum()
)

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Products Purchased",
        products_bought
    )

with c2:

    st.metric(
        "Total Purchase Quantity",
        total_quantity
    )

# =====================================
# CUSTOMER PURCHASE PROFILE
# =====================================

st.subheader("📦 Purchase Profile")

profile_df = (
    customer_products
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

profile_df.columns = [
    "Product",
    "Purchases"
]

fig_profile = px.bar(
    profile_df,
    x="Purchases",
    y="Product",
    orientation="h",
    title="Most Purchased Products"
)

fig_profile.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_profile,
    use_container_width=True
)

# =====================================
# SIMILAR CUSTOMERS
# =====================================

similar_customers = (
    similarity_df[str(customer_id)]
    .sort_values(
        ascending=False
    )
    .iloc[1:6]
)

st.subheader("👥 Similar Customers")

similar_df = pd.DataFrame({
    "Customer ID":
    similar_customers.index,

    "Similarity":
    similar_customers.values
})

fig_similar = px.bar(
    similar_df,
    x="Customer ID",
    y="Similarity",
    color="Similarity",
    title="Customer Similarity Scores"
)

fig_similar.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_similar,
    use_container_width=True
)

st.dataframe(
    similar_df,
    use_container_width=True
)
# =====================================
# AI RECOMMENDED PRODUCTS
# =====================================

st.subheader("🎯 Recommended Products")

recommended_products = (
    customer_product_matrix
    .loc[
        similar_customers.index
    ]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(top_n)
)

rec_df = pd.DataFrame({
    "Product":
    recommended_products.index,

    "Recommendation Score":
    recommended_products.values
})

fig_rec = px.bar(
    rec_df,
    x="Recommendation Score",
    y="Product",
    orientation="h",
    color="Recommendation Score",
    title=f"Top {top_n} Product Recommendations"
)

fig_rec.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_rec,
    use_container_width=True
)

# =====================================
# RECOMMENDATION CONFIDENCE
# =====================================

st.subheader("📊 Recommendation Confidence")

confidence_score = round(
    similar_customers.mean() * 100,
    1
)

st.progress(
    min(
        int(confidence_score),
        100
    )
)

st.write(
    f"Recommendation Confidence: {confidence_score}%"
)

# =====================================
# CROSS SELLING OPPORTUNITIES
# =====================================

st.subheader("🛒 Cross-Selling Opportunities")

cross_sell_df = rec_df.head(5)

fig_cross = px.pie(
    cross_sell_df,
    names="Product",
    values="Recommendation Score",
    hole=0.5,
    title="Top Cross-Selling Products"
)

fig_cross.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_cross,
    use_container_width=True
)

# =====================================
# RECOMMENDATION TABLE
# =====================================

st.subheader("📋 Recommendation Results")

st.dataframe(
    rec_df,
    use_container_width=True
)

# =====================================
# RECOMMENDATION SUMMARY
# =====================================

st.subheader("💡 Recommendation Summary")

top_product = rec_df.iloc[0]["Product"]

highest_similarity = round(
    similar_customers.iloc[0],
    2
)

st.markdown(f"""
<div class='insight-box'>

<h3>Recommendation Findings</h3>

👤 Selected Customer:
<b>{customer_id}</b>

<br><br>

🤝 Highest Similarity Score:
<b>{highest_similarity}</b>

<br><br>

🏆 Top Recommended Product:
<b>{top_product}</b>

<br><br>

📦 Total Recommendations:
<b>{len(rec_df)}</b>

<br><br>

📈 Recommendations are generated
using customer-to-customer
collaborative filtering.

<br><br>

🎯 Business Use Cases:

• Personalized Marketing

• Product Cross-Selling

• Customer Retention

• Revenue Growth

</div>
""", unsafe_allow_html=True)

# =====================================
# DOWNLOAD RECOMMENDATIONS
# =====================================

st.subheader("⬇ Download Recommendations")

csv = rec_df.to_csv(
    index=False
)

st.download_button(
    label="Download Recommendation Report",
    data=csv,
    file_name="recommendation_report.csv",
    mime="text/csv"
)
import streamlit as st


def load_css():

    st.markdown("""
<style>

/* ==========================================
   GLOBAL
========================================== */

html,
body,
[class*="css"]{
    font-family:'Segoe UI',sans-serif;
}

.stApp{
    background:#0E1117;
    color:#FFFFFF;
}
section.main{
    color:white !important;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* ==========================================
   TEXT COLORS
========================================== */

h1,h2,h3,h4,h5,h6{
    color:#FFFFFF !important;
    font-weight:700 !important;
}

p{
    color:#E5E7EB !important;
}

strong,b{
    color:#FFFFFF !important;
}

label{
    color:#FFFFFF !important;
}

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6{
    color:white !important;
}

/* ==========================================
   SIDEBAR
========================================== */

[data-testid="stSidebar"]{
    background:#151B27;
    border-right:1px solid #293548;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label{
    color:white !important;
}

/* ==========================================
   HERO SECTION
========================================== */

.hero{

    background:linear-gradient(
        135deg,
        #1A2238,
        #2C3E5D
    );

    border-radius:22px;

    padding:35px;

    margin-bottom:25px;

    box-shadow:
    0 10px 35px rgba(0,0,0,.35);
}

.hero-title{
    font-size:48px;
    font-weight:800;
    color:#FFFFFF !important;
    line-height:1.2;
    margin-bottom:10px;
}

.hero-subtitle{
    font-size:19px;
    color:#D1D5DB !important;
    line-height:1.7;
}

/* ==========================================
   KPI CARDS
========================================== */

.metric-box{

    background:linear-gradient(
        135deg,
        #1C2435,
        #273752
    );

    padding:22px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:
    0 8px 24px rgba(0,0,0,.35);

    transition:.3s;
}

.metric-box:hover{

    transform:translateY(-5px);

    box-shadow:
    0 12px 28px rgba(0,229,255,.18);
}

.metric-title{
    color:#CBD5E1 !important;
    font-size:15px;
    font-weight:600;
}

.metric-value{
    color:#FFFFFF !important;
    font-size:34px;
    font-weight:800;
}

/* Streamlit metric */

[data-testid="stMetric"]{

    background:#1C2435;

    padding:18px;

    border-radius:16px;

    border:1px solid rgba(255,255,255,.06);
}

[data-testid="stMetricValue"]{

    color:white !important;

    font-size:30px;

    font-weight:700;
}

[data-testid="stMetricLabel"]{

    color:#E5E7EB !important;
    font-size:16px;
    font-weight:600;
}
st.title()

st.header()

st.subheader()
/* ==========================================
   INSIGHT CARDS
========================================== */

.insight-box{
    background:#1B2233;
    border-left:6px solid #00D9FF;
    border-radius:18px;
    padding:25px;
    margin:15px 0;
}

.insight-box *{
    color:#FFFFFF !important;
    opacity:1 !important;
}

.insight-box p{
    color:#E5E7EB !important;
}


/* ==========================================
   BUTTONS
========================================== */

.stButton > button{

    width:100%;

    border-radius:12px;

    border:none;

    background:#00BCD4;

    color:white;

    font-weight:600;

    padding:.7rem;

    transition:.3s;
}

.stButton > button:hover{

    background:#0097A7;

    transform:translateY(-2px);
}

/* ==========================================
   DOWNLOAD BUTTON
========================================== */

.stDownloadButton > button{

    width:100%;

    border-radius:12px;

    border:none;

    background:#4CAF50;

    color:white;

    font-weight:600;

    padding:.7rem;
}

.stDownloadButton > button:hover{

    background:#2E7D32;
}

/* ==========================================
   SELECTBOXES
========================================== */

.stSelectbox label{

    color:white !important;

    font-weight:600;
}

/* ==========================================
   DATAFRAME
========================================== */

[data-testid="stDataFrame"]{

    border-radius:15px;

    overflow:hidden;

    border:1px solid rgba(255,255,255,.08);
}

/* ==========================================
   TABLES
========================================== */

table{

    color:white !important;
}

/* ==========================================
   PLOTLY CHARTS
========================================== */

.js-plotly-plot{

    border-radius:18px;

    overflow:hidden;

    background:#1A2238;

    padding:8px;
}

/* ==========================================
   DIVIDER
========================================== */

hr{

    border:0;

    height:1px;

    background:#2C3445;

    margin:25px 0;
}

/* ==========================================
   SCROLLBAR
========================================== */

::-webkit-scrollbar{

    width:10px;
}

::-webkit-scrollbar-track{

    background:#151B27;
}

::-webkit-scrollbar-thumb{

    background:#3A4A63;

    border-radius:20px;
}

::-webkit-scrollbar-thumb:hover{

    background:#4F6382;
}

/* ==========================================
   SUCCESS / WARNING / ERROR
========================================== */

[data-testid="stAlert"]{

    border-radius:14px;

    border:none;
}

/* ==========================================
   CAPTION
========================================== */

.caption{

    color:#C6CFDD;
}

/* ==========================================
   FOOTER
========================================== */

footer{

    visibility:hidden;
}

header{

    background:transparent;
}

</style>
""", unsafe_allow_html=True)
import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .stApp{
        background-color:#0E1117;
    }

    .block-container{
        padding-top:1rem;
        padding-bottom:1rem;
    }

    .hero{
        background: linear-gradient(
            135deg,
            #1A1F2E,
            #243B55
        );

        padding:35px;
        border-radius:20px;
        margin-bottom:25px;

        box-shadow:
        0 8px 32px rgba(0,0,0,0.3);
    }

    .hero-title{
        font-size:48px;
        font-weight:700;
        color:white;
    }

    .hero-subtitle{
        font-size:18px;
        color:#B0BEC5;
    }

    .metric-box{
    background: linear-gradient(
        135deg,
        #1A1F2E,
        #243B55
    );

    padding:20px;
    border-radius:18px;
    text-align:center;

    box-shadow:
    0 8px 20px rgba(0,0,0,0.3);

    border:1px solid rgba(255,255,255,0.08);
}
    }

    .metric-title{
        color:#B0BEC5;
        font-size:15px;
    }

    .metric-value{
        color:white;
        font-size:30px;
        font-weight:bold;
    }

    .insight-box{
        background:#1A1F2E;
        padding:20px;
        border-radius:15px;
        border-left:5px solid #00E5FF;
        margin-top:15px;
    }

    </style>
    """,
    unsafe_allow_html=True)
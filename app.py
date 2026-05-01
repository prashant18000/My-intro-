import streamlit as st

# Page configuration
st.set_page_config(page_title="Mr. Futuristic", layout="centered")

# CSS for moving background and glowing box
st.markdown("""
<style>
    /* Moving Dots Background (Yellowish lights) */
    .stApp {
        background-color: #0e1117;
        background-image: radial-gradient(circle, rgba(255, 255, 0, 0.4) 1px, transparent 1px);
        background-size: 40px 40px;
        animation: moveDots 20s linear infinite;
    }
    @keyframes moveDots {
        from { background-position: 0 0; }
        to { background-position: 1000px 1000px; }
    }

    /* Inbox with Grassy Green Neon Border */
    .intro-box {
        border: 2px solid #7CFC00;
        border-radius: 15px;
        padding: 30px;
        background: rgba(0, 0, 0, 0.85);
        box-shadow: 0 0 15px #7CFC00, inset 0 0 10px #7CFC00;
        color: white;
        text-align: left;
        max-width: 500px;
        margin: auto;
    }

    /* Line by line structure */
    .line {
        margin-bottom: 20px;
        font-size: 1.3rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-left: 3px solid #7CFC00;
        padding-left: 15px;
    }

    .highlight {
        color: #7CFC00;
        font-weight: bold;
    }
</style>

<div class="intro-box">
    <div class="line">👤 Name: <span class="highlight">☠️𝓜𝓻. 𝓯𝓾𝓽𝓾𝓻𝓲𝓼𝓽𝓲𝓬 ☠️</span></div>
    <div class="line">🔗 Username: <span class="highlight">@descent_boyy</span></div>
    <div class="line">🎂 Age: <span class="highlight">jaankar kya karoge 😏</span></div>
</div>
""", unsafe_allow_html=True)

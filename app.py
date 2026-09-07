import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="OmniSales AI - Multi-Platform Sales Suite",
    page_icon="⚡",
    layout="wide",
)

API_KEY = "AQ.Ab8RN6L8itVMEbft3uUbpadXgkQWB4ERXH0pZnSF6fGmcg9qdA"
genai.configure(api_key=API_KEY)

st.sidebar.title("⚡ OmniSales AI")
st.sidebar.caption("SaaS AI Agent Management Portal")

# Rent / Plan Status in Sidebar
st.sidebar.divider()
st.sidebar.subheader("💳 Active Subscription")
st.sidebar.success("Pro Plan (₹2,999/mo) - Active")
st.sidebar.caption("Next Billing Date: 07 Oct 2026")

if "shop_info" not in st.session_state:
    st.session_state.shop_info = {
        "business_name": "TechPulse Electronics",
        "product_details": "Smart Wireless Earbuds with ANC, 40hr Battery, Price: ₹2,499",
        "agent_name": "Rohan Malhotra",
        "agent_role": "Senior Sales Specialist",
    }

tab1, tab2, tab3 = st.tabs(
    [
        "🏪 1. Business Setup",
        "🌐 2. Multi-Platform Keys",
        "💬 3. Agent Simulator",
    ]
)

# TAB 1: BUSINESS SETUP
with tab1:
    st.header("🏪 Dukandar Profile Setup")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.shop_info["business_name"] = st.text_input(
            "Business / Shop Name",
            value=st.session_state.shop_info["business_name"],
        )
        st.session_state.shop_info["agent_name"] = st.text_input(
            "Salesman Ka Naam", value=st.session_state.shop_info["agent_name"]
        )
        st.session_state.shop_info["agent_role"] = st.text_input(
            "Salesman Designation",
            value=st.session_state.shop_info["agent_role"],
        )
    with col2:
        st.session_state.shop_info["product_details"] = st.text_area(
            "Product Details & Pricing",
            value=st.session_state.shop_info["product_details"],
            height=110,
        )

# TAB 2: CREDENTIALS & PLATFORMS
with tab2:
    st.header("🌐 Connect Business Platforms")
    st.write("Apne platforms connect karne ke liye credentials enter karein:")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📱 WhatsApp Business (Twilio/Meta)")
        wa_enable = st.toggle("Enable WhatsApp Integration")
        if wa_enable:
            st.text_input("WhatsApp Business Phone Number", placeholder="+91 9876543210")
            st.text_input("Meta / Twilio Auth Token", type="password")

        st.subheader("💬 Website Chat Widget")
        st.code("<script src='https://omnisales.ai/widget.js'></script>", language="html")
        st.caption("Yeh script dukandar apni website me paste karega.")

    with col_b:
        st.subheader("📧 Email Automation (SMTP)")
        em_enable = st.toggle("Enable Cold Email Agent")
        if em_enable:
            st.text_input("Business Email ID", placeholder="sales@yourshop.com")
            st.text_input("SMTP App Password", type="password")

# TAB 3: SIMULATOR
with tab3:
    agent_n = st.session_state.shop_info["agent_name"]
    biz_n = st.session_state.shop_info["business_name"]
    st.subheader(f"🟢 {agent_n} - {st.session_state.shop_info['agent_role']}")

    SYSTEM_PROMPT = f"""
    Aapka naam '{agent_n}' hai, aap '{biz_n}' ke Senior Sales Executive hain.
    Product Info: {st.session_state.shop_info['product_details']}
    User jis language me bole, natural human style me reply de aur sale close karne ki koshish karein.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT
    )

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    if "sim_messages" not in st.session_state:
        st.session_state.sim_messages = [
            {"role": "assistant", "content": f"Hey! I'm {agent_n} from {biz_n}. How can I help you today?"}
        ]

    for msg in st.session_state.sim_messages:
        avatar = "👤" if msg["role"] == "user" else "👨‍💼"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    if user_input := st.chat_input(f"Message {agent_n}..."):
        st.session_state.sim_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        response = st.session_state.chat_session.send_message(user_input)
        st.session_state.sim_messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant", avatar="👨‍💼"):
            st.write(response.text)
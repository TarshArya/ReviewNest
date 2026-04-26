import streamlit as st

st.set_page_config(
    page_title="ReviewNest",
    page_icon="🛍️",
    layout="wide"
)

with st.sidebar:
    st.image("assets/reviewnest_logo.png", width=190)
    st.markdown("###")
    st.page_link("0_Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Search_Reviews.py", label="Search Reviews", icon="🔍")
    st.page_link("pages/2_Compare_Products.py", label="Compare Products", icon="⚖️")

st.title("ReviewNest")
st.write("Search real products, read reviews, get AI summaries, and compare products.")

st.markdown("## Choose a feature")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🔍 Search Reviews")
        st.write("Search one product and view real customer reviews with AI summary.")
        st.page_link("pages/1_Search_Reviews.py", label="Open Search Reviews")

with col2:
    with st.container(border=True):
        st.subheader("⚖️ Compare Products")
        st.write("Compare two products side by side using review-based insights.")
        st.page_link("pages/2_Compare_Products.py", label="Open Compare Products")
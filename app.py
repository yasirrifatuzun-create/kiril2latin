import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="KIRIL2LATIN", layout="wide")

# BU CSS, butonun kimliğine bakmadan sayfadaki tüm butonları zorlar
st.markdown("""
<style>
button {
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}
</style>
""", unsafe_allow_html=True)

# ... (Kodun geri kalanı aynı)

st.markdown("""
<style>
/* 1. Tüm butonların boyutunu sabitle (Kare yapı) */
div[data-testid="stColumn"] button {
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important; /* Esnemeyi engeller */
    padding: 0 !important;
    margin: 2px !important;
    /* Butonun içini hizalamaya hazırla */
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* 2. Buton içindeki metni (p etiketi) tam ortaya kilitler */
div[data-testid="stColumn"] button p {
    margin: 0 !important;
    line-height: 1 !important; /* Satır yüksekliğini sıfırla */
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    height: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Butonları zorla kare ve ortalı yap */
    div[data-testid="stColumn"] button {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 45px !important;  /* Genişliği sabitledik */
        height: 45px !important; /* Yüksekliği genişlikle aynı yaptık (KARE) */
        padding: 0 !important;
        margin: 2px !important;
        min-width: 45px !important;
    }
    /* Harfi butonun içinde merkeze tam oturt */
    div[data-testid="stColumn"] button p {
        margin: 0 !important;
        font-weight: bold !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    </style>
""", unsafe_allow_html=True)

import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="KIRIL2LATIN", layout="wide")

# Sadece butonların boyutlarını sabitleyen, yerleşimi bozmayan minimal CSS
st.markdown("""
    <style>
    /* Klavye buton sabitleme */
    .stButton > button {
        width: 44px !important;
        height: 44px !important;
        padding: 0px !important;
        margin: 2px !important;
        font-size: 16px !important;
    }
    /* Sağdaki işlem butonlarını normal boyutuna getirir */
    div[data-testid="stColumn"] .stButton > button {
        width: 100% !important;
        height: 45px !important;
    }
    </style>
""", unsafe_allow_html=True)

RUSCA_KIRIL_TABLO = {
    'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
    'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd', 'Е': 'Ye', 'е': 'ye',
    'Ё': 'Yo', 'ё': 'yo', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z',
    'И': 'İ', 'и': 'i', 'Й': 'Y', 'й': 'y', 'К': 'K', 'к': 'k',
    'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n',
    'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r',
    'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u',
    'Ф': 'F', 'ф': 'f', 'Х': 'H', 'х': 'h', 'Ц': 'Ts', 'ц': 'ts',
    'Ч': 'Ç', 'ч': 'ç', 'Ш': 'Ş', 'ш': 'ş', 'Щ': 'Şç', 'щ': 'şç',
    'Ъ': "'", 'ъ': "'", 'Ы': 'I', 'ы': 'ı', 'Ь': "^", 'ь': "^",
    'Э': 'E', 'э': 'e', 'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya', 'я': 'ya'
}

if "kiril_text" not in st.session_state:
    st.session_state["kiril_text"] = ""
if "latin_text" not in st.session_state:
    st.session_state["latin_text"] = ""
if "audio_data" not in st.session_state:
    st.session_state["audio_data"] = None

def harf_bas(h):
    st.session_state["kiril_text"] += h

st.title("KIRIL2LATIN - Transliterasyon")

sol, sag = st.columns([1, 1])

with sol:
    st.write("Kiril Alfabe - Sanal Klavye")
    
    # Harfler tamamen orijinal Kiril karakterleridir
    satirlar = [
        ["А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д", "Е", "е", "Ё", "ё"],
        ["Ж", "ж", "З", "z", "И", "и", "Й", "й", "К", "к", "Л", "л", "М", "м"],
        ["Н", "н", "О", "о", "П", "п", "Р", "р", "С", "с", "Т", "т", "У", "у"],
        ["Ф", "ф", "Х", "x", "Ц", "ц", "Ч", "ч", "Ш", "ш", "Щ", "щ", "Ъ", "ъ"],
        ["Ы", "ы", "Ь", "ь", "Э", "э", "Ю", "ю", "Я", "я"]
    ]
    
    # Esnemeyi önleyen tek parça container yapısı
    for satir in satirlar:
        container = st.container()
        with container:
            html_kod = ""
            for harf in satir:
                st.button(harf, key=f"k_{harf}_{satirlar.index(satir)}", on_click=harf_bas, args=(harf,))

with sag:
    girdi = st.text_area("Kiril Metin Girişi:", value=st.session_state["kiril_text"], height=150, key="ana_girdi")
    st.session_state["kiril_text"] = girdi
    
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Dönüştür", type="primary"):
            sonuc = ""
            for k in st.session_state["kiril_text"]:
                sonuc += RUSCA_KIRIL_TABLO.get(k, k)
            st.session_state["latin_text"] = sonuc
            st.rerun()
    with b2:
        if st.button("Temizle"):
            st.session_state["kiril_text"] = ""
            st.session_state["latin_text"] = ""
            st.session_state["audio_data"] = None
            st.rerun()
    with b3:
        if st.button("Sesle Oku"):
            if st.session_state["kiril_text"].strip():
                try:
                    tts = gTTS(text=st.session_state["kiril_text"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["audio_data"] = fp.getvalue()
                except:
                    st.error("Ses yüklenemedi.")
                st.rerun()
                
    st.write("Latin Alfabesi Sonucu:")
    st.text_area("", value=st.session_state["latin_text"], height=150, disabled=True, key="sonuc_alanı", label_visibility="collapsed")
    
    if st.session_state["audio_data"] and st.session_state["kiril_text"].strip():
        st.audio(st.session_state["audio_data"], format='audio/mp3')

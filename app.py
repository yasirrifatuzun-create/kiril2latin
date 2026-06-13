import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="KIRIL2LATIN", layout="wide")

# CSS: Sola yaslı, düzenli ve iç içe geçmeyen buton yapısı
st.markdown("""
<style>
/* Butonları sola yasla ve düzenli bir grid oluştur */
.keyboard-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 5px;
}
div.stButton > button {
    width: 35px !important;
    height: 35px !important;
    padding: 0 !important;
    font-size: 14px !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# Harf Tablosu
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

def transliterasyon_yap(metin):
    return "".join([RUSCA_KIRIL_TABLO.get(k, k) for k in metin])

if "girdi" not in st.session_state: st.session_state["girdi"] = ""
if "sonuc" not in st.session_state: st.session_state["sonuc"] = ""

st.title("KIRIL2LATIN")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Sanal Klavye")
    # Butonları kapsayıcı içine alıp sola yaslıyoruz
    st.markdown('<div class="keyboard-container">', unsafe_allow_html=True)
    harfler = ["А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д", "Е", "е", "Ё", "ё",
               "Ж", "ж", "З", "з", "И", "и", "Й", "й", "К", "к", "Л", "л", "М", "м",
               "Н", "н", "О", "о", "П", "п", "Р", "р", "С", "с", "Т", "т", "У", "у",
               "Ф", "ф", "Х", "х", "Ц", "ц", "Ч", "ч", "Ш", "ш", "Щ", "щ", "Ъ", "ъ",
               "Ы", "ы", "Ь", "ь", "Э", "э", "Ю", "ю", "Я", "я"]
    
    for h in harfler:
        if st.button(h, key=f"btn_{h}"):
            st.session_state["girdi"] += h
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.session_state["girdi"] = st.text_area("Kiril Metin:", value=st.session_state["girdi"], height=100)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Dönüştür"):
        st.session_state["sonuc"] = transliterasyon_yap(st.session_state["girdi"])
        st.rerun()
    if c2.button("Temizle"):
        st.session_state["girdi"] = ""
        st.session_state["sonuc"] = ""
        st.rerun()
    if c3.button("Sesle Oku"):
        if st.session_state["girdi"]:
            tts = gTTS(text=st.session_state["girdi"], lang='ru')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp.getvalue(), format='audio/mp3')

    st.text_area("Latin Sonucu:", value=st.session_state["sonuc"], height=100)

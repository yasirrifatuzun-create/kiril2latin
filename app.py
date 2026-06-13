import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="KIRIL2LATIN", layout="wide")

# CSS: Butonları minik, bağımsız ve ızgaraya sığacak şekilde sabitledik
st.markdown("""
<style>
div.stButton > button {
    width: 28px !important;
    height: 28px !important;
    padding: 0 !important;
    margin: 1px !important;
    font-size: 10px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    border-radius: 3px !important;
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

# Session state yönetimi
if "girdi" not in st.session_state: st.session_state["girdi"] = ""
if "sonuc" not in st.session_state: st.session_state["sonuc"] = ""

st.title("KIRIL2LATIN")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("Sanal Klavye")
    harfler = [("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
               ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
               ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
               ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
               ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")]
    
    # Her harf çiftini ayrı sütunlarda, ızgara düzeninde çiz
    for i in range(0, len(harfler), 7):
        cols = st.columns(14)
        for j, (b, k) in enumerate(harfler[i:i+7]):
            if cols[j*2].button(b, key=f"b_{i}_{j}"):
                st.session_state["girdi"] += b
                st.rerun()
            if cols[j*2+1].button(k, key=f"k_{i}_{j}"):
                st.session_state["girdi"] += k
                st.rerun()

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

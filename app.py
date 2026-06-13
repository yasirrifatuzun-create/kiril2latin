import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN", layout="wide")

# CSS: En sola yaslı (girintisiz) şekilde sabitlenmiş tasarım
st.markdown("""
<style>
/* Buton boyutlarını sabitliyoruz (kare yapı) */
div[data-testid="stColumn"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important;
    padding: 0 !important;
    margin: 2px !important;
}
/* Harfleri kutunun tam merkezine kilitliyoruz */
div[data-testid="stColumn"] button p {
    margin: 0 !important;
    font-weight: bold !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
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

# Session State
if "girdi_metni" not in st.session_state: st.session_state["girdi_metni"] = ""
if "sonuc_metni" not in st.session_state: st.session_state["sonuc_metni"] = ""

st.title("KIRIL2LATIN - Transliterasyon")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.write("Sanal Klavye")
    harfler = [("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
               ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
               ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
               ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
               ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")]
    
    for i in range(0, len(harfler), 7):
        row = st.columns(14)
        for j, (b, k) in enumerate(harfler[i:i+7]):
            if row[j*2].button(b, key=f"btn_b_{i}_{j}"):
                st.session_state["girdi_metni"] += b
                st.rerun()
            if row[j*2+1].button(k, key=f"btn_k_{i}_{j}"):
                st.session_state["girdi_metni"] += k
                st.rerun()

with col2:
    yeni_girdi = st.text_area("Kiril Metin:", value=st.session_state["girdi_metni"], height=150)
    if yeni_girdi != st.session_state["girdi_metni"]:
        st.session_state["girdi_metni"] = yeni_girdi
        st.rerun()

    b1, b2, b3 = st.columns(3)
    if b1.button("Dönüştür"):
        st.session_state["sonuc_metni"] = transliterasyon_yap(st.session_state["girdi_metni"])
        st.rerun()
    if b2.button("Temizle"):
        st.session_state["girdi_metni"] = ""
        st.session_state["sonuc_metni"] = ""
        st.rerun()
    if b3.button("Sesle Oku"):
        if st.session_state["girdi_metni"]:
            tts = gTTS(text=st.session_state["girdi_metni"], lang='ru')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp.getvalue(), format='audio/mp3')

    st.text_area("Latin Sonucu:", value=st.session_state["sonuc_metni"], height=150)

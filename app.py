import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")
st.markdown("""
    <style>
    /* Sonuç kutusunun sadece seçilebilir olmasını sağlar */
    textarea[disabled] {
        cursor: text !important;
        background-color: #f0f2f6 !important;
    }
    </style>
""", unsafe_allow_html=True)
# Harfleri buton kutusunun tam ortasına oturtan CSS
st.markdown("""
    <style>
    div[data-testid="stColumn"] button p {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# DÜZELTİLMİŞ Harf Tablosu (Küçük 'т' artık 't' olacak)
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
    'Ъ': "‘", 'ъ': "‘", 'Ы': 'I', 'ы': 'ı', 'Ь': "’", 'ь': "’",
    'Э': 'E', 'э': 'e', 'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya', 'я': 'ya'
}

def transliterasyon_yap(metin):
    sonuc = ""
    for karakter in metin:
        sonuc += RUSCA_KIRIL_TABLO.get(karakter, karakter)
    return sonuc

# --- SESSION STATE INITIALIZATION ---
if "girdi_metni" not in st.session_state:
    st.session_state["girdi_metni"] = ""
if "sonuc_metni" not in st.session_state:
    st.session_state["sonuc_metni"] = ""

# --- ARAYÜZ ---
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")

sol_sutun, sag_sutun = st.columns([1, 1.1])

with sol_sutun:
    st.write("Kiril Alfabe - Sanal Klavye")
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # Klavye Izgarası
    for i in range(0, len(kiril_harfleri), 7):
        cols = st.columns(14)
        for j, (buyuk, kucuk) in enumerate(kiril_harfleri[i:i+7]):
            if cols[j*2].button(buyuk):
                st.session_state["girdi_metni"] += buyuk
                st.rerun()
            if cols[j*2+1].button(kucuk):
                st.session_state["girdi_metni"] += kucuk
                st.rerun()

with sag_sutun:
    # Metin Giriş Alanı
    yeni_girdi = st.text_area("Kiril Metin Girişi:", value=st.session_state["girdi_metni"], height=150)
    st.session_state["girdi_metni"] = yeni_girdi

    # Butonlar
    c1, c2, c3 = st.columns(3)
    
    if c1.button("Dönüştür", type="primary"):
        st.session_state["sonuc_metni"] = transliterasyon_yap(st.session_state["girdi_metni"])
        st.rerun()
        
    if c2.button("Temizle"):
        st.session_state["girdi_metni"] = ""
        st.session_state["sonuc_metni"] = ""
        st.rerun()
            
    if c3.button("Sesle Oku (Kiril)"):
        if st.session_state["girdi_metni"].strip():
            tts = gTTS(text=st.session_state["girdi_metni"], lang='ru')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp.getvalue(), format='audio/mp3')
# Sadece disabled=True'yu kaldırıyoruz, artık kopyalanabilir olacak
    st.text_area(
        label="Latin Alfabesi Sonucu:",
        value=st.session_state["sonuc_metni"],
        height=150,
        key="latin_sonuc_kutusu",
        label_visibility="collapsed"
    )

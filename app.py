import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

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

# Orijinal Transliterasyon Harf Tablosu
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
    sonuc = ""
    for karakter in metin:
        sonuc += RUSCA_KIRIL_TABLO.get(karakter, karakter)
    return sonuc

# --- STREAMLIT MERKEZİ BELLEK AYARLARI ---
if "kiril_metin_alani" not in st.session_state:
    st.session_state["kiril_metin_alani"] = ""
if "latin_metin" not in st.session_state:
    st.session_state["latin_metin"] = ""
if "ses_dosyasi" not in st.session_state:
    st.session_state["ses_dosyasi"] = None

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# İki Sütunlu Ana Düzen
sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "l"), ("М", "m"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "t"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    satir_genisligi = 7
    for i in range(0, len(kiril_harfleri), satir_genisligi):
        grup = kiril_harfleri[i:i+satir_genisligi]
        klavye_cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with klavye_cols[idx * 2]:
                if st.button(buyuk, key=f"k_b_{buyuk}_{i}_{idx}"):
                    st.session_state["kiril_metin_alani"] += buyuk
                    st.rerun()
            with klavye_cols[(idx * 2) + 1]:
                if st.button(kucuk, key=f"k_k_{kucuk}_{i}_{idx}"):
                    st.session_state["kiril_metin_alani"] += kucuk
                    st.rerun()

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Giriş Alanı
    giris_alani = st.text_area(
        label="Kiril Metin Girişi",
        value=st.session_state["kiril_metin_alani"],
        height=180,
        key="kiril_girdisi",
        label_visibility="collapsed"
    )
    st.session_state["kiril_metin_alani"] = giris_alani

    # İşlem Butonları
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_metin"] = transliterasyon_yap(st.session_state["kiril_metin_alani"])
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_metin_alani"] = ""
            st.session_state["latin_metin"] = ""
            st.session_state["ses_dosyasi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["kiril_metin_alani"].strip():
                try:
                    tts_ru = gTTS(text=st.session_state["kiril_metin_alani"], lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_dosyasi"] = fp_ru.getvalue()
                except:
                    st.error("Ses dosyası üretilemedi.")
                st.rerun()

    # Sonuç Alanı
    st.write("Latin alfabesi sonucu:")
    st.text_area(
        label="Sonuç Alanı",
        value=st.session_state["latin_metin"],
        height=180,
        disabled=True,
        key="latin_sonuc_kutusu",
        label_visibility="collapsed"
    )

    # Ses Oynatıcı
    if st.session_state["ses_dosyasi"] is not None and st.session_state["kiril_metin_alani"].strip():
        st.audio(st.session_state["ses_dosyasi"], format='audio/mp3')

st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesine karşılıklarının yazdırılmasıdır.")

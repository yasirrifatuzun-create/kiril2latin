import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# Orijinal Türkçe harf tablonuz
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
if "kiril_yazi_kutusu" not in st.session_state:
    st.session_state["kiril_yazi_kutusu"] = ""
if "latin_metin" not in st.session_state:
    st.session_state["latin_metin"] = ""
if "ses_dosyasi" not in st.session_state:
    st.session_state["ses_dosyasi"] = None

# HTML Klavyeden gelen tıklamaları yakalayan mekanizma
query_params = st.query_params
if "ekle_harf" in query_params:
    st.session_state["kiril_yazi_kutusu"] += query_params["ekle_harf"]
    st.query_params.clear()
    st.rerun()

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: KUSURSUZ KARE SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    # Harf listesi
    kiril_harfleri = [
        "А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д", "Е", "е", "Ё", "ё",
        "Ж", "ж", "З", "з", "И", "и", "Й", "й", "К", "к", "Л", "л", "М", "м",
        "Н", "н", "О", "о", "П", "п", "Р", "р", "С", "с", "Т", "т", "У", "у",
        "Ф", "ф", "Х", "х", "Ц", "ц", "Ч", "ç", "Ш", "ş", "Щ", "щ", "Ъ", "ъ",
        "Ы", "ы", "Ь", "ь", "Э", "э", "Ю", "ю", "Я", "я"
    ]
    
    # Butonları milimetrik kare yapan, harfleri tam ortalayan HTML Grid Yapısı
    klavye_html = """
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(14, 1fr);
        gap: 6px;
        background-color: transparent;
        padding: 5px 0px;
    }
    .grid-item {
        background-color: #262730;
        color: #ffffff;
        border: 1px solid #464855;
        border-radius: 4px;
        aspect-ratio: 1 / 1; /* Kesin kare olmasını zorunlu kılar */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 500;
        text-decoration: none;
        transition: background-color 0.1s, border-color 0.1s;
    }
    .grid-item:hover {
        background-color: #31333F;
        border-color: #ff4b4b;
    }
    .grid-item:active {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    <div class="grid-container">
    """
    
    for harf in kiril_harfleri:
        klavye_html += f'<a href="?ekle_harf={harf}" target="_self" class="grid-item">{harf}</a>'
    
    klavye_html += "</div>"
    st.components.v1.html(klavye_html, height=280, scrolling=False)

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Giriş Alanı: Doğrudan hafıza hücresine bağlıdır, asla sıfırlanmaz veya takılmaz
    giris_alani = st.text_area(
        "",
        value=st.session_state["kiril_yazi_kutusu"],
        height=180,
        key="kiril_yazi_kutusu_ana",
        label_visibility="collapsed"
    )

    # 3'lü İşlem Butonları
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["kiril_yazi_kutusu"] = giris_alani
            st.session_state["latin_metin"] = transliterasyon_yap(giris_alani)
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_yazi_kutusu"] = ""
            st.session_state["latin_metin"] = ""
            st.session_state["ses_dosyasi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            st.session_state["kiril_yazi_kutusu"] = giris_alani
            if giris_alani.strip():
                try:
                    tts_ru = gTTS(text=giris_alani, lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_dosyasi"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses dosyası üretilemedi.")
                st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Çıktı Kutusu
    st.text_area(
        "",
        value=st.session_state["latin_metin"],
        height=180,
        disabled=True,
        key="latin_sonuc_kutusu",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_dosyasi"] is not None and st.session_state["kiril_yazi_kutusu"].strip():
        st.audio(st.session_state["ses_dosyasi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

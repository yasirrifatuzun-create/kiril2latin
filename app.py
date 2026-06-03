import streamlit as st
from gtts import gTTS
import io
import re

# Sayfa Ayarları (Tarayıcı sekmesinde görünecek kısım)
st.set_page_config(page_title="KİRİL2LATİN - Transliterasyon", page_icon="🔤", layout="centered")

RUSCA_KIRIL_TABLO = {
    'A': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
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

def contains_cyrillic(text):
    return any("\u0400" <= ch <= "\u04FF" for ch in text)

# --- WEB ARAYÜZÜ ---
st.title("🔤 KİRİL2LATİN")
st.subheader("Transliterasyon Uygulaması")
st.write("Kiril harfli metni aşağıya yapıştırın veya sanal klavyeyi kullanın.")

# Sanal Klavye Bölümü
st.write("**Sanal Kiril Klavyesi** (Tıklayarak metin alanına ekleyebilirsiniz)")
kiril_harfleri = [
    "А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д", "Е", "е", "Ё", "ё", "Ж", "ж",
    "З", "з", "И", "и", "Й", "y", "К", "к", "Л", "л", "М", "м", "Н", "н", "О", "о",
    "П", "п", "Р", "р", "С", "с", "Т", "t", "У", "у", "Ф", "ф", "Х", "х", "Ц", "ц",
    "Ч", "ç", "Ш", "ш", "Щ", "щ", "Ъ", "ъ", "Ы", "ы", "Ь", "ь", "Э", "э", "Ю", "ю", "Я", "я"
]

# Session state ile klavyeden basılan harfleri tutuyoruz
if "metin_kutusu" not in st.session_state:
    st.session_state["metin_kutusu"] = ""

# Harf butonlarını yan yana dizmek için grid yapısı
cols = st.columns(12)
for i, harf in enumerate(kiril_harfleri):
    with cols[i % 12]:
        if st.button(harf, key=f"btn_{harf}"):
            st.session_state["metin_kutusu"] += harf

# Giriş Alanı
giris_metni = st.text_area("Kiril Metin:", value=st.session_state["metin_kutusu"], height=150, key="ana_giris")

# Temizleme Butonu
if st.button("Metni Temizle"):
    st.session_state["metin_kutusu"] = ""
    st.rerun()

# Dönüştürme Mantığı
if giris_metni:
    latin_sonuc = transliterasyon_yap(giris_metni)
    
    st.markdown("### 📝 Latin Alfabesi Sonucu:")
    st.info(latin_sonuc)
    
    # Seslendirme Bölümü (Web uyumlu gTTS)
    st.markdown("### 🔊 Sesli Okuma")
    col1, col2 = st.columns(2)
    
    with col1:
        if contains_cyrillic(giris_metni):
            st.write("Kiril (Rusça Okunuş):")
            try:
                tts_ru = gTTS(text=giris_metni, lang='ru', slow=False)
                fp_ru = io.BytesIO()
                tts_ru.write_to_fp(fp_ru)
                st.audio(fp_ru, format='audio/mp3')
            except Exception as e:
                st.error("Ses yüklenemedi.")
                
    with col2:
        st.write("Latin (Türkçe Okunuş simülasyonu):")
        try:
            # Türkçe ses motoruyla Latin çıktıyı okutuyoruz
            tts_tr = gTTS(text=latin_sonuc, lang='tr', slow=False)
            fp_tr = io.BytesIO()
            tts_tr.write_to_fp(fp_tr)
            st.audio(fp_tr, format='audio/mp3')
        except Exception as e:
            st.error("Ses yüklenemedi.")

st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesine karşılıklarının yazdırılmasıdır.")

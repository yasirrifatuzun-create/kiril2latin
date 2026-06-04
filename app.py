import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KİRİL2LATİN - Transliterasyon", page_icon="🔤", layout="centered")

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

# --- STREAMLIT MEMORY (SESSION STATE) AYARLARI ---
# Web sayfasında yazılan metnin kaybolmaması için hafıza alanı oluşturuyoruz
if "metin_hafizasi" not in st.session_state:
    st.session_state["metin_hafizasi"] = ""

# --- WEB ARAYÜZÜ ---
st.title("🔤 KİRİL2LATİN")
st.subheader("Transliterasyon Uygulaması")
st.write("Kiril harfli metni aşağıya yapıştırın veya sanal klavyeyi kullanın.")

# Sanal Klavye Bölümü
st.write("**Sanal Kiril Klavyesi** (Harflere basarak metin oluşturabilirsiniz):")
kiril_harfleri = [
    ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"),
    ("Д", "д"), ("Е", "е"), ("Ё", "ё"), ("Ж", "ж"),
    ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"),
    ("Л", "л"), ("М", "м"), ("Н", "н"), ("О", "о"),
    ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"),
    ("У", "у"), ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"),
    ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
    ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"),
    ("Я", "я")
]

# Klavye harflerini düzgün butonlar halinde dizmek için grid (8 sütunlu)
cols = st.columns(8)
for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
    col_idx = index % 4  # 4 çifti yan yana koyacağız (büyük-küçük yan yana dursun diye)
    
    with cols[col_idx * 2]:
        if st.button(buyuk, key=f"btn_b_{buyuk}", use_container_width=True):
            st.session_state["metin_hafizasi"] += buyuk
            st.rerun() # Sayfayı güncelleyip harfi kutuya yansıtıyoruz
            
    with cols[(col_idx * 2) + 1]:
        if st.button(kucuk, key=f"btn_k_{kucuk}", use_container_width=True):
            st.session_state["metin_hafizasi"] += kucuk
            st.rerun()

st.write("---")

# Giriş Alanı (Hafızadaki metne bağlanmıştır)
giris_metni = st.text_area(
    "Kiril Metin Girişi:", 
    value=st.session_state["metin_hafizasi"], 
    height=120,
    help="Klavyeden bastığınız harfler buraya eklenir. İsterseniz kendiniz de yazabilirsiniz."
)

# Değişiklikleri el yazısıyla yapıldıysa hafızaya geri alalım
st.session_state["metin_hafizasi"] = giris_metni

# Temizleme Butonu
if st.button("🗑️ Metni Temizle", type="secondary"):
    st.session_state["metin_hafizasi"] = ""
    st.rerun()

# --- DÖNÜŞTÜRME VE SESLENDİRME MANTIĞI ---
if giris_metni.strip():
    latin_sonuc = transliterasyon_yap(giris_metni)
    
    st.markdown("### 📝 Latin Alfabesi Sonucu (Türkçe Okunuşu):")
    st.success(latin_sonuc)
    
    st.markdown("### 🔊 Sesli Okuma Paneli")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Rusça Seslendirme (Kiril):**")
        try:
            # Orijinal Kiril metni doğrudan Rusça dil koduyla ('ru') Google'a okutuyoruz
            tts_ru = gTTS(text=giris_metni, lang='ru', slow=False)
            fp_ru = io.BytesIO()
            tts_ru.write_to_fp(fp_ru)
            st.audio(fp_ru, format='audio/mp3')
        except Exception as e:
            st.error("Rusça ses oluşturulamadı.")
            
    with col2:
        st.write("**Türkçe Yaklaşık Okunuş (Latin):**")
        try:
            # Çıkan Latin harfli sonucu Türkçe dil koduyla ('tr') okutuyoruz
            tts_tr = gTTS(text=latin_sonuc, lang='tr', slow=False)
            fp_tr = io.BytesIO()
            tts_tr.write_to_fp(fp_tr)
            st.audio(fp_tr, format='audio/mp3')
        except Exception as e:
            st.error("Türkçe ses oluşturulamadı.")

st.caption("Not: Bu bir çeviri değil, Kiril harflerin Türkçe Latin alfabesine göre okunuş simülasyonudur.")

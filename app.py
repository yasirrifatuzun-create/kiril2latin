import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları - Tarayıcı ikonu tamamen kaldırıldı
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="centered")

# Orijinal Türkçe harf tablonuz aynen korunuyor
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

# --- STREAMLIT HAFIZA AYARLARI ---
if "metin_hafizasi" not in st.session_state:
    st.session_state["metin_hafizasi"] = ""

# --- ARAYÜZ BAŞLIĞI ---
st.title("KIRIL2LATIN")
st.subheader("Transliterasyon Uygulaması")

# --- 1. GİRİŞ ALANI VE SONUÇLAR (GÖZ ÖNÜNDE OLMASI İÇİN EN ÜSTTE) ---
giris_metni = st.text_input(
    "Kiril Metin Girişi:", 
    value=st.session_state["metin_hafizasi"],
    placeholder="Sanal klavyeyi kullanabilir veya buraya doğrudan yazabilirsiniz..."
)
st.session_state["metin_hafizasi"] = giris_metni

# Dönüştürme Çıktısı ve Ses Oynatıcı
if giris_metni.strip():
    latin_sonuc = transliterasyon_yap(giris_metni)
    
    st.markdown("### Latin Alfabesi Sonucu:")
    st.success(latin_sonuc)
    
    st.markdown("### Sesli Okuma (Rusça Orijinal)")
    try:
        tts_ru = gTTS(text=giris_metni, lang='ru', slow=False)
        fp_ru = io.BytesIO()
        tts_ru.write_to_fp(fp_ru)
        st.audio(fp_ru, format='audio/mp3')
    except Exception as e:
        st.error("Rusça ses oluşturulamadı.")

st.write("---")

# --- 2. KONTROL TUŞLARI (EMOJİSİZ VE ENTEGRE) ---
kontrol_col1, kontrol_col2, kontrol_col3 = st.columns([2, 2, 3])

with kontrol_col1:
    if st.button("Space (Boşluk)", use_container_width=True):
        st.session_state["metin_hafizasi"] += " "
        st.rerun()

with kontrol_col2:
    if st.button("Sil (Backspace)", use_container_width=True):
        if len(st.session_state["metin_hafizasi"]) > 0:
            st.session_state["metin_hafizasi"] = st.session_state["metin_hafizasi"][:-1]
        st.rerun()

with kontrol_col3:
    if st.button("Tüm Metni Temizle", type="secondary", use_container_width=True):
        st.session_state["metin_hafizasi"] = ""
        st.rerun()

st.write("")

# --- 3. SANAL KLAVYE ALANI ---
st.write("**Sanal Kiril Klavyesi**")

kiril_harfleri = [
    ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
    ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"), 
    ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"), 
    ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
    ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
]

# Yan yana bağımsız büyük ve küçük harf butonları (14 Sütunlu Düzen)
cols = st.columns(14)
for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
    col_idx = index % 7
    
    # Büyük Harf Düğmesi
    with cols[col_idx * 2]:
        if st.button(buyuk, key=f"btn_b_{buyuk}_{index}", use_container_width=True):
            st.session_state["metin_hafizasi"] += buyuk
            st.rerun()
            
    # Küçük Harf Düğmesi
    with cols[(col_idx * 2) + 1]:
        if st.button(kucuk, key=f"btn_k_{kucuk}_{index}", use_container_width=True):
            st.session_state["metin_hafizasi"] += kucuk
            st.rerun()

st.write("")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesine karşılıklarının yazdırılmasıdır.")

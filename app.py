import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

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
if "ses_tetikleyici" not in st.session_state:
    st.session_state["ses_tetikleyici"] = False

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni aşağıya yapıştırın veya aşağıdaki alfabe sırasına göre kullanılan klavyeyi seçin.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"), 
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14)
            
        col_idx = index % 7
        
        with klavye_cols[col_idx * 2]:
            if st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True):
                st.session_state["metin_hafizasi"] += buyuk
                st.rerun()
                
        with klavye_cols[(col_idx * 2) + 1]:
            if st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True):
                st.session_state["metin_hafizasi"] += kucuk
                st.rerun()

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    # Kiril Giriş Alanı
    giris_metni = st.text_area(
        "", 
        value=st.session_state["metin_hafizasi"], 
        height=180,
        label_visibility="collapsed"
    )
    st.session_state["metin_hafizasi"] = giris_metni

    # 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    donustur_basildi = False
    with btn_col1:
        # Dönüştür butonuna basıldığında tetiklenecek mekanizma eklendi
        if st.button("Dönüştür", type="primary", use_container_width=True):
            donustur_basildi = True
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["metin_hafizasi"] = ""
            st.session_state["ses_tetikleyici"] = False
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            st.session_state["ses_tetikleyici"] = True

    # Yavaş Okuma Seçeneği (İsteğe bağlı hız ayarı)
    yavas_oku = st.checkbox("Yavaş Okuma (Tane tane telaffuz et)")

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Giriş yapılmışsa veya Dönüştür butonuna basılmışsa sonucu göster
    latin_sonuc = transliterasyon_yap(giris_metni) if giris_metni else ""
    
    st.markdown(
        f"""
        <textarea 
            readonly 
            style="
                width: 100%; 
                height: 180px; 
                font-size: 18px; 
                font-family: inherit;
                padding: 12px; 
                border-radius: 8px; 
                border: 1px solid #ccc; 
                background-color: #f8f9fa; 
                color: #212529;
                resize: none;
                outline: none;
            "
        >{latin_sonuc}</textarea>
        """, 
        unsafe_allow_html=True
    )

    # Ses oynatıcı paneli (Yavaş okuma parametresi entegre edildi)
    if st.session_state["ses_tetikleyici"] and giris_metni.strip():
        try:
            # slow=yavas_oku parametresi ile kullanıcının seçimi gTTS motoruna aktarılır
            tts_ru = gTTS(text=giris_metni, lang='ru', slow=yavas_oku)
            fp_ru = io.BytesIO()
            tts_ru.write_to_fp(fp_ru)
            st.audio(fp_ru, format='audio/mp3')
        except Exception as e:
            st.error("Ses oluşturulamadı.")
        st.session_state["ses_tetikleyici"] = False

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

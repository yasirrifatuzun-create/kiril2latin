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

# --- STREAMLIT KALICI HAFIZA (SESSION STATE) İLKLENDİRME ---
if "kiril_yazi_alani" not in st.session_state:
    st.session_state["kiril_yazi_alani"] = ""
if "ses_verisi" not in st.session_state:
    st.session_state["ses_verisi"] = None

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
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "m"), 
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
                st.session_state["kiril_yazi_alani"] += buyuk
                st.session_state["ses_verisi"] = None  # Metin değişince eski sesi temizle
                st.rerun()
                
        with klavye_cols[(col_idx * 2) + 1]:
            if st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True):
                st.session_state["kiril_yazi_alani"] += kucuk
                st.session_state["ses_verisi"] = None  # Metin değişince eski sesi temizle
                st.rerun()

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    # Kiril Giriş Alanı
    giris_metni = st.text_area(
        "", 
        height=180,
        key="kiril_yazi_alani",
        label_visibility="collapsed"
    )

    # CRITICAL DEBUG: Yavaş okuma seçimini butonlardan ÖNCEYE aldık. 
    # Böylece kod yukarıdan aşağıya çalışırken buton hız değerini görebiliyor.
    yavas_mi = st.checkbox("Yavaş Okuma (Tane tane telaffuz et)", key="yavas_oku_secimi")

    # 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_yazi_alani"] = ""
            st.session_state["ses_verisi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["kiril_yazi_alani"].strip():
                try:
                    # Yukarıda tanımlanan yavas_mi durumunu direkt ses motoruna veriyoruz
                    tts_ru = gTTS(text=st.session_state["kiril_yazi_alani"], lang='ru', slow=yavas_mi)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_verisi"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses oluşturulamadı.")

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Girişteki metne göre anlık canlı transliterasyon hesabı
    latin_sonuc = transliterasyon_yap(st.session_state["kiril_yazi_alani"]) if st.session_state["kiril_yazi_alani"] else ""
    
    # Giriş kutusuyla tarz, punto, yükseklik ve boşlukları birebir eşitlenmiş Streamlit Text Area bileşeni
    st.text_area(
        "",
        value=latin_sonuc,
        height=180,
        disabled=True,
        key="latin_sonuc_alani",
        label_visibility="collapsed"
    )

    # Eğer hafızada üretilmiş güncel ses verisi varsa ekranda sabit tut ve oynat
    if st.session_state["ses_verisi"] is not None and st.session_state["kiril_yazi_alani"].strip():
        st.audio(st.session_state["ses_verisi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

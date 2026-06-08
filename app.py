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

# --- SOL SÜTUN: SANAL KLAVYE (DEBUG EDİLDİ) ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"), 
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # Döngü içinde çökme yaşanmaması için satır satır (Grid) yapı kuruldu
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14) # Her 7 harfte bir yeni temiz satır açılır
            
        col_idx = index % 7
        
        # Büyük Harf Butonu
        with klavye_cols[col_idx * 2]:
            if st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True):
                st.session_state["metin_hafizasi"] += buyuk
                st.rerun()
                
        # Küçük Harf Butonu
        with klavye_cols[(col_idx * 2) + 1]:
            if st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True):
                st.session_state["metin_hafizasi"] += kucuk
                st.rerun()

# --- SAĞ SÜTUN: METİN GİRİŞİ, KALAN BUTONLAR VE BÜYÜTÜLMÜŞ ÇIKTI ---
with sag_sutun:
    # Kiril Giriş Alanı
    giris_metni = st.text_area(
        "", 
        value=st.session_state["metin_hafizasi"], 
        height=200,
        label_visibility="collapsed"
    )
    st.session_state["metin_hafizasi"] = giris_metni

    # İstediğin gibi sadece 3 buton bırakıldı (Diğer ikisi kaldırıldı)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        st.button("Dönüştür", type="primary", use_container_width=True)
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["metin_hafizasi"] = ""
            st.session_state["ses_tetikleyici"] = False
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            st.session_state["ses_tetikleyici"] = True

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Küçük görünme sorunu için CSS ile yazı boyutu 24px yapıldı ve kalınlaştırıldı
    if giris_metni:
        latin_sonuc = transliterasyon_yap(giris_metni)
        st.markdown(
            f"""
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; border-left: 6px solid #2e7d32;">
                <span style="color: #1b5e20; font-size: 24px; font-weight: bold; font-family: sans-serif;">
                    {latin_sonuc}
                </span>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; border-left: 6px solid #9e9e9e; height: 70px;">
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Ses oynatıcı paneli
    if st.session_state["ses_tetikleyici"] and giris_metni.strip():
        try:
            tts_ru = gTTS(text=giris_metni, lang='ru', slow=False)
            fp_ru = io.BytesIO()
            tts_ru.write_to_fp(fp_ru)
            st.audio(fp_ru, format='audio/mp3')
        except Exception as e:
            st.error("Ses oluşturulamadı.")
        st.session_state["ses_tetikleyici"] = False

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

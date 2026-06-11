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

# --- STREAMLIT MERKEZİ HAFIZA (SESSION STATE) ---
if "kiril_input" not in st.session_state:
    st.session_state["kiril_input"] = ""
if "latin_output" not in st.session_state:
    st.session_state["latin_output"] = ""
if "ses_verisi" not in st.session_state:
    st.session_state["ses_verisi"] = None

# KRİTİK DEBUG: Kutuda el yazısı değiştikçe tetiklenen ve kilidi kıran fonksiyon
def kutu_guncellendi():
    st.session_state["latin_output"] = transliterasyon_yap(st.session_state["kiril_input"])

# KRİTİK DEBUG: Sanal klavyeye basıldığında tetiklenen fonksiyon
def harf_ekle(harf):
    st.session_state["kiril_input"] += harf
    st.session_state["latin_output"] = transliterasyon_yap(st.session_state["kiril_input"])
    st.session_state["ses_verisi"] = None

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "l"), ("М", "м"), 
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14)
            
        col_idx = index % 7
        
        with klavye_cols[col_idx * 2]:
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(kucuk,))

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Kiril Giriş Alanı - Hem el yazısını hem butonları çakıştırmayan on_change mimarisi
    st.text_area(
        "Kiril Metin Girişi:", 
        height=180,
        key="kiril_input",
        on_change=kutu_guncellendi,
        label_visibility="collapsed"
    )

    # 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTONU: Form kilitlerini kırarak anlık veriyi ekrana basmaya zorlar
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_output"] = transliterasyon_yap(st.session_state["kiril_input"])
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_input"] = ""
            st.session_state["latin_output"] = ""
            st.session_state["ses_verisi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["kiril_input"].strip():
                try:
                    tts_ru = gTTS(text=st.session_state["kiril_input"], lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_verisi"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses oluşturulamadı.")

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Tamamen bağımsız çalışan salt okunur sonuç kutusu
    st.text_area(
        "",
        value=st.session_state["latin_output"],
        height=180,
        disabled=True,
        key="latin_output_alani",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_verisi"] is not None and st.session_state["kiril_input"].strip():
        st.audio(st.session_state["ses_verisi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

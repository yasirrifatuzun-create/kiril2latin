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

# --- GÜVENLİ VE SABİT HAFIZA SİSTEMİ ---
if "form_girdisi" not in st.session_state:
    st.session_state["form_girdisi"] = ""
if "form_cikti" not in st.session_state:
    st.session_state["form_cikti"] = ""
if "form_ses" not in st.session_state:
    st.session_state["form_ses"] = None

# Sanal klavye buton aksiyonu
def harf_bas(harf):
    st.session_state["form_girdisi"] += harf

# Başlık Alanları
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ORİJİNAL GÖRSEL DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"), 
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "t"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14)
            
        col_idx = index % 7
        
        with klavye_cols[col_idx * 2]:
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_bas, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_bas, args=(kucuk,))

# --- SAĞ SÜTUN: ARTIK BOZULMAYAN ORİJİNAL TASARIM ---
with sag_sutun:
    
    # Kilitlenmeleri önleyen form yapısı
    with st.form("transliterasyon_formu", clear_on_submit=False):
        
        # Orijinal üst büyük metin alanı
        kiril_metin_alani = st.text_area(
            "", 
            value=st.session_state["form_girdisi"],
            height=180,
            key="kiril_form_kutusu",
            label_visibility="collapsed"
        )
        
        # 3'lü Buton Sırası
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            # DÖNÜŞTÜR: Sadece dönüştürme yapar, hafızayı senkronize eder
            if st.form_submit_button("Dönüştür", type="primary", use_container_width=True):
                st.session_state["form_girdisi"] = kiril_metin_alani
                st.session_state["form_cikti"] = transliterasyon_yap(kiril_metin_alani)
                st.rerun()
            
        with btn_col2:
            # TEMİZLE: Hatalı atamalardan arındırıldı, tüm hafızayı güvenle sıfırlar
            if st.form_submit_button("Temizle", use_container_width=True):
                st.session_state["form_girdisi"] = ""
                st.session_state["form_cikti"] = ""
                st.session_state["form_ses"] = None
                st.rerun()
                
        with btn_col3:
            # SESLE OKU: Kiril metni alır ve ses dosyasına dönüştürür
            if st.form_submit_button("Sesle Oku (Kiril)", use_container_width=True):
                st.session_state["form_girdisi"] = kiril_metin_alani
                if kiril_metin_alani.strip():
                    try:
                        tts = gTTS(text=kiril_metin_alani, lang='ru', slow=False)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        st.session_state["form_ses"] = fp.getvalue()
                    except Exception as e:
                        st.error("Ses sentezlenemedi.")
                st.rerun()

    # Orijinal alt büyük çıktı alanı
    st.write("Latin alfabesi sonucu:")
    st.text_area(
        "",
        value=st.session_state["form_cikti"],
        height=180,
        disabled=True,
        key="latin_form_cikti_kutusu",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["form_ses"] is not None and st.session_state["form_girdisi"].strip():
        st.audio(st.session_state["form_ses"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

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

# --- KİLİTLENMEYEN GÜVENLİ HAFIZA ALANI ---
if "kiril_girdi_alani" not in st.session_state:
    st.session_state["kiril_girdi_alani"] = ""
if "latin_sonuc_alani" not in st.session_state:
    st.session_state["latin_sonuc_alani"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Sanal klavye butonu basıldığında çalışan kilit kırıcı fonksiyon
def harf_butonu_tetiklendi(harf):
    # Kutuda o an el yazısıyla veya butonla ne varsa güvenle çek
    mevcut_metin = st.session_state.get("kiril_girdi_alani", "")
    # Harfi üzerine ekle ve doğrudan kutunun ana hafızasına yazdır
    st.session_state["kiril_girdi_alani"] = mevcut_metin + harf

# Üst Başlık ve Açıklamalar (Birebir Aynı Tasarım)
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU DÜZEN ---
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
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_butonu_tetiklendi, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_butonu_tetiklendi, args=(kucuk,))

# --- SAĞ SÜTUN: KİLİTLENMEYEN ORİJİNAL TASARIM ---
with sag_sutun:
    
    # Giriş Kutusu: 'value' parametresi kaldırıldı. Kilitlenme imkansız hale getirildi.
    # Tarayıcı çakışması yaşanmadan hem el yazısını hem butonları burası havada kapar.
    st.text_area(
        "", 
        height=180,
        key="kiril_girdi_alani",
        label_visibility="collapsed"
    )
    
    # Kutudaki en güncel metni güvenli değişkene aktarıyoruz
    guncel_kiril_metin = st.session_state.get("kiril_girdi_alani", "")

    # 3'lü Buton Sırası (Birebir Aynı Tasarım)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTONU: Hafızadaki metni anında işler ve alt kutuya basar
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_sonuc_alani"] = transliterasyon_yap(guncel_kiril_metin)
            st.rerun

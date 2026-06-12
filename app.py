import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# CSS: Sadece sol sütundaki klavye butonlarını kare yapar, sağdaki işlem butonlarına dokunmaz
st.markdown("""
    <style>
    /* Sol sütundaki (sanal klavye) kolon boşluklarını daraltır */
    [data-testid="stColumn"] [data-testid="stColumn"] {
        padding: 1px !important;
        margin: 0px !important;
    }
    
    /* YALNIZCA sanal klavye butonlarını tam birer kare yapar ve harfi ortalar */
    [data-testid="stColumn"] [data-testid="stColumn"] div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 15px !important;
    }
    
    /* Sağ sütundaki ana işlem butonlarının (Dönüştür vb.) dev kare olmasını engeller, normal hizalar */
    div.stButton > button[key^="main_"] {
        aspect-ratio: auto !important;
        height: 45px !important;
    }
    </style>
""", unsafe_allow_html=True)

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
if "kiril_metin_alani" not in st.session_state:
    st.session_state["kiril_metin_alani"] = ""
if "latin_metin" not in st.session_state:
    st.session_state["latin_metin"] = ""
if "ses_dosyasi" not in st.session_state:
    st.session_state["ses_dosyasi"] = None

# Sanal klavye buton tetikleyicisi
def harf_ekle(harf):
    st.session_state["kiril_metin_alani"] += harf

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE (TAM KARE) ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "m"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ç"), ("Ш", "ş"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    satir_genisligi = 7
    for i in range(0, len(kiril_harfleri), satir_genisligi):
        grup = kiril_harfleri[i:i+satir_genisligi]
        klavye_cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with klavye_cols[idx * 2]:
                st.button(buyuk, key=f"k_b_{buyuk}_{i}_{idx}", on_click=harf_ekle, args=(buyuk,))
            with klavye_cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"k_k_{kucuk}_{i}_{idx}", on_click=harf_ekle, args=(kucuk,))

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Giriş Alanı
    giris_alani = st.text_area(
        label="Giriş Alanı",
        value=st.session_state["kiril_metin_alani"],
        height=180,
        key="kiril_girdisi",
        label_visibility="collapsed"
    )
    
    # Hafızayı el ile yazılan metne göre güncel tutar
    st.session_state["kiril_metin_alani"] = giris_alani

    # 3'lü Buton Sırası (Buradaki butonların key'leri CSS tarafından hedef alınmıştır)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True, key="main_donustur"):
            st.session_state["latin_metin"] = transliterasyon_yap(giris_alani)
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True, key="main_temizle"):
            st.session_state["kiril_metin_alani"] = ""
            st.session_state["latin_metin"] = ""
            st.session_state["ses_dosyasi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True, key="main_sesle_oku"):
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
    
    # Çıktı Kutusu (Hediye harf sorunu tamamen temizlendi)
    st.text_area(
        label="Sonuç Alanı",
        value=st.session_state["latin_metin"],
        height=180,
        disabled=True,
        key="latin_sonuc_kutusu",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_dosyasi"] is not None and st.session_state["kiril_metin_alani"].strip():
        st.audio(st.session_state["ses_dosyasi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

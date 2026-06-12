import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# CSS: Butonları tam kare yapar, harfleri ortalar ve sola hizalı bir grid düzeni kurar
st.markdown("""
    <style>
    /* Streamlit'in varsayılan buton esnetmesini engeller, butonları sola yaslar */
    div.stButton {
        text-align: left !important;
    }
    
    /* Sanal klavyedeki tüm butonları milimetrik kare yapar */
    div.stButton > button {
        width: 45px !important;
        height: 45px !important;
        padding: 0px !important;
        margin: 0px !important;
        aspect-ratio: 1 / 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
    }
    
    /* Sağ taraftaki işlem butonlarının (Dönüştür vb.) normal dikdörtgen kalmasını sağlar */
    div[data-testid="stColumn"]:nth-child(2) div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        aspect-ratio: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# Orijinal Transliterasyon Tablosu (Tüm harfler eksiksiz ve doğrudur)
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

# --- STREAMLIT BELLEK YÖNETİMİ ---
if "metin_kutusu" not in st.session_state:
    st.session_state["metin_kutusu"] = ""
if "latin_cikti" not in st.session_state:
    st.session_state["latin_cikti"] = ""
if "ses_verisi" not in st.session_state:
    st.session_state["ses_verisi"] = None

# Butona basıldığında doğrudan text_area'yı tetikleyen temiz fonksiyon
def harf_basildi(harf):
    st.session_state["metin_kutusu"] += harf

st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın veya soldaki sanal klavyeyi kullanın.")

# İki Sütunlu Düzen
sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Sanal Klavye")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "l"), ("М", "м"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # Her satırda tam 14 buton olacak şekilde kusursuz yerleşim
    for i in range(0, len(kiril_harfleri), 7):
        grup = kiril_harfleri[i:i+7]
        cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with cols[idx * 2]:
                st.button(buyuk, key=f"b_{buyuk}_{i}", on_click=harf_basildi, args=(buyuk,))
            with cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"k_{kucuk}_{i}", on_click=harf_basildi, args=(kucuk,))

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Giriş alanı anlık olarak klavyeden beslenir
    girdi = st.text_area(
        "Kiril Metin Girişi:",
        value=st.session_state["metin_kutusu"],
        height=150,
        key="kiril_girdi_alani"
    )
    st.session_state["metin_kutusu"] = girdi
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary"):
            st.session_state["latin_cikti"] = transliterasyon_yap(st.session_state["metin_kutusu"])
            st.rerun()
            
    with btn_col2:
        if st.button("Temizle"):
            st.session_state["metin_kutusu"] = ""
            st.session_state["latin_cikti"] = ""
            st.session_state["ses_verisi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)"):
            if st.session_state["metin_kutusu"].strip():
                try:
                    tts = gTTS(text=st.session_state["metin_kutusu"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_verisi"] = fp.getvalue()
                except:
                    st.error("Ses dosyası oluşturulamadı.")
                st.rerun()
                
    st.write("Latin Alfabesi Sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_cikti"],
        height=150,
        disabled=True,
        key="latin_sonuc_pencerem",
        label_visibility="collapsed"
    )
    
    if st.session_state["ses_verisi"] and st.session_state["metin_kutusu"].strip():
        st.audio(st.session_state["ses_verisi"], format='audio/mp3')

st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesindeki ses karşılıklarına dönüştürülmesidir.")

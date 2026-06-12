import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# CSS: Klavye butonlarını tam sola yaslar, milimetrik kare yapar ve sağdaki işlem butonlarını korur
st.markdown("""
    <style>
    /* Sanal klavye butonlarının geniş ekranlarda sağa doğru açılmasını engeller, sola sabitler */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] {
        justify-content: flex-start !important;
    }
    
    /* Klavye sütunlarındaki gereksiz boşlukları temizler */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] {
        padding: 1px !important;
        margin: 0px !important;
        max-width: 45px !important; /* Butonların büyümesini engeller */
    }
    
    /* Sadece sanal klavye butonlarını hedefler ve tam kare yapar */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] button {
        width: 42px !important;
        height: 42px !important;
        padding: 0px !important;
        margin: 0px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
    }
    
    /* Sağ taraftaki ana işlem butonlarının kare olmasını engeller, standart formda bırakır */
    div[data-testid="stColumn"]:nth-child(2) button {
        width: 100% !important;
        height: 45px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Doğrulanan Transliterasyon Harf Tablosu
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

# --- STREAMLIT SESSION STATE BELLEK KONTROLLERİ ---
if "kiril_metin" not in st.session_state:
    st.session_state["kiril_metin"] = ""
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_dosyasi" not in st.session_state:
    st.session_state["ses_dosyasi"] = None

# Butonların anlık ve kararlı tetiklenmesini sağlayan callback fonksiyonu
def harf_ekle_callback(harf):
    st.session_state["kiril_metin"] += harf

st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın veya soldaki sanal klavyeyi kullanın.")

# İki ana sütun düzeni
sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Sanal Klavye")
    
    # Tüm harfler (ç ve m dahil) orijinal Kiril formuna getirildi
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # Her satırda 7 çift (14 buton) sola hizalı grid yerleşimi
    for i in range(0, len(kiril_harfleri), 7):
        grup = kiril_harfleri[i:i+7]
        cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with cols[idx * 2]:
                st.button(buyuk, key=f"b_{buyuk}_{i}_{idx}", on_click=harf_ekle_callback, args=(buyuk,))
            with cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"k_{kucuk}_{i}_{idx}", on_click=harf_ekle_callback, args=(kucuk,))

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    
    # Giriş kutusu anlık olarak state değerini okur ve yansıtır
    girdi = st.text_area(
        "Kiril Metin Girişi:",
        value=st.session_state["kiril_metin"],
        height=150,
        key="kiril_girdisi_kutusu"
    )
    st.session_state["kiril_metin"] = girdi
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary"):
            st.session_state["latin_sonuc"] = transliterasyon_yap(st.session_state["kiril_metin"])
            st.rerun()
            
    with btn_col2:
        if st.button("Temizle"):
            st.session_state["kiril_metin"] = ""
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_dosyasi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)"):
            if st.session_state["kiril_metin"].strip():
                try:
                    tts = gTTS(text=st.session_state["kiril_metin"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_dosyasi"] = fp.getvalue()
                except:
                    st.error("Ses dosyası oluşturulamadı.")
                st.rerun()
                
    st.write("Latin Alfabesi Sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_sonuc"],
        height=150,
        disabled=True,
        key="latin_cikti_kutusu",
        label_visibility="collapsed"
    )
    
    if st.session_state["ses_dosyasi"] and st.session_state["kiril_metin"].strip():
        st.audio(st.session_state["ses_dosyasi"], format='audio/mp3')

st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesindeki ses karşılıklarına dönüştürülmesidir.")

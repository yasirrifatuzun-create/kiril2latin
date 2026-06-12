import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# CSS: Sadece sol sütundaki butonları kare yapar, sağdaki butonlara asla dokunmaz
st.markdown("""
    <style>
    /* Sol sütunun (sanal klavye) altındaki sütun boşluklarını sıfırla */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] {
        padding: 2px !important;
        margin: 0px !important;
    }
    
    #klavye_alani button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
    }
    
    /* Sağ sütundaki işlem butonlarının yüksekliğini sabitler, kare olmalarını engeller */
    #islem_alani button {
        height: 45px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Karşılık tablosundaki hatalı 'm' harfi 'n' olarak düzeltildi
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
    'Ъ': "'", 'ъ': "'", 'Ъ': "'", 'ъ': "'", 'Ы': 'I', 'ы': 'ı', 
    'Ь': "^", 'ь': "^", 'Э': 'E', 'э': 'e', 'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya', 'я': 'ya'
}

def transliterasyon_yap(metin):
    sonuc = ""
    for karakter in metin:
        sonuc += RUSCA_KIRIL_TABLO.get(karakter, karakter)
    return sonuc

# --- BELLEK AYARLARI ---
if "kiril_input" not in st.session_state:
    st.session_state["kiril_input"] = ""
if "latin_output" not in st.session_state:
    st.session_state["latin_output"] = ""
if "ses_data" not in st.session_state:
    st.session_state["ses_data"] = None

# Klavyeden harf ekleme tetikleyicisi
def klik_harf(harf):
    st.session_state["kiril_input"] += harf

st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın veya soldaki sanal klavyeyi kullanın.")

sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Sanal Klavye")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "y"), ("К", "k"), ("Л", "l"), ("М", "m"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ç"), ("Ш", "ş"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # CSS'in sadece burayı etkilemesi için div alanı tanımlıyoruz
    st.markdown('<div id="klavye_alani">', unsafe_allow_html=True)
    
    for i in range(0, len(kiril_harfleri), 7):
        grup = kiril_harfleri[i:i+7]
        klavye_cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with klavye_cols[idx * 2]:
                st.button(buyuk, key=f"kb_{buyuk}_{i}_{idx}", on_click=klik_harf, args=(buyuk,))
            with klavye_cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"kk_{kucuk}_{i}_{idx}", on_click=klik_harf, args=(kucuk,))
                
    st.markdown('</div>', unsafe_allow_html=True)

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    st.markdown('<div id="islem_alani">', unsafe_allow_html=True)
    
    # Anlık güncellenen giriş alanı
    st.session_state["kiril_input"] = st.text_input(
        "Kiril Metin Girişi:",
        value=st.session_state["kiril_input"],
        key="kiril_yazi_alani"
    )
    
    st.write("") # Boşluk
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_output"] = transliterasyon_yap(st.session_state["kiril_input"])
            st.rerun()
            
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_input"] = ""
            st.session_state["latin_output"] = ""
            st.session_state["ses_data"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            metin = st.session_state["kiril_input"]
            if metin.strip():
                try:
                    tts = gTTS(text=metin, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_data"] = fp.getvalue()
                except:
                    st.error("Ses üretilemedi.")
                st.rerun()
                
    st.write("Latin Alfabesi Sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_output"],
        height=100,
        disabled=True,
        key="latin_sonuc_penceresi",
        label_visibility="collapsed"
    )
    
    if st.session_state["ses_data"] and st.session_state["kiril_input"].strip():
        st.audio(st.session_state["ses_data"], format='audio/mp3')
        
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesine harf eşlemesidir.")

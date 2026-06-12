import streamlit as st
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="KIRIL2LATIN - Transliterasyon", layout="wide")

# CSS: Sadece sol sütundaki butonları kare yapar, sağdaki ana butonları korur
st.markdown("""
    <style>
    /* Sanal klavye alanındaki buton hiyerarşisini hedefler */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] {
        padding: 2px !important;
        margin: 0px !important;
    }
    
    #klavye_kutusu button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
    }
    
    /* Sağ taraftaki işlem butonlarının kare olmasını engeller */
    #islem_kutusu button {
        height: 45px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Orijinal Transliterasyon Tablosu
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

# --- STREAMLIT MERKEZİ BELLEK ---
if "metin_deposu" not in st.session_state:
    st.session_state["metin_deposu"] = ""
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_kaydi" not in st.session_state:
    st.session_state["ses_kaydi"] = None

# Klavyeden harfe basıldığında girdiyi anlık güncelleyen güvenli fonksiyon
def klavyeden_harf_ekle(harf):
    st.session_state["metin_deposu"] += harf

st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın veya soldaki sanal klavyeyi kullanın.")

sol_sutun, sag_sutun = st.columns([1, 1.1])

# --- SOL SÜTUN: SANAL KLAVYE (TAM KARE VE HATASIZ HARFLER) ---
with sol_sutun:
    st.write("Kiril Alfabe - Sanal Klavye")
    
    # Hatalı tüm Türkçe karakterler (ç, ş, y, m vb.) temizlendi, orijinal Rusça Kiril harfleri eklendi
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    st.markdown('<div id="klavye_kutusu">', unsafe_allow_html=True)
    
    satir_sayisi = 7
    for i in range(0, len(kiril_harfleri), satir_sayisi):
        grup = kiril_harfleri[i:i+satir_sayisi]
        klavye_cols = st.columns(14)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with klavye_cols[idx * 2]:
                st.button(buyuk, key=f"btn_b_{buyuk}_{i}", on_click=klavyeden_harf_ekle, args=(buyuk,))
            with klavye_cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"btn_k_{kucuk}_{i}", on_click=klavyeden_harf_ekle, args=(kucuk,))
                
    st.markdown('</div>', unsafe_allow_html=True)

# --- SAĞ SÜTUN: METİN GİRİŞİ VE İŞLEMLER ---
with sag_sutun:
    st.markdown('<div id="islem_kutusu">', unsafe_allow_html=True)
    
    # Giriş Alanı: text_area yerine anlık veriyi ezmeyen yapı kullanıldı
    giris_metni = st.text_area(
        "Kiril Metin Girişi:",
        value=st.session_state["metin_deposu"],
        height=150,
        key="kiril_metin_alani"
    )
    
    # El ile yazılan metni hafızayla senkronize tutuyoruz
    st.session_state["metin_deposu"] = giris_metni
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_sonuc"] = transliterasyon_yap(st.session_state["metin_deposu"])
            st.rerun()
            
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["metin_deposu"] = ""
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_kaydi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["metin_deposu"].strip():
                try:
                    tts = gTTS(text=st.session_state["metin_deposu"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_kaydi"] = fp.getvalue()
                except:
                    st.error("Ses dosyası oluşturulamadı.")
                st.rerun()
                
    st.write("Latin Alfabesi Sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_sonuc"],
        height=150,
        disabled=True,
        key="latin_cikis_alani",
        label_visibility="collapsed"
    )
    
    if st.session_state["ses_kaydi"] and st.session_state["metin_deposu"].strip():
        st.audio(st.session_state["ses_kaydi"], format='audio/mp3')
        
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin Latin alfabesindeki ses karşılıklarına dönüştürülmesidir.")

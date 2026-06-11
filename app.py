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

# --- KESİNTİSİZ TEK MERKEZLİ HAFIZA ---
if "stabil_metin" not in st.session_state:
    st.session_state["stabil_metin"] = ""
if "latin_cikti" not in st.session_state:
    st.session_state["latin_cikti"] = ""
if "ses_oynatici" not in st.session_state:
    st.session_state["ses_oynatici"] = None

# Sanal klavye basışlarını hafızaya alan kararlı fonksiyon
def harf_bas(harf):
    st.session_state["stabil_metin"] += harf

# Başlıklar
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
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"), 
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

# --- SAĞ SÜTUN: VERİ ALANI VE AKSİYONLAR ---
with sag_sutun:
    
    # Giriş Alanı: Doğrudan harf_bas veya el yazısıyla beslenen ana bileşen
    girdi_kutusu = st.text_area(
        "Kiril Metin Girişi", 
        value=st.session_state["stabil_metin"],
        height=180,
        key="kiril_yazi_alani_yeni",
        label_visibility="collapsed"
    )
    
    # El yazısıyla gelen değişikliği anında algıla ve hafızaya al
    if girdi_kutusu != st.session_state["stabil_metin"]:
        st.session_state["stabil_metin"] = girdi_kutusu

    # İşlem Butonları
    b1, b2, b3 = st.columns(3)
    
    with b1:
        # DÖNÜŞTÜR BUTTON: Hafızadaki güncel metni alır ve sağdaki kutuyu doldurur
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_cikti"] = transliterasyon_yap(st.session_state["stabil_metin"])
            st.rerun()
            
    with b2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["stabil_metin"] = ""
            st.session_state["latin_cikti"] = ""
            st.session_state["ses_oynatici"] = None
            st.rerun()
            
    with b3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["stabil_metin"].strip():
                try:
                    tts = gTTS(text=st.session_state["stabil_metin"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_oynatici"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses sentezlenemedi.")
            st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Çıktı Kutusu
    st.text_area(
        "",
        value=st.session_state["latin_cikti"],
        height=180,
        disabled=True,
        key="latin_cikti_alani_yeni",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_oynatici"] is not None and st.session_state["stabil_metin"].strip():
        st.audio(st.session_state["ses_oynatici"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

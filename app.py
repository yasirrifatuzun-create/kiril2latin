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

# --- MERKEZİ GÜVENLİ HAFIZA SİSTEMİ ---
if "ana_metin" not in st.session_state:
    st.session_state["ana_metin"] = ""
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_verisi" not in st.session_state:
    st.session_state["ses_verisi"] = None

# Sanal klavye butonları için kilit kırma fonksiyonu
def harf_ekle_callback(harf):
    # Eğer input alanında el yazısı varsa önce onu session_state ile eşitle
    if "kiril_input_widget" in st.session_state:
        st.session_state["ana_metin"] = st.session_state["kiril_input_widget"]
    
    # Üzerine sanal klavyeden gelen harfi ekle
    st.session_state["ana_metin"] += harf
    # Canlı önizleme için dönüşümü anında yap
    st.session_state["latin_sonuc"] = transliterasyon_yap(st.session_state["ana_metin"])

# Başlıklar
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
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
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_ekle_callback, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_ekle_callback, args=(kucuk,))

# --- SAĞ SÜTUN: KİLİTLENMEYEN METİN ALANLARI VE AKSİYONLAR ---
with sag_sutun:
    
    # Giriş Alanı: Doğrudan session_state nesnesine bağlandı, çakışma ihtimali sıfırlandı
    kiril_girdi = st.text_area(
        "Kiril Metin Girişi", 
        value=st.session_state["ana_metin"],
        height=180,
        key="kiril_input_widget",
        label_visibility="collapsed"
    )
    
    # Kullanıcı elle yazıp alanı değiştirdiyse hafızayı güncelle
    if kiril_girdi != st.session_state["ana_metin"]:
        st.session_state["ana_metin"] = kiril_girdi
        st.session_state["latin_sonuc"] = transliterasyon_yap(kiril_girdi)

    # 3'lü İşlem Butonları
    b1, b2, b3 = st.columns(3)
    
    with b1:
        # DÖNÜŞTÜR BUTONU: Kutudaki en son el yazısını zorla çeker ve dönüştürür
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["ana_metin"] = kiril_girdi
            st.session_state["latin_sonuc"] = transliterasyon_yap(kiril_girdi)
            st.rerun()
            
    with b2:
        # TEMİZLE BUTONU: Tüm sistemi sıfırlar
        if st.button("Temizle", use_container_width=True):
            st.session_state["ana_metin"] = ""
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_verisi"] = None
            if "kiril_input_widget" in st.session_state:
                st.session_state["kiril_input_widget"] = ""
            st.rerun()
            
    with b3:
        # SESLE OKU BUTONU
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            st.session_state["ana_metin"] = kiril_girdi
            st.session_state["latin_sonuc"] = transliterasyon_yap(kiril_girdi)
            if kiril_girdi.strip():
                try:
                    tts = gTTS(text=kiril_girdi, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_verisi"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses motoru hatası.")
            st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Salt Okunur Çıktı Kutusu
    st.text_area(
        "",
        value=st.session_state["latin_sonuc"],
        height=180,
        disabled=True,
        key="latin_output_widget",
        label_visibility="collapsed"
    )

    # Ses Oynatıcı
    if st.session_state["ses_verisi"] is not None and st.session_state["ana_metin"].strip():
        st.audio(st.session_state["ses_verisi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

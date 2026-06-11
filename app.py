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

# --- ASLA KİLİTLENMEYEN GÜVENLİ TEK HAFIZA ---
if "metin_hafizasi" not in st.session_state:
    st.session_state["metin_hafizasi"] = ""
if "latin_cikti" not in st.session_state:
    st.session_state["latin_cikti"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Sanal klavyeden harf ekleme fonksiyonu
def harf_ekle(harf):
    st.session_state["metin_hafizasi"] += harf

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
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(kucuk,))

# --- SAĞ SÜTUN: O İSTEDİĞİN ŞIK İKİ BÜYÜK KUTULU DÜZEN ---
with sag_sutun:
    
    # Kilitlenmeyen ve el yazısını da klavyeyi de anında kabul eden modern Giriş Kutusu
    kiril_metin_alani = st.text_area(
        "", 
        value=st.session_state["metin_hafizasi"],
        height=180,
        key="kiril_kutusu_orijinal",
        label_visibility="collapsed"
    )
    
    # Kullanıcı elle yazdıysa hafızayı sessizce senkronize et
    if kiril_metin_alani != st.session_state["metin_hafizasi"]:
        st.session_state["metin_hafizasi"] = kiril_metin_alani

    # Orijinal 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTONU
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_cikti"] = transliterasyon_yap(st.session_state["metin_hafizasi"])
            st.rerun()
        
    with btn_col2:
        # TEMİZLE BUTONU
        if st.button("Temizle", use_container_width=True):
            st.session_state["metin_hafizasi"] = ""
            st.session_state["latin_cikti"] = ""
            st.session_state["ses_deposu"] = None
            st.rerun()
            
    with btn_col3:
        # SESLE OKU BUTONU
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if st.session_state["metin_hafizasi"].strip():
                try:
                    tts = gTTS(text=st.session_state["metin_hafizasi"], lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_deposu"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses sentezlenirken hata oluştu.")
            st.rerun()

    # Orijinal Geniş Latin Çıktı Kutusu
    st.write("Latin alfabesi sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_cikti"],
        height=180,
        disabled=True,
        key="latin_cikti_orijinal",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None and st.session_state["metin_hafizasi"].strip():
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

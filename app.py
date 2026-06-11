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

# --- STREAMLIT MERKEZİ HAFIZA ALANI ---
if "kiril_input_alani" not in st.session_state:
    st.session_state["kiril_input_alani"] = ""
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Sanal klavye butonlarına basıldığında veriyi doğrudan widget state'ine basan fonksiyon
def harf_butonu_tetiklendi(harf):
    # Giriş kutusunun o anki güncel durumunu çek ve harfi ekle
    mevcut_girdi = st.session_state.get("kiril_input_alani", "")
    yeni_girdi = mevcut_girdi + harf
    
    # Doğrudan widget'ın kendisine yeni değeri yazıyoruz (Kilit kıran nokta burası)
    st.session_state["kiril_input_alani"] = yeni_girdi
    st.session_state["latin_sonuc"] = transliterasyon_yap(yeni_girdi)
    st.session_state["ses_deposu"] = None

# Üst Başlık Alanı
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

# --- SAĞ SÜTUN: METİN GİRİŞİ VE REAL-TIME DÖNÜŞTÜRME ---
with sag_sutun:
    
    # Giriş Alanı - 'value=' parametresi kaldırılarak tüm kilitlenmeler %100 tarihe gömüldü
    st.text_area(
        "", 
        height=180,
        key="kiril_input_alani",
        label_visibility="collapsed"
    )
    
    # Kullanıcının o an kutuda yazdığı metni güvenle yakalıyoruz
    guncel_kiril_metin = st.session_state.get("kiril_input_alani", "")

    # Butonlar Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTONU: Basıldığı an kutudaki metni Latin alfabesine dönüştürür ve ekrana basar
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_sonuc"] = transliterasyon_yap(guncel_kiril_metin)
            st.rerun()
        
    with btn_col2:
        # TEMİZLE BUTONU: Hafızadaki her şeyi tamamen sıfırlar
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_input_alani"] = ""
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_deposu"] = None
            st.rerun()
            
    with btn_col3:
        # SESLE OKU BUTONU
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if guncel_kiril_metin.strip():
                try:
                    tts_ru = gTTS(text=guncel_kiril_metin, lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_deposu"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses dosyası oluşturulamadı.")
                st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Kullanıcı butona basmasa bile el yazısıyla canlı dönüştürmeyi destekleyen emniyet subabı
    if guncel_kiril_metin:
        anlik_sonuc = transliterasyon_yap(guncel_kiril_metin)
    else:
        anlik_sonuc = ""

    # Giriş kutusuyla tamamen simetrik ve asla kilitlenmeyen sonuç alanı
    st.text_area(
        "",
        value=anlik_sonuc,
        height=180,
        disabled=True,
        key="latin_output_alani",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None and guncel_kiril_metin.strip():
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

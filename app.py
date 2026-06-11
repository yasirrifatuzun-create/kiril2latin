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

# --- HAFIZA AYARLARI ---
if "kiril_kutusu" not in st.session_state:
    st.session_state["kiril_kutusu"] = ""
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Kilitlenmeyi önleyen buton fonksiyonu
def harf_ekle(harf):
    # Ekranda o an yazan metni session_state'den çekip üzerine harfi ekliyoruz
    st.session_state["kiril_kutusu"] = st.session_state.get("kiril_kutusu", "") + harf

# Başlıklar (Orijinal Tasarım)
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

# --- SAĞ SÜTUN: ASLA KİLİTLENMEYEN GİRİŞ/ÇIKTI KUTULARI ---
with sag_sutun:
    
    # GİRİŞ KUTUSU: Değişken çakışması yapmaması için 'value' parametresi kaldırıldı.
    # Doğrudan canlı hücreye ('key') bağlı. Asla donmaz, butonları kilitlemez.
    kiril_girdisi = st.text_area(
        "", 
        height=180,
        key="kiril_kutusu",
        label_visibility="collapsed"
    )

    # 3'lü Buton Sırası (Birebir Aynı Tasarım)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTONU: Kutuda o an ne varsa anında yakalar ve transliterasyon yapar
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_sonuc"] = transliterasyon_yap(kiril_girdisi)
            st.rerun()
        
    with btn_col2:
        # TEMİZLE BUTONU: Tüm girdileri ve çıktıları sıfırlar
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_kutusu"] = ""
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_deposu"] = None
            st.rerun()
            
    with btn_col3:
        # SESLE OKU BUTONU
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if kiril_girdisi.strip():
                try:
                    tts = gTTS(text=kiril_girdisi, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_deposu"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses sentezlenemedi.")
            st.rerun()

    # Orijinal Çıktı Kutusu
    st.write("Latin alfabesi sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_sonuc"],
        height=180,
        disabled=True,
        key="latin_sonuc_orijinal_kutusu",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None and kiril_girdisi.strip():
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

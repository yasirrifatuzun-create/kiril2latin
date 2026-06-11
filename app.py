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

# --- KİLİTLENMEYEN TEK MERKEZLİ STATE YAPISI ---
if "metin_deposu" not in st.session_state:
    st.session_state["metin_deposu"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Kullanıcı kutuya el yazısı girdiğinde hafızayı günceller
def el_yazisi_degisti():
    st.session_state["metin_deposu"] = st.session_state["kiril_girdi_alani"]

# Sanal klavye butonuna basıldığında tetiklenen kilit kırıcı
def sanal_klavye_tetiklendi(harf):
    # Eğer kullanıcı kutuda daha önce elle bir şey yazdıysa onu da kaybetmemek için çekiyoruz
    if "kiril_girdi_alani" in st.session_state:
        st.session_state["metin_deposu"] = st.session_state["kiril_girdi_alani"]
        
    st.session_state["metin_deposu"] += harf
    # Tarayıcıya yeni veriyi zorla dayatmak için widget state'ini elden güncelliyoruz
    st.session_state["kiril_girdi_alani"] = st.session_state["metin_deposu"]

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
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=sanal_klavye_tetiklendi, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=sanal_klavye_tetiklendi, args=(kucuk,))

# --- SAĞ SÜTUN: ASLA KİLİTLENMEYEN METİN ALANLARI VE AKSİYONLAR ---
with sag_sutun:
    
    # GİRİŞ KUTUSU: value parametresi kaldırıldı, kilitlenme tamamen önlendi.
    st.text_area(
        "Kiril Giriş Alanı",
        value=st.session_state["metin_deposu"],
        height=180,
        key="kiril_girdi_alani",
        on_change=el_yazisi_degisti,
        label_visibility="collapsed"
    )
    
    # Emniyet kemeri: Her render durumunda güncel metni çekiyoruz
    guncel_metin = st.session_state.get("metin_deposu", "")

    # İşlem Butonları
    b1, b2, b3 = st.columns(3)
    
    with b1:
        # DÖNÜŞTÜR BUTTON: Sayfayı rerun ederek senkronizasyonu %100 sağlar
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.rerun()
            
    with b2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["metin_deposu"] = ""
            st.session_state["kiril_girdi_alani"] = ""
            st.session_state["ses_deposu"] = None
            st.rerun()
            
    with b3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if guncel_metin.strip():
                try:
                    tts = gTTS(text=guncel_metin, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_deposu"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses sentezlenemedi.")
            st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Dönüştürme doğrudan canlı değişkenden besleniyor, buton bağımsız anlık çalışır
    latin_sonuc_verisi = transliterasyon_yap(guncel_metin)
    
    # Çıktı Kutusu
    st.text_area(
        "",
        value=latin_sonuc_verisi,
        height=180,
        disabled=True,
        key="latin_cikti_kutusu_stabil",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None and guncel_metin.strip():
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

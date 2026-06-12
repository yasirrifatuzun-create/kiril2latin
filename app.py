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

# --- STREAMLIT MERKEZİ BELLEK AYARLARI ---
if "kiril_metin" not in st.session_state:
    st.session_state["kiril_metin"] = ""
if "latin_metin" not in st.session_state:
    st.session_state["latin_metin"] = ""
if "ses_dosyasi" not in st.session_state:
    st.session_state["ses_dosyasi"] = None

# Sanal klavyeden harf ekleme tetikleyicisi
def klavyeden_ekle(harf):
    st.session_state["kiril_metin"] += harf
    st.session_state["latin_metin"] = transliterasyon_yap(st.session_state["kiril_metin"])

# Üst Başlık Alanı
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanın.")

# --- İKİ SÜTUNLU ANA DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: SANAL KLAVYE (İlk Çalışan Yapınız) ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"),
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "м"),
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "т"), ("У", "у"),
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"),
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    satir_genisligi = 7
    for i in range(0, len(kiril_harfleri), satir_genisligi):
        grup = kiril_harfleri[i:i+satir_genisligi]
        klavye_cols = st.columns(len(grup) * 2)
        
        for idx, (buyuk, kucuk) in enumerate(grup):
            with klavye_cols[idx * 2]:
                st.button(buyuk, key=f"b_{buyuk}_{i+idx}", use_container_width=True, on_click=klavyeden_ekle, args=(buyuk,))
            with klavye_cols[(idx * 2) + 1]:
                st.button(kucuk, key=f"k_{kucuk}_{i+idx}", use_container_width=True, on_click=klavyeden_ekle, args=(kucuk,))

# --- SAĞ SÜTUN: METİN GİRİŞİ VE TAMİR EDİLEN BUTONLAR ---
with sag_sutun:
    
    # Giriş Alanı
    giris_alani = st.text_area(
        "",
        value=st.session_state["kiril_metin"],
        height=180,
        key="kiril_yazi_kutusu",
        label_visibility="collapsed"
    )

    # 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÜZELTME: Butona basıldığında text_area'nın o anki canlı değerini doğrudan okur
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["kiril_metin"] = giris_alani
            st.session_state["latin_metin"] = transliterasyon_yap(giris_alani)
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["kiril_metin"] = ""
            st.session_state["latin_metin"] = ""
            st.session_state["ses_dosyasi"] = None
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            # DÜZELTME: Gecikmeyi önlemek için canlı giris_alani verisi aktarıldı
            st.session_state["kiril_metin"] = giris_alani
            if giris_alani.strip():
                try:
                    tts_ru = gTTS(text=giris_alani, lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_dosyasi"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses dosyası üretilemedi.")
                st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Çıktı Kutusu
    st.text_area(
        "",
        value=st.session_state["latin_metin"],
        height=180,
        disabled=True,
        key="latin_sonuc_kutusu",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_dosyasi"] is not None and st.session_state["kiril_metin"].strip():
        st.audio(st.session_state["ses_dosyasi"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

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

# --- EN GÜVENLİ HAFIZA SİSTEMİ ---
if "klavye_buffer" not in st.session_state:
    st.session_state["klavye_buffer"] = ""
if "latin_cikti" not in st.session_state:
    st.session_state["latin_cikti"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

# Butona basıldığında harfi hafızaya ekleyen fonksiyon
def harf_tiklandi(harf):
    st.session_state["klavye_buffer"] += harf

# Başlıklar
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")

# --- İKİ SÜTUNLU DÜZEN ---
sol_sutun, sag_sutun = st.columns([1, 1.2])

# --- SOL SÜTUN: SANAL KLAVYE ---
with sol_sutun:
    st.write("Kiril Alfabe - Alfabetik Sıra")
    
    kiril_harfleri = [
        ("А", "а"), ("Б", "б"), ("В", "в"), ("Г", "г"), ("Д", "д"), ("Е", "е"), ("Ё", "ё"), 
        ("Ж", "ж"), ("З", "з"), ("И", "и"), ("Й", "й"), ("К", "к"), ("Л", "л"), ("М", "m"), 
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "t"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14)
            
        col_idx = index % 7
        
        with klavye_cols[col_idx * 2]:
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_tiklandi, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_tiklandi, args=(kucuk,))

# --- SAĞ SÜTUN: ASLA HATA VERMEYEN DÜZEN ---
with sag_sutun:
    
    # Sanal klavyeden yazılan harflerin anlık biriktiği güvenli alan
    if st.session_state["klavye_buffer"]:
        st.info(f"Sanal Klavyeden Yazılan: {st.session_state['klavye_buffer']}")
    
    # GİRİŞ ALANI: Race condition (yarış durumu) yaratmaması için ne 'value' ne 'on_change' var. 
    # Tamamen bağımsız bir text_input. Kopyala/yapıştır veya el yazısını buraya yazıyorsun.
    girdi_metni = st.text_input(
        "Kiril Metni Buraya Yazın veya Sanal Klavyeyi Kullanın:", 
        placeholder="Kopyala-yapıştır yapabilir veya yazabilirsiniz...",
        key="kiril_girdi_kutusu_nihai"
    )

    # 3'lü Buton Sırası
    b1, b2, b3 = st.columns(3)
    
    with b1:
        # DÖNÜŞTÜR BUTTON: Hangi kaynaktan veri gelirse gelsin kilitlenmeden okur
        if st.button("Dönüştür", type="primary", use_container_width=True):
            # Eğer kutu boşsa ama sanal klavyede yazı varsa onu baz al
            final_metin = girdi_metni if girdi_metni else st.session_state["klavye_buffer"]
            st.session_state["latin_cikti"] = transliterasyon_yap(final_metin)
            st.rerun()
            
    with b2:
        # TEMİZLE BUTTON: Bütün hafızayı tertemiz eder
        if st.button("Temizle", use_container_width=True):
            st.session_state["klavye_buffer"] = ""
            st.session_state["latin_cikti"] = ""
            st.session_state["ses_deposu"] = None
            st.rerun()
            
    with b3:
        # SESLE OKU BUTTON
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            final_metin = girdi_metni if girdi_metni else st.session_state["klavye_buffer"]
            if final_metin.strip():
                try:
                    tts = gTTS(text=final_metin, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_deposu"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses sentezlenemedi.")
            st.rerun()

    # Sonuç Alanı
    st.write("Latin alfabesi sonucu:")
    st.success(st.session_state["latin_cikti"] if st.session_state["latin_cikti"] else "Sonuç burada görünecek.")

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None:
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

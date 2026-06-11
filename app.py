import streamlit as st
from gtts import gTTS
import io
import streamlit.components.v1 as components

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

# --- HAFIZA ALANLARI ---
if "latin_sonuc" not in st.session_state:
    st.session_state["latin_sonuc"] = ""
if "ses_deposu" not in st.session_state:
    st.session_state["ses_deposu"] = None

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
        ("Н", "н"), ("О", "о"), ("П", "п"), ("Р", "р"), ("С", "с"), ("Т", "t"), ("У", "у"), 
        ("Ф", "ф"), ("Х", "х"), ("Ц", "ц"), ("Ч", "ч"), ("Ш", "ш"), ("Щ", "щ"), ("Ъ", "ъ"), 
        ("Ы", "ы"), ("Ь", "ь"), ("Э", "э"), ("Ю", "ю"), ("Я", "я")
    ]
    
    # Harfleri ekrana buton olarak basıyoruz
    for index, (buyuk, kucuk) in enumerate(kiril_harfleri):
        if index % 7 == 0:
            klavye_cols = st.columns(14)
            
        col_idx = index % 7
        
        with klavye_cols[col_idx * 2]:
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True)
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True)

# --- SAĞ SÜTUN: ESKİ ŞIK TASARIM VE KUSURSUZ ÇALIŞAN DÜĞMELER ---
with sag_sutun:
    
    # Giriş kutusu (Tamamen bağımsız, ne value ne on_change var. Kilitlenmesi imkansız.)
    kiril_metin_alani = st.text_area(
        "", 
        height=180,
        key="kiril_girdi_pencerem",
        label_visibility="collapsed"
    )

    # 3'lü Buton Sırası (Birebir Geri Geldi)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["latin_sonuc"] = transliterasyon_yap(kiril_metin_alani)
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["latin_sonuc"] = ""
            st.session_state["ses_deposu"] = None
            # JavaScript kullanarak ana metin alanını da temizle tetikleyicisi gönderiyoruz
            components.html(
                """
                <script>
                var textarea = window.parent.document.querySelector('textarea[aria-label=""]');
                if(textarea) {
                    textarea.value = "";
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                }
                </script>
                """,
                height=0
            )
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            if kiril_metin_alani.strip():
                try:
                    tts = gTTS(text=kiril_metin_alani, lang='ru', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.session_state["ses_deposu"] = fp.getvalue()
                except Exception as e:
                    st.error("Ses motoru hatası.")
            st.rerun()

    # Orijinal Geniş Latin Sonuç Kutusu
    st.write("Latin alfabesi sonucu:")
    st.text_area(
        "",
        value=st.session_state["latin_sonuc"],
        height=180,
        disabled=True,
        key="latin_cikti_pencerem",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı
    if st.session_state["ses_deposu"] is not None and kiril_metin_alani.strip():
        st.audio(st.session_state["ses_deposu"], format='audio/mp3')

# --- JAVASCRIPT KLAVYE BAĞLANTISI ---
# Soldaki butonlara basıldığında, harfleri doğrudan yukarıdaki kutuya (textarea) enjekte eder.
js_script = """
<script>
    const buttons = window.parent.document.querySelectorAll('button');
    const textarea = window.parent.document.querySelector('textarea[aria-label=""]');
    
    buttons.forEach(button => {
        // Eğer buton bir klavye butonuysa (üzerinde tek karakter veya Kiril harfi varsa)
        if (button.innerText.length === 1 && !button.data_listener_added) {
            button.data_listener_added = true;
            button.addEventListener('click', () => {
                if (textarea) {
                    textarea.value += button.innerText;
                    // Streamlit'in değişimi fark etmesi için input event'ini tetikliyoruz
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
        }
    });
</script>
"""
components.html(js_script, height=0)

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

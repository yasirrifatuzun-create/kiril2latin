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

# --- HAFIZA ALANLARI ---
if "sanal_klavye_metni" not in st.session_state:
    st.session_state["sanal_klavye_metni"] = ""
if "final_latin" not in st.session_state:
    st.session_state["final_latin"] = ""
if "ses_data" not in st.session_state:
    st.session_state["ses_data"] = None

# Sanal klavye buton fonksiyonu
def harf_ekle(harf):
    # Eğer kullanıcı kutuya elle bir şey yazdıysa, Streamlit'in widget hafızasındaki metni çek
    if "kiril_input_box" in st.session_state:
        st.session_state["sanal_klavye_metni"] = st.session_state["kiril_input_box"]
    
    st.session_state["sanal_klavye_metni"] += harf
    # Ekranın güncellenmesi için anlık eşleme yap
    st.session_state["kiril_input_box"] = st.session_state["sanal_klavye_metni"]

# Başlıklar
st.title("KIRIL2LATIN - Transliterasyon Uygulaması")
st.caption("Kiril harfli metni sağdaki kutuya yazın/yapıştırın veya soldaki sanal klavyeyi kullanıp Dönüştür'e basın.")

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
            st.button(buyuk, key=f"b_{buyuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(buyuk,))
                
        with klavye_cols[(col_idx * 2) + 1]:
            st.button(kucuk, key=f"k_{kucuk}_{index}", use_container_width=True, on_click=harf_ekle, args=(kucuk,))

# --- SAĞ SÜTUN: METİN ALANI VE KESİN DÖNÜŞTÜRME ---
with sag_sutun:
    
    # Giriş Kutusu (Value doğrudan session_state nesnesine bağlandı)
    girilen_kiril = st.text_area(
        "", 
        value=st.session_state["sanal_klavye_metni"],
        height=180,
        key="kiril_input_box",
        label_visibility="collapsed"
    )

    # 3'lü Buton Sırası
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # DÖNÜŞTÜR BUTTON: Kutuda o an ne yazıyorsa (ister el yazısı, ister buton) yakalar ve dönüştürür.
        if st.button("Dönüştür", type="primary", use_container_width=True):
            st.session_state["sanal_klavye_metni"] = girilen_kiril
            st.session_state["final_latin"] = transliterasyon_yap(girilen_kiril)
            st.rerun()
        
    with btn_col2:
        if st.button("Temizle", use_container_width=True):
            st.session_state["sanal_klavye_metni"] = ""
            st.session_state["final_latin"] = ""
            st.session_state["ses_data"] = None
            if "kiril_input_box" in st.session_state:
                st.session_state["kiril_input_box"] = ""
            st.rerun()
            
    with btn_col3:
        if st.button("Sesle Oku (Kiril)", use_container_width=True):
            st.session_state["sanal_klavye_metni"] = girilen_kiril
            st.session_state["final_latin"] = transliterasyon_yap(girilen_kiril)
            if girilen_kiril.strip():
                try:
                    tts_ru = gTTS(text=girilen_kiril, lang='ru', slow=False)
                    fp_ru = io.BytesIO()
                    tts_ru.write_to_fp(fp_ru)
                    st.session_state["ses_data"] = fp_ru.getvalue()
                except Exception as e:
                    st.error("Ses dosyası oluşturulamadı.")
            st.rerun()

    # Sonuç Alanı Başlığı
    st.write("Latin alfabesi sonucu:")
    
    # Canlı takip mekanizması (Eğer kullanıcı butona basmadan elle yazıyorsa arkada dönüştürür)
    if girilen_kiril and not st.session_state["final_latin"]:
        st.session_state["final_latin"] = transliterasyon_yap(girilen_kiril)
    elif not girilen_kiril:
        st.session_state["final_latin"] = ""

    # Çıktı Kutusu
    st.text_area(
        "",
        value=st.session_state["final_latin"],
        height=180,
        disabled=True,
        key="latin_output_box",
        label_visibility="collapsed"
    )

    # Ses oynatıcısı (Hatalı syntax temizlendi)
    if st.session_state["ses_data"] is not None and girilen_kiril.strip():
        st.audio(st.session_state["ses_data"], format='audio/mp3')

# Alt Bilgi
st.write("---")
st.caption("Not: Bu bir çeviri değil, Kiril harflerin-Latin alfabesine karşılıklarının yazdırılmasıdır.")

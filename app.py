# --- SAĞ SÜTUN: METİN GİRİŞİ VE KESİN DÖNÜŞTÜRME ---
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
        # ÇÖZÜM: Butona basıldığı an session_state yerine DOĞRUDAN giris_alani'nı okuyoruz
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
            # Buradaki ses motorunu da giris_alani ile senkronize ediyoruz
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

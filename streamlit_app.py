# APLIKASI ASISTEN RANGKUM MATERI + GENERATE KODE
# Dengan pilihan AI: Groq (Llama 3) atau Gemini (Flash Lite)

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Load API key dari .env
load_dotenv()

# Import modul AI
from modules.utils import extract_text_from_file
from modules.ai_gemini import rangkum_dengan_gemini, generate_kode_gemini
from modules.ai_groq import rangkum_dengan_groq, generate_kode_groq

# Konfigurasi halaman
st.set_page_config(
    page_title="Asisten Rangkum Materi AI",
    page_icon="📚",
    layout="wide"
)

# ========== HEADER ==========
st.title("📚 Asisten Rangkum Materi + Generate Kode")
st.caption("Pilih AI favoritmu, upload materi, dapatkan rangkuman instan!")

# ========== CEK API KEY ==========
cek_gemini = os.getenv("GEMINI_API_KEY")
cek_groq = os.getenv("GROQ_API_KEY")

if not cek_gemini and not cek_groq:
    st.error("❌ API Key tidak ditemukan! Buat file .env dari .env.example dan isi API key kamu.")
    st.stop()
elif not cek_gemini:
    st.warning("⚠️ GEMINI_API_KEY tidak ditemukan. Fitur Gemini tidak tersedia.")
elif not cek_groq:
    st.warning("⚠️ GROQ_API_KEY tidak ditemukan. Fitur Groq tidak tersedia.")

# ========== SIDEBAR: PILIH AI & UPLOAD ==========
with st.sidebar:
    st.header("🤖 1. Pilih AI")
    
    # Tentukan opsi AI yang tersedia
    ai_options = []
    if cek_groq:
        ai_options.append("Groq (Llama 3 - Cepat)")
    if cek_gemini:
        ai_options.append("Gemini (Google - Akurat)")
    
    if not ai_options:
        st.error("Tidak ada AI yang tersedia. Periksa API key di file .env")
        st.stop()
    
    pilihan_ai = st.radio(
        "Model AI yang ingin digunakan:",
        ai_options,
        help="Groq lebih cepat, Gemini lebih akurat untuk teks panjang"
    )
    
    st.divider()
    
    st.header("📤 2. Upload Materi")
    uploaded_file = st.file_uploader(
        "Pilih file materi (PDF, TXT)",  
        type=["pdf", "txt"],
        help="Upload file PDF atau TXT. File DOCX belum support untuk sementara."
    )
    
    if uploaded_file:
        st.success(f"✅ File siap: {uploaded_file.name}")
        st.info(f"Ukuran: {uploaded_file.size} bytes")
    
    st.divider()
    
    st.header("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini menggunakan **2 model AI berbeda**:
    - **Groq (Llama 3)**: Cepat, cocok untuk rangkuman singkat
    - **Gemini (Google)**: Akurat, cocok untuk teks panjang
    
    **Cara pakai:**
    1. Pilih AI yang kamu mau
    2. Upload file materi
    3. Klik "Rangkum Sekarang"
    """)

# ========== MAIN AREA ==========
tab1, tab2 = st.tabs(["📖 Rangkum Materi", "💻 Generate Kode"])

# ========== TAB 1: RANGKUM MATERI ==========
with tab1:
    st.subheader("📖 Rangkuman Materi")
    
    if not uploaded_file:
        st.info("📂 **Belum ada file** — Upload file materi terlebih dahulu di sidebar.")
    else:
        # Tombol rangkum
        if st.button("🔍 Rangkum Sekarang", type="primary", use_container_width=True):
            with st.spinner(f"📖 Membaca file & menghubungi {pilihan_ai}..."):
                try:
                    # Step 1: Baca file yang diupload
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Step 2: Ekstrak teks dari file
                    teks_materi = extract_text_from_file(tmp_path)
                    os.unlink(tmp_path)
                    
                    if not teks_materi or len(teks_materi.strip()) < 50:
                        st.error("❌ Gagal membaca file atau teks terlalu pendek. Pastikan file mengandung teks yang cukup.")
                    else:
                        # Step 3: Panggil AI sesuai pilihan user
                        if "Groq" in pilihan_ai:
                            with st.status("🟢 Menghubungi Groq (Llama 3)..."):
                                rangkuman = rangkum_dengan_groq(teks_materi)
                            ai_nama = "Groq (Llama 3)"
                            ai_icon = "🟢"
                        else:
                            with st.status("🔵 Menghubungi Gemini (Google)..."):
                                rangkuman = rangkum_dengan_gemini(teks_materi)
                            ai_nama = "Gemini (Google)"
                            ai_icon = "🔵"
                        
                        # Step 4: Tampilkan hasil
                        st.success(f"{ai_icon} Rangkuman dari **{ai_nama}** berhasil dibuat!")
                        
                        st.subheader("📝 Hasil Rangkuman:")
                        st.markdown(rangkuman)
                        
                        st.caption(f"📄 Sumber: **{uploaded_file.name}**")
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")
                    st.info("Coba refresh halaman atau pilih AI lain.")

# ========== TAB 2: GENERATE KODE ==========
with tab2:
    st.subheader("💻 Generate Kode Program")
    st.caption(f"Minta **{pilihan_ai}** untuk membuat kode program sesuai keinginanmu")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        bahasa = st.selectbox(
            "Bahasa pemrograman",
            ["Python", "JavaScript", "Java", "C++", "HTML/CSS", "SQL"],
            help="Pilih bahasa yang kamu inginkan"
        )
    with col2:
        st.write("")  # Spacer biar rapi
    
    perintah = st.text_area(
        "Deskripsikan kode yang kamu mau:",
        placeholder="Contoh: Buat fungsi untuk menghitung luas lingkaran\n\nAtau: Buat program sederhana untuk login dengan username dan password",
        height=120
    )
    
    if st.button("⚡ Generate Kode", type="primary", use_container_width=True):
        if not perintah:
            st.warning("✏️ Masukkan deskripsi kode terlebih dahulu.")
        else:
            with st.spinner(f"💻 {pilihan_ai} sedang menulis kode..."):
                try:
                    if "Groq" in pilihan_ai:
                        hasil = generate_kode_groq(perintah, bahasa)
                        ai_nama = "Groq (Llama 3)"
                    else:
                        hasil = generate_kode_gemini(perintah, bahasa)
                        ai_nama = "Gemini (Google)"
                    
                    st.success(f"✅ Kode dari **{ai_nama}** berhasil dibuat!")
                    
                    # Tampilkan hasil dengan syntax highlighting
                    st.code(hasil, language=bahasa.lower())
                    
                    # Tombol copy manual (Streamlit belum punya built-in copy)
                    st.caption("📋 Klik kode lalu Ctrl+C / Cmd+C untuk menyalin")
                    
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")

# ========== FOOTER ==========
st.divider()
st.caption("🚀 **Teknologi**: Google Gemini AI + Groq Llama 3 | Aplikasi ini menggabungkan 2 model AI berbeda dalam 1 platform | Tugas Agile - Asisten Belajar")
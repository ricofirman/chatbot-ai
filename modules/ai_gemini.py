# Gemini API - Model yang sudah terbukti running di komputer kamu
import google.generativeai as genai
import os

def get_gemini_model():
    """Inisialisasi model Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan di environment")
    
    genai.configure(api_key=api_key)
    # Pakai model yang sudah terbukti running di test kamu
    return genai.GenerativeModel('gemini-flash-lite-latest')

def rangkum_dengan_gemini(teks_materi):
    """Rangkum materi teks menggunakan Gemini"""
    model = get_gemini_model()
    
    # Batasi teks agar tidak terlalu panjang
    teks_terbatas = teks_materi[:5000]
    
    prompt = f"""Rangkum materi berikut dalam poin-poin penting yang jelas dan mudah dipahami.

MATERI:
{teks_terbatas}

HASIL RANGKUMAN (dalam poin):"""

    response = model.generate_content(prompt)
    return response.text

def generate_kode_gemini(perintah, bahasa="Python"):
    """Generate kode program menggunakan Gemini"""
    model = get_gemini_model()
    
    prompt = f"""Buatkan kode program {bahasa} untuk keperluan berikut:

PERINTAH: {perintah}

Berikan kode lengkap dan penjelasan singkat."""

    response = model.generate_content(prompt)
    return response.text
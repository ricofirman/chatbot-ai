# Groq API - Model yang sudah terbukti running di komputer kamu
from groq import Groq
import os

def get_groq_client():
    """Inisialisasi client Groq"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan di environment")
    
    return Groq(api_key=api_key)

def rangkum_dengan_groq(teks_materi):
    """Rangkum materi teks menggunakan Groq (Llama 3)"""
    client = get_groq_client()
    
    # Batasi teks agar tidak terlalu panjang
    teks_terbatas = teks_materi[:5000]
    
    response = client.chat.completions.create(
        # Pakai model yang sudah terbukti running di test kamu
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten AI yang membantu merangkum materi pelajaran dengan jelas dan ringkas."},
            {"role": "user", "content": f"Rangkum materi berikut dalam poin-poin penting:\n\n{teks_terbatas}"}
        ],
        max_tokens=800
    )
    return response.choices[0].message.content

def generate_kode_groq(perintah, bahasa="Python"):
    """Generate kode program menggunakan Groq"""
    client = get_groq_client()
    
    response = client.chat.completions.create(
        # Pakai model yang sudah terbukti running di test kamu
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Kamu adalah programmer expert yang membuat kode {bahasa} yang bersih dan efisien."},
            {"role": "user", "content": f"Buatkan kode {bahasa} untuk: {perintah}\n\nBerikan kode lengkap dan penjelasan singkat."}
        ],
        max_tokens=800
    )
    return response.choices[0].message.content
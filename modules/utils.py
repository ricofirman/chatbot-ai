# modules/utils.py
# Hanya support PDF dan TXT (DOCX skip untuk sementara)

import pypdf

def extract_text_from_file(file_path):
    """Ekstrak teks dari PDF atau TXT (DOCX tidak support)"""
    if file_path.endswith('.pdf'):
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif file_path.endswith('.docx'):
        return ""  # Skip DOCX untuk sementara
    else:
        return ""

def chunk_text(text, chunk_size=500, overlap=50):
    """Potong teks menjadi chunk-chunk kecil"""
    if not text:
        return []
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
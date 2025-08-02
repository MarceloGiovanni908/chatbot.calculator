import re

def clean_text(text):
    """
    Enhanced text cleaning untuk menangani spasi yang tidak konsisten dari PDF
    """
    # Hapus karakter khusus dan whitespace berlebih
    text = re.sub(r'[^\w\s=*\n()√/+\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_pdf_extracted_text(text):
    """
    Specialized cleaning untuk teks yang diekstrak dari PDF
    Menangani spasi yang tidak konsisten dan karakter khusus
    """
    # Convert to string if not already
    if not isinstance(text, str):
        text = str(text)
    
    # Normalize line breaks
    text = re.sub(r'\r\n|\r|\n', '\n', text)
    
    # Fix spacing issues around mathematical operators
    # Remove excessive spaces around equals signs
    text = re.sub(r'\s*=\s*', ' = ', text)
    
    # Fix spacing around multiplication signs
    text = re.sub(r'\s*\*\s*', ' * ', text)
    
    # Fix spacing around division signs
    text = re.sub(r'\s*/\s*', ' / ', text)
    
    # Fix spacing around plus/minus signs
    text = re.sub(r'\s*\+\s*', ' + ', text)
    text = re.sub(r'\s*-\s*', ' - ', text)
    
    # Fix spacing around parentheses
    text = re.sub(r'\s*\(\s*', ' (', text)
    text = re.sub(r'\s*\)\s*', ') ', text)
    
    # Handle square root symbol
    text = re.sub(r'√\s*', 'sqrt(', text)
    text = re.sub(r'√', 'sqrt(', text)
    
    # Fix "sisi2" to "sisi * sisi" or "sisi**2"
    text = re.sub(r'sisi\s*2', 'sisi**2', text, flags=re.IGNORECASE)
    text = re.sub(r'(\w+)\s*2(?!\d)', r'\1**2', text)  # Convert any "word2" to "word**2"
    
    # Fix common Indonesian math terms with spacing issues
    replacements = {
        'Pers egi': 'Persegi',
        'Segiti ga': 'Segitiga',
        'Panjang  *': 'Panjang *',
        'lebar': 'lebar',
        'alas  *': 'alas *',
        'tinggi': 'tinggi',
        '𝑥2': 'x**2',  # Handle mathematical notation
        'x2': 'x**2'
    }
    
    for old, new in replacements.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)
    
    # Remove multiple consecutive spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Clean up lines
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def normalize_formula_text(text):
    """
    Normalize text specifically for formula extraction
    """
    # Convert common variations
    text = text.lower()
    
    # Normalize equals signs
    text = re.sub(r'\s*=\s*', '=', text)
    
    # Normalize mathematical operators
    text = re.sub(r'\s*\*\s*', '*', text)
    text = re.sub(r'\s*/\s*', '/', text)
    text = re.sub(r'\s*\+\s*', '+', text)
    text = re.sub(r'\s*-\s*', '-', text)
    
    # Handle parentheses
    text = re.sub(r'\s*\(\s*', '(', text)
    text = re.sub(r'\s*\)\s*', ')', text)
    
    return text

if __name__ == "__main__":
    # Test dengan contoh teks yang bermasalah
    sample_messy = """Persegi Panjang  = Panjang  * lebar
Pers egi = sisi2
Segiti ga = (alas * tinggi) / 2
Mencari akar = √𝑥2"""
    
    print("Original messy text:")
    print(sample_messy)
    print("\nCleaned text:")
    print(clean_pdf_extracted_text(sample_messy))
    print("\nNormalized for formulas:")
    print(normalize_formula_text(clean_pdf_extracted_text(sample_messy)))
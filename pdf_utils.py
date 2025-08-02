import fitz
import re
import os
from preprocessing import clean_pdf_extracted_text, normalize_formula_text

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF with enhanced cleaning for mathematical content
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        # Open PDF
        doc = fitz.open(file_path)
        all_text = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            all_text += page_text + "\n"
        
        doc.close()
        
        # Apply enhanced cleaning
        cleaned_text = clean_pdf_extracted_text(all_text)
        
        if not cleaned_text.strip():
            return "Error: No readable text found in PDF."
        
        return cleaned_text
        
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def detect_pdf_path_in_message(message):
    """
    Detect PDF file path in user message with various formats
    """
    # Pattern 1: Absolute paths (Windows & Unix)
    abs_pattern = r'([A-Za-z]:[\\\/][\w\s\\\/.]+\.pdf|\/[\w\s\/\-.]+\.pdf)'
    
    # Pattern 2: Relative paths
    rel_pattern = r'([\w\s\-_.]+\.pdf)'
    
    # Pattern 3: Specific extract commands
    extract_pattern = r'(?:extract|read|process).*?([^\s]+\.pdf)'
    
    # Try patterns in order
    for pattern in [abs_pattern, extract_pattern, rel_pattern]:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def extract_and_clean_formulas(file_path):
    """
    Extract text from PDF and prepare it specifically for formula parsing
    """
    try:
        raw_text = extract_text_from_pdf(file_path)
        
        if raw_text.startswith("Error"):
            return raw_text
        
        # Apply additional formula-specific cleaning
        formula_ready_text = normalize_formula_text(raw_text)
        
        return {
            'raw_text': raw_text,
            'cleaned_text': formula_ready_text,
            'formulas_detected': detect_formula_lines(formula_ready_text)
        }
        
    except Exception as e:
        return f"Error in formula extraction: {str(e)}"

def detect_formula_lines(text):
    """
    Detect lines that contain mathematical formulas
    """
    formula_lines = []
    
    for line in text.split('\n'):
        line = line.strip()
        # Check if line contains mathematical operators and equals sign
        if ('=' in line and 
            any(op in line for op in ['*', '/', '+', '-', '**', 'sqrt', '(', ')'])):
            formula_lines.append(line)
    
    return formula_lines

if __name__ == "__main__":
    # Test with the problematic PDF
    result = extract_text_from_pdf('test.pdf')
    print("Extracted and cleaned text:")
    print(result)
    print("\nFormula lines detected:")
    formula_result = extract_and_clean_formulas('test.pdf')
    if isinstance(formula_result, dict):
        for formula in formula_result['formulas_detected']:
            print(f"- {formula}")

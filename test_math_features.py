#!/usr/bin/env python3
"""
Test script untuk fitur matematika dan terjemahan PDF chatbot
"""

from math_utils import (
    translate_indonesian_to_english,
    extract_math_formulas, 
    process_pdf_with_math,
    parse_user_math_input,
    calculate_math_expression
)

def test_translation():
    print("=== Testing Translation ===")
    
    test_texts = [
        "Persegi Panjang = Panjang * Lebar",
        "Persegi = Sisi * Sisi",
        "Luas persegi panjang sama dengan panjang dikali lebar"
    ]
    
    for text in test_texts:
        translated = translate_indonesian_to_english(text)
        print(f"Original: {text}")
        print(f"Translated: {translated}\n")

def test_formula_extraction():
    print("=== Testing Formula Extraction ===")
    
    sample_text = "Persegi Panjang = Panjang * Lebar\nPersegi = Sisi * Sisi"
    formulas = extract_math_formulas(sample_text)
    
    print(f"Sample text: {sample_text}")
    print(f"Extracted formulas: {len(formulas)}")
    for i, formula in enumerate(formulas, 1):
        print(f"  {i}. {formula}")
    print()

def test_user_input_parsing():
    print("=== Testing User Input Parsing ===")
    
    test_inputs = [
        "calculate 5 + 3",
        "compute 10 * 2",
        "length=10, width=5",
        "side=4",
        "just some random text"
    ]
    
    for input_text in test_inputs:
        result = parse_user_math_input(input_text)
        print(f"Input: '{input_text}'")
        print(f"Parsed: {result}\n")

def test_pdf_processing():
    print("=== Testing PDF Processing ===")
    
    # Test dengan file test.pdf yang ada
    try:
        result = process_pdf_with_math("test.pdf")
        print("PDF Processing Result:")
        if isinstance(result, dict):
            print(f"Original text: {result['original_text'][:100]}...")
            print(f"Translated text: {result['translated_text'][:100]}...")
            print(f"Formulas found: {len(result['formulas'])}")
            for formula in result['formulas']:
                print(f"  - {formula}")
        else:
            print(result)
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("🧪 Testing Enhanced Chatbot Math Features\n")
    
    test_translation()
    test_formula_extraction()
    test_user_input_parsing()
    test_pdf_processing()
    
    print("✅ All tests completed!")

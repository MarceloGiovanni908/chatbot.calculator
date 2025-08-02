#!/usr/bin/env python3
"""
Test script untuk PDF extraction functionality
"""

from pdf_utils import extract_text_from_pdf, detect_pdf_path_in_message

def test_pdf_functions():
    print("=== Testing PDF Extractor Functions ===\n")
    
    # Test 1: File detection
    print("1. Testing PDF path detection:")
    test_messages = [
        "extract pdf C:\\Documents\\test.pdf",
        "Can you read myfile.pdf",
        "extract text from /home/user/document.pdf",
        "just extract some pdf"
    ]
    
    for msg in test_messages:
        detected = detect_pdf_path_in_message(msg)
        print(f"   Message: '{msg}'")
        print(f"   Detected path: {detected}\n")
    
    # Test 2: Error handling for non-existent file
    print("2. Testing error handling:")
    result = extract_text_from_pdf("nonexistent.pdf")
    print(f"   Result: {result}\n")
    
    print("3. Testing with invalid file extension:")
    result = extract_text_from_pdf("test.txt")
    print(f"   Result: {result}\n")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_pdf_functions()

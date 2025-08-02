#!/usr/bin/env python3
"""
Test chatbot dengan fitur PDF dan matematika yang sudah diupgrade
"""

from chat import get_response

def test_chatbot_features():
    print("🤖 Testing Enhanced Chatbot Features")
    print("="*50)
    
    # Test cases untuk berbagai fitur
    test_cases = [
        # Basic greetings
        ("Hi", "Basic greeting"),
        
        # PDF extraction
        ("extract pdf test.pdf", "PDF extraction"),
        
        # PDF math processing  
        ("process PDF with math test.pdf", "PDF math processing"),
        
        # Mathematical calculations
        ("calculate 5 + 3", "Simple addition"),
        ("compute 10 * 2", "Simple multiplication"),
        ("calculate 15 - 7", "Simple subtraction"),
        
        # Variable calculations
        ("length=10, width=5", "Rectangle calculation"),
        ("side=4", "Square calculation"),
        
        # Edge cases
        ("what is 100 / 0", "Division by zero test"),
        ("some random text", "Unrecognized input"),
    ]
    
    for i, (user_input, description) in enumerate(test_cases, 1):
        print(f"\n{i}. Test: {description}")
        print(f"   User: {user_input}")
        response = get_response(user_input)
        print(f"   Bot: {response}")
        print("-" * 50)
    
    print("\n✅ All chatbot tests completed!")

if __name__ == "__main__":
    test_chatbot_features()

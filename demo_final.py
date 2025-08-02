#!/usr/bin/env python3
"""
Demo Final Chatbot dengan PDF + Math Processing
"""

from chat import get_response

def demo_final():
    print("🚀 DEMO FINAL - Enhanced Math Chatbot")
    print("="*60)
    print("Fitur yang tersedia:")
    print("1. ✅ PDF Text Extraction")
    print("2. ✅ PDF Math Processing (Indonesian → English + Formula Detection)")
    print("3. ✅ Mathematical Calculations (+, -, *, /)")
    print("4. ✅ Geometric Area Calculations (Rectangle & Square)")
    print("="*60)
    
    demo_cases = [
        ("Hi there!", "🤝 Greeting"),
        
        ("extract pdf test.pdf", "📄 PDF Text Extraction"),
        
        ("process PDF with math test.pdf", "🔬 PDF Math Processing\n   (Indonesian→English + Formula Detection)"),
        
        ("calculate 15 + 25", "🧮 Simple Addition"),
        ("compute 100 - 37", "🧮 Simple Subtraction"),
        ("calculate (2 + 3) * 4", "🧮 Complex Expression"),
        ("calculate 2**3", "🧮 Power"), 
        ("calculate 8 * 12", "🧮 Simple Multiplication"),
        ("calculate 144 / 12", "🧮 Simple Division"),
        
        ("length=12, width=8", "📐 Rectangle (FIXED)"),
        ("side=7", "⬜ Square (FIXED)"),
        ("radius=5", "⭕ Circle"),
        ("base=6, height=4", "🔺 Triangle"),
        
        ("Thank you", "🙏 Politeness"),
        ("Goodbye", "👋 Farewell")
    ]
    
    for i, (user_input, description) in enumerate(demo_cases, 1):
        print(f"\n{i}. {description}")
        print(f"   👤 User: {user_input}")
        try:
            response = get_response(user_input)
            print(f"   🤖 Bot:  {response}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        print("-" * 50)
    
    print(f"\n✅ Fixed demo completed!")

if __name__ == "__main__":
    demo_final()
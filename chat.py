import random
import json
import re

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from pdf_utils import extract_text_from_pdf, detect_pdf_path_in_message
from math_utils import (
    process_pdf_with_math, 
    parse_user_math_input, 
    calculate_math_expression,
    translate_indonesian_to_english,
    MathExpressionEvaluator
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    # FIRST: Check for direct patterns that don't need NLU
    if is_variable_assignment(msg):
        return handle_math_calculation(msg)
    
    if is_pdf_extraction(msg):
        return handle_pdf_extraction(msg)
    
    if is_pdf_math_processing(msg):
        return handle_pdf_math_processing(msg)
    
    if is_calculation_request(msg):
        return handle_math_calculation(msg)
    
    # THEN: Use NLU for general conversation
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    # Lowered threshold for better recognition
    if prob.item() > 0.5:  # Changed from 0.75 to 0.5
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # Special handling for different types of requests
                if tag == "pdf_extract":
                    return handle_pdf_extraction(msg)
                elif tag == "pdf_math":
                    return handle_pdf_math_processing(msg)
                elif tag == "math_calculate":
                    return handle_math_calculation(msg)
                return random.choice(intent['responses'])
    
    return "I do not understand..."

def is_variable_assignment(message):
    """Check if message contains variable assignments like 'length=10, width=5'"""
    pattern = r'\w+\s*=\s*\d+(?:\.\d+)?'
    return bool(re.search(pattern, message.lower()))

def is_pdf_extraction(message):
    """Check if message is requesting PDF extraction"""
    keywords = ['extract pdf', 'read pdf', 'pdf extract', 'get text from pdf']
    return any(keyword in message.lower() for keyword in keywords)

def is_pdf_math_processing(message):
    """Check if message is requesting PDF math processing"""
    keywords = ['process pdf with math', 'pdf math', 'analyze math pdf']
    return any(keyword in message.lower() for keyword in keywords)

def is_calculation_request(message):
    """Check if message is requesting calculation"""
    keywords = ['calculate', 'compute', 'solve', 'what is', 'how much is']
    return any(keyword in message.lower() for keyword in keywords)

def handle_pdf_extraction(message):
    """
    Handle PDF extraction requests
    """
    # Try to detect PDF path in the message
    pdf_path = detect_pdf_path_in_message(message)
    
    if pdf_path:
        # User provided a path, try to extract
        result = extract_text_from_pdf(pdf_path)
        return result
    else:
        # No path provided, ask for it
        return "I can help you extract text from PDF files! Please provide the PDF file path. For example: 'extract pdf C:\\Documents\\myfile.pdf'"

def handle_math_calculation(message):
    """
    Enhanced mathematical calculation with complex expressions support
    """
    try:
        math_input = parse_user_math_input(message)
        
        if math_input:
            if math_input['type'] == 'simple_calculation':
                num1 = math_input['num1']
                num2 = math_input['num2']
                operator_sym = math_input['operator']
                
                if operator_sym == '+':
                    result = num1 + num2
                elif operator_sym == '-':
                    result = num1 - num2
                elif operator_sym == '*':
                    result = num1 * num2
                elif operator_sym == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return "❌ Error: Division by zero!"
                elif operator_sym == '**':
                    result = num1 ** num2
                else:
                    return "❌ Unsupported operation. Use +, -, *, /, or **"
                
                return f"🧮 **Calculation Result:** {num1} {operator_sym} {num2} = {result:.4f}"
            
            elif math_input['type'] == 'complex_calculation':
                expression = math_input['expression']
                try:
                    result = MathExpressionEvaluator.eval_expression(expression)
                    if isinstance(result, (int, float)):
                        return f"🧮 **Complex Calculation:** {expression} = {result:.4f}"
                    else:
                        return f"❌ {result}"
                except Exception as e:
                    return f"❌ Error evaluating expression: {str(e)}"
            
            elif math_input['type'] == 'variable_assignment':
                variables = math_input['variables']
                
                # Enhanced geometric calculations
                if 'length' in variables and 'width' in variables:
                    area = variables['length'] * variables['width']
                    perimeter = 2 * (variables['length'] + variables['width'])
                    return (f"📐 **Rectangle Calculations:**\n"
                           f"• Length = {variables['length']}\n"
                           f"• Width = {variables['width']}\n"
                           f"• Area = {area:.4f}\n"
                           f"• Perimeter = {perimeter:.4f}")
                
                elif 'side' in variables:
                    area = variables['side'] ** 2
                    perimeter = 4 * variables['side']
                    return (f"🔲 **Square Calculations:**\n"
                           f"• Side = {variables['side']}\n"
                           f"• Area = {area:.4f}\n"
                           f"• Perimeter = {perimeter:.4f}")
                
                elif 'radius' in variables:
                    import math
                    area = math.pi * (variables['radius'] ** 2)
                    circumference = 2 * math.pi * variables['radius']
                    return (f"⭕ **Circle Calculations:**\n"
                           f"• Radius = {variables['radius']}\n"
                           f"• Area = π × {variables['radius']}² = {area:.4f}\n"
                           f"• Circumference = 2π × {variables['radius']} = {circumference:.4f}")
                
                elif 'base' in variables and 'height' in variables:
                    area = 0.5 * variables['base'] * variables['height']
                    return (f"🔺 **Triangle Area:**\n"
                           f"• Base = {variables['base']}\n"
                           f"• Height = {variables['height']}\n"
                           f"• Area = ½ × {variables['base']} × {variables['height']} = {area:.4f}")
                
                else:
                    response = f"📊 **Variables received:** {variables}\n\n"
                    response += "💡 **Available calculations:**\n"
                    response += "• Rectangle: length + width\n"
                    response += "• Square: side\n"
                    response += "• Circle: radius\n"
                    response += "• Triangle: base + height\n"
                    return response
        else:
            return ("🔢 **Math Calculator Ready!** Try:\n\n"
                   "**Simple calculations:**\n"
                   "• `calculate 5 + 3`\n"
                   "• `calculate 2 * 4`\n\n"
                   "**Complex expressions:**\n"
                   "• `calculate (2 + 3) * 4`\n"
                   "• `calculate 2**3` (power)\n"
                   "• `calculate sqrt(16)` (square root)\n"
                   "• `calculate (5 + 3)**2`\n\n"
                   "**Geometry:**\n"
                   "• `length=10, width=5`\n"
                   "• `side=4`\n"
                   "• `radius=3`\n"
                   "• `base=6, height=4`")
            
    except Exception as e:
        return f"❌ Math calculation error: {str(e)}"

def handle_pdf_math_processing(message):
    """
    Enhanced PDF math processing with complex formula support
    """
    pdf_path = detect_pdf_path_in_message(message)
    
    if pdf_path:
        try:
            result = process_pdf_with_math(pdf_path)
            
            if isinstance(result, dict):
                response = f"📄 **PDF Math Processing Results:**\n\n"
                response += f"**Original Text:**\n{result['original_text']}\n\n"
                response += f"**Translated Text:**\n{result['translated_text']}\n\n"
                response += f"🔢 **Mathematical Formulas Found:**\n"
                
                for i, formula in enumerate(result['formulas'], 1):
                    formula_type = formula.get('type', 'simple')
                    if formula_type == 'sqrt':
                        response += f"{i}. {formula['formula']} (Square Root)\n"
                    elif formula_type == 'power':
                        response += f"{i}. {formula['formula']} (Power)\n"
                    elif formula_type == 'parentheses':
                        response += f"{i}. {formula['formula']} (Parentheses)\n"
                    elif formula_type == 'parentheses_power':
                        response += f"{i}. {formula['formula']} (Parentheses + Power)\n"
                    else:
                        response += f"{i}. {formula['formula']} (Simple)\n"
                
                if result['formulas']:
                    response += f"\n💡 **You can now calculate using these formulas!**\n"
                    response += f"Examples:\n"
                    response += f"• `calculate (2 + 3) * 4`\n"
                    response += f"• `calculate sqrt(16)`\n"
                    response += f"• `length=10, width=5`\n"
                
                return response
            else:
                return result
        except Exception as e:
            return f"❌ Error processing PDF with math: {str(e)}"
    else:
        return ("📋 Please provide the PDF file path for enhanced math processing.\n"
               "Example: `process PDF with math test.pdf`\n\n"
               "✨ **Enhanced features:**\n"
               "• Parentheses support: (a + b) * c\n"
               "• Power calculations: a**b\n"
               "• Square roots: sqrt(x)\n"
               "• Complex expressions")


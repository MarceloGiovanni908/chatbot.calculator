from googletrans import Translator
import re
import math
import ast
import operator

# Initialize translator
translator = Translator()

def clean_pdf_extracted_text(text):
    """
    Enhanced cleaning yang mempertahankan line breaks dan format
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Pertama, pisahkan berdasarkan formula patterns untuk mempertahankan struktur
    lines = []
    
    # Split berdasarkan pattern formula (kapital = ...)
    formula_pattern = r'([A-Z][a-zA-Z\s]*\s*=\s*[^=]+?)(?=[A-Z][a-zA-Z\s]*\s*=|$)'
    matches = re.findall(formula_pattern, text)
    
    if matches:
        lines = [match.strip() for match in matches]
    else:
        # Fallback: split by common patterns
        # Try to identify where one formula ends and another begins
        temp_text = text
        # Add line breaks before capital letters that start new formulas
        temp_text = re.sub(r'([a-z])\s*([A-Z][a-z]+\s*=)', r'\1\n\2', temp_text)
        lines = [line.strip() for line in temp_text.split('\n') if line.strip()]
    
    cleaned_lines = []
    for line in lines:
        # Clean each line individually
        cleaned_line = clean_single_line(line)
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    
    return '\n'.join(cleaned_lines)

def clean_single_line(line):
    """
    Clean individual line while preserving mathematical structure
    """
    # Normalize spacing around operators
    line = re.sub(r'\s*=\s*', ' = ', line)
    line = re.sub(r'\s*\*\*\s*', '**', line)
    line = re.sub(r'\s*\*\s*', ' * ', line)
    line = re.sub(r'\s*/\s*', ' / ', line)
    line = re.sub(r'\s*\+\s*', ' + ', line)
    line = re.sub(r'\s*-\s*', ' - ', line)
    
    # Fix parentheses spacing
    line = re.sub(r'\s*\(\s*', '(', line)
    line = re.sub(r'\s*\)\s*', ')', line)
    
    # Handle mathematical symbols
    line = re.sub(r'𝑥', 'x', line)
    line = re.sub(r'√', 'sqrt', line)
    
    # Fix power notation specifically
    line = re.sub(r'sisi\s*\*\*\s*2', 'sisi**2', line, flags=re.IGNORECASE)
    line = re.sub(r'(\w+)\s*\*\*\s*2', r'\1**2', line)
    
    # Fix broken words
    line = re.sub(r'Pers\s+egi', 'Persegi', line, flags=re.IGNORECASE)
    line = re.sub(r'Segiti\s+ga', 'Segitiga', line, flags=re.IGNORECASE)
    line = re.sub(r'Men\s+cari', 'Mencari', line, flags=re.IGNORECASE)
    
    # Remove excessive whitespace
    line = re.sub(r'\s{2,}', ' ', line)
    
    return line.strip()

def translate_indonesian_to_english(text):
    """
    Enhanced translation yang mempertahankan struktur line-by-line
    """
    try:
        # Clean text first to get proper line structure
        cleaned_text = clean_pdf_extracted_text(text)
        
        # Translate line by line untuk mempertahankan struktur
        lines = cleaned_text.split('\n')
        translated_lines = []
        
        for line in lines:
            if line.strip():
                translated_line = translate_single_line(line)
                translated_lines.append(translated_line)
        
        return '\n'.join(translated_lines)
        
    except Exception as e:
        print(f"Translation error: {e}")
        return clean_pdf_extracted_text(text)

def translate_single_line(line):
    """
    Translate single line dengan preserving mathematical structure
    """
    # Dictionary untuk terminologi matematika Indonesia-Inggris
    math_terms = {
        'persegi panjang': 'rectangle',
        'persegi': 'square',
        'segitiga': 'triangle',
        'lingkaran': 'circle',
        'panjang': 'length',
        'lebar': 'width',
        'sisi': 'side',
        'alas': 'base', 
        'tinggi': 'height',
        'jari-jari': 'radius',
        'mencari akar': 'square root',
        'akar kuadrat': 'square root',
        'akar': 'root',
        'luas': 'area',
        'keliling': 'perimeter'
    }
    
    translated = line.lower()
    
    # Apply term-by-term translation
    for indonesian, english in math_terms.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(indonesian) + r'\b'
        translated = re.sub(pattern, english, translated, flags=re.IGNORECASE)
    
    # Preserve mathematical operators and fix spacing
    translated = re.sub(r'\s*\*\*\s*', '**', translated)
    translated = re.sub(r'\s*\*\s*', ' * ', translated)
    translated = re.sub(r'\s*=\s*', ' = ', translated)
    translated = re.sub(r'\s*/\s*', ' / ', translated)
    translated = re.sub(r'\s*\+\s*', ' + ', translated)
    translated = re.sub(r'\s*-\s*', ' - ', translated)
    
    # Fix parentheses
    translated = re.sub(r'\s*\(\s*', '(', translated)
    translated = re.sub(r'\s*\)\s*', ')', translated)
    
    # Clean up extra spaces
    translated = re.sub(r'\s{2,}', ' ', translated)
    
    return translated.strip()

def extract_math_formulas(text):
    """
    Enhanced formula extraction dengan line-by-line processing
    """
    # Clean and prepare text
    cleaned_text = clean_pdf_extracted_text(text)
    lines = cleaned_text.split('\n')
    
    formulas = []
    
    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line or '=' not in line:
            continue
        
        # Normalize line for processing
        normalized_line = line.lower()
        
        # Apply Indonesian->English mapping for analysis
        term_mappings = {
            'persegi panjang': 'rectangle',
            'persegi': 'square',
            'segitiga': 'triangle',
            'panjang': 'length',
            'lebar': 'width',
            'sisi': 'side',
            'alas': 'base',
            'tinggi': 'height',
            'mencari akar': 'square_root'
        }
        
        processed_line = normalized_line
        for indonesian, english in term_mappings.items():
            processed_line = processed_line.replace(indonesian, english)
        
        # Enhanced pattern matching
        formula = extract_formula_from_line(processed_line, line, line_num)
        if formula:
            formulas.append(formula)
    
    return formulas

def extract_formula_from_line(processed_line, original_line, line_num):
    """
    Extract formula dari single line dengan pattern matching yang lebih baik
    """
    # Pattern untuk berbagai jenis formula
    patterns = [
        # Rectangle: rectangle = length * width
        (r'rectangle\s*=\s*(\w+)\s*\*\s*(\w+)', 'rectangle'),
        
        # Square: square = side**2
        (r'square\s*=\s*(\w+)\s*\*\*\s*2', 'square'),
        
        # Triangle: triangle = (base * height) / 2
        (r'triangle\s*=\s*\(([^)]+)\)\s*/\s*2', 'triangle'),
        
        # Square root: square_root = sqrt(expression)
        (r'square_root\s*=\s*sqrt\(([^)]+)\)', 'sqrt'),
        
        # General pattern: variable = expression
        (r'(\w+)\s*=\s*(.+)', 'general')
    ]
    
    for pattern, formula_type in patterns:
        match = re.search(pattern, processed_line)
        if match:
            if formula_type == 'rectangle':
                var1, var2 = match.groups()
                return {
                    'result': 'rectangle_area',
                    'type': 'rectangle',
                    'variable1': var1,
                    'variable2': var2,
                    'formula': f"rectangle_area = {var1} * {var2}",
                    'original_line': original_line,
                    'line_number': line_num + 1
                }
            
            elif formula_type == 'square':
                var1 = match.group(1)
                return {
                    'result': 'square_area',
                    'type': 'square', 
                    'variable1': var1,
                    'formula': f"square_area = {var1}**2",
                    'original_line': original_line,
                    'line_number': line_num + 1
                }
            
            elif formula_type == 'triangle':
                expression = match.group(1)
                return {
                    'result': 'triangle_area',
                    'type': 'triangle',
                    'expression': expression,
                    'formula': f"triangle_area = ({expression}) / 2",
                    'original_line': original_line,
                    'line_number': line_num + 1
                }
            
            elif formula_type == 'sqrt':
                expression = match.group(1)
                return {
                    'result': 'sqrt_result',
                    'type': 'sqrt',
                    'expression': expression,
                    'formula': f"sqrt_result = sqrt({expression})",
                    'original_line': original_line,
                    'line_number': line_num + 1
                }
            
            elif formula_type == 'general':
                result_var, expression = match.groups()
                return {
                    'result': result_var,
                    'type': 'general',
                    'expression': expression.strip(),
                    'formula': f"{result_var} = {expression.strip()}",
                    'original_line': original_line,
                    'line_number': line_num + 1
                }
    
    return None

class MathExpressionEvaluator:
    """Safe mathematical expression evaluator"""
    
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    @classmethod
    def eval_expression(cls, expr, variables=None):
        if variables is None:
            variables = {}
        
        try:
            expr = re.sub(r'sqrt\(([^)]+)\)', r'(\1)**0.5', expr)
            
            for var, val in variables.items():
                expr = re.sub(r'\b' + re.escape(var) + r'\b', str(val), expr)
            
            node = ast.parse(expr, mode='eval')
            return cls._eval_node(node.body)
        
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
    
    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op = cls.operators.get(type(node.op))
            if op:
                if isinstance(node.op, ast.Div) and right == 0:
                    raise ValueError("Division by zero")
                return op(left, right)
            else:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op = cls.operators.get(type(node.op))
            if op:
                return op(operand)
            else:
                raise ValueError(f"Unsupported unary operator: {type(node.op)}")
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

def parse_user_math_input(message):
    """Parse user input for math operations"""
    var_pattern = r'(\w+)\s*=\s*(\d+(?:\.\d+)?)'
    variables = re.findall(var_pattern, message.lower())
    
    if variables:
        var_dict = {var: float(val) for var, val in variables}
        return {
            'type': 'variable_assignment',
            'variables': var_dict
        }
    
    complex_calc_pattern = r'(?:calculate|compute|solve)\s+(.+)'
    match = re.search(complex_calc_pattern, message.lower())
    
    if match:
        expression = match.group(1).strip()
        if re.match(r'^\d+(?:\.\d+)?\s*[\+\-\*/\*\*]\s*\d+(?:\.\d+)?$', expression):
            simple_match = re.match(r'^(\d+(?:\.\d+)?)\s*([\+\-\*/\*\*])\s*(\d+(?:\.\d+)?)$', expression)
            if simple_match:
                num1, operator_sym, num2 = simple_match.groups()
                return {
                    'type': 'simple_calculation',
                    'num1': float(num1),
                    'operator': operator_sym,
                    'num2': float(num2)
                }
        else:
            return {
                'type': 'complex_calculation',
                'expression': expression
            }
    
    return None

def process_pdf_with_math(file_path):
    """
    Process PDF file dengan enhanced line-by-line processing
    """
    from pdf_utils import extract_text_from_pdf
    
    pdf_text = extract_text_from_pdf(file_path)
    
    if pdf_text.startswith("Error"):
        return pdf_text
    
    # Enhanced processing
    translated_text = translate_indonesian_to_english(pdf_text)
    formulas = extract_math_formulas(pdf_text)
    
    result = {
        'original_text': pdf_text,
        'translated_text': translated_text,
        'formulas': formulas,
        'summary': f"Found {len(formulas)} mathematical formulas with proper line structure."
    }
    
    return result

def calculate_math_expression(formula_dict, values):
    """Calculate simple mathematical expression"""
    try:
        var1 = formula_dict['variable1']
        var2 = formula_dict['variable2'] 
        operator_sym = formula_dict['operator']
        
        if var1 in values and var2 in values:
            val1 = float(values[var1])
            val2 = float(values[var2])
            
            if operator_sym == '+':
                result = val1 + val2
            elif operator_sym == '-':
                result = val1 - val2
            elif operator_sym == '*':
                result = val1 * val2
            elif operator_sym == '/':
                if val2 != 0:
                    result = val1 / val2
                else:
                    return "Error: Division by zero"
            elif operator_sym == '**':
                result = val1 ** val2
            else:
                return f"Error: Unsupported operator {operator_sym}"
                
            return f"{formula_dict['result']} = {val1} {operator_sym} {val2} = {result:.4f}"
        else:
            missing_vars = []
            if var1 not in values:
                missing_vars.append(var1)
            if var2 not in values:
                missing_vars.append(var2)
            return f"Missing values for: {', '.join(missing_vars)}"
            
    except Exception as e:
        return f"Calculation error: {str(e)}"

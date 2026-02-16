"""
Coding Assistant Module
Helps with code analysis, debugging, explanations, and suggestions
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from core.logger import setup_logger

logger = setup_logger("CodingAssistant")


class CodingAssistant:
    """Intelligent coding helper"""
    
    def __init__(self):
        self.language_patterns = self._init_language_patterns()
        self.common_errors = self._init_common_errors()
        self.code_templates = self._init_code_templates()
    
    def _init_language_patterns(self) -> Dict[str, List[str]]:
        """Initialize programming language detection patterns"""
        return {
            "python": [
                r"\bdef\s+\w+\s*\(",
                r"\bimport\s+\w+",
                r"\bprint\s*\(",
                r"\bif\s+.+:",
                r"\.py\b",
            ],
            "javascript": [
                r"\bfunction\s+\w+\s*\(",
                r"\bconst\s+\w+",
                r"\blet\s+\w+",
                r"\bconsole\.log\s*\(",
                r"\.js\b",
            ],
            "java": [
                r"\bpublic\s+class\s+\w+",
                r"\bprivate\s+\w+",
                r"\bSystem\.out\.println",
                r"\.java\b",
            ],
            "cpp": [
                r"#include\s*<",
                r"\bstd::",
                r"\bcout\s*<<",
                r"\.cpp\b",
            ],
            "c": [
                r"#include\s*<",
                r"\bprintf\s*\(",
                r"\.c\b",
            ],
        }
    
    def _init_common_errors(self) -> Dict[str, Dict]:
        """Initialize common programming errors and solutions"""
        return {
            "python": {
                "IndentationError": "Check your indentation. Python requires consistent spacing (use 4 spaces).",
                "NameError": "Variable not defined. Make sure you've declared the variable before using it.",
                "TypeError": "Wrong data type operation. Check if you're using the right types together.",
                "SyntaxError": "Code syntax is incorrect. Check for missing colons, parentheses, or quotes.",
                "IndexError": "List index out of range. Check your list boundaries.",
                "KeyError": "Dictionary key doesn't exist. Use .get() method or check if key exists.",
            },
            "javascript": {
                "ReferenceError": "Variable is not defined. Declare it with let, const, or var.",
                "TypeError": "Cannot read property of undefined. Check if object/variable exists first.",
                "SyntaxError": "Syntax error. Check for missing semicolons, brackets, or parentheses.",
            },
            "general": {
                "logic_error": "Code runs but gives wrong results. Review your algorithm step by step.",
                "infinite_loop": "Program hangs. Check your loop conditions and ensure they can exit.",
                "null_pointer": "Trying to access null/undefined. Always check if object exists first.",
            }
        }
    
    def _init_code_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize code templates for common tasks"""
        return {
            "python": {
                "function": "def function_name(parameters):\n    \"\"\"Docstring describing the function\"\"\"\n    # Your code here\n    return result",
                "class": "class ClassName:\n    def __init__(self, parameters):\n        self.attribute = parameters\n    \n    def method(self):\n        # Your code here\n        pass",
                "file_read": "with open('filename.txt', 'r') as file:\n    content = file.read()\n    # Process content",
                "try_except": "try:\n    # Code that might raise an exception\n    pass\nexcept Exception as e:\n    print(f'Error: {e}')",
                "list_comprehension": "[expression for item in iterable if condition]",
                "dictionary": "my_dict = {'key1': 'value1', 'key2': 'value2'}",
            },
            "javascript": {
                "function": "function functionName(parameters) {\n    // Your code here\n    return result;\n}",
                "arrow_function": "const functionName = (parameters) => {\n    // Your code here\n    return result;\n}",
                "promise": "const myPromise = new Promise((resolve, reject) => {\n    // Async operation\n    if (success) {\n        resolve(result);\n    } else {\n        reject(error);\n    }\n});",
                "async_await": "async function fetchData() {\n    try {\n        const response = await fetch(url);\n        const data = await response.json();\n        return data;\n    } catch (error) {\n        console.error('Error:', error);\n    }\n}",
            },
            "java": {
                "class": "public class ClassName {\n    private int attribute;\n    \n    public ClassName(int attribute) {\n        this.attribute = attribute;\n    }\n    \n    public void method() {\n        // Your code here\n    }\n}",
                "main": "public static void main(String[] args) {\n    // Your code here\n}",
            },
            "cpp": {
                "function": "returnType functionName(parameters) {\n    // Your code here\n    return result;\n}",
                "class": "class ClassName {\nprivate:\n    int attribute;\npublic:\n    ClassName(int attr) : attribute(attr) {}\n    void method() {\n        // Your code here\n    }\n};",
            }
        }
    
    def detect_language(self, code: str) -> Optional[str]:
        """Detect programming language from code snippet"""
        code_lower = code.lower()
        
        language_scores = {}
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for pattern in patterns if re.search(pattern, code, re.IGNORECASE))
            if score > 0:
                language_scores[lang] = score
        
        if language_scores:
            detected_lang = max(language_scores, key=language_scores.get)
            logger.info(f"Detected language: {detected_lang}")
            return detected_lang
        
        return None
    
    def explain_code(self, code: str) -> str:
        """Explain what a code snippet does"""
        lang = self.detect_language(code)
        
        explanation_parts = []
        
        if lang:
            explanation_parts.append(f"This appears to be {lang.upper()} code.")
        
        # Analyze code structure
        if "def " in code or "function " in code:
            explanation_parts.append("• Defines a function")
        
        if "class " in code:
            explanation_parts.append("• Defines a class")
        
        if "for " in code or "while " in code:
            explanation_parts.append("• Contains a loop")
        
        if "if " in code:
            explanation_parts.append("• Has conditional logic (if statements)")
        
        if "import " in code or "include" in code:
            explanation_parts.append("• Imports external libraries/modules")
        
        if "return " in code:
            explanation_parts.append("• Returns a value")
        
        # Look for common operations
        if re.search(r"(print|console\.log|cout)", code, re.IGNORECASE):
            explanation_parts.append("• Outputs/prints data")
        
        if re.search(r"(read|open|file)", code, re.IGNORECASE):
            explanation_parts.append("• Reads from a file")
        
        if re.search(r"(write|save)", code, re.IGNORECASE):
            explanation_parts.append("• Writes to a file")
        
        if explanation_parts:
            return "\n".join(explanation_parts)
        else:
            return "I can see this is code, but I need more context to explain it fully. Can you provide more details about what it should do?"
    
    def suggest_improvements(self, code: str, lang: Optional[str] = None) -> List[str]:
        """Suggest code improvements"""
        if not lang:
            lang = self.detect_language(code)
        
        suggestions = []
        
        # Python-specific suggestions
        if lang == "python":
            if not re.search(r'""".*?"""', code) and "def " in code:
                suggestions.append("Add docstrings to your functions for better documentation")
            
            if "except:" in code:
                suggestions.append("Avoid bare except clauses. Specify the exception type: except ValueError:")
            
            if re.search(r'\bprint\s*\(', code):
                suggestions.append("Consider using logging instead of print for production code")
            
            if not re.search(r'if __name__ == ["\']__main__["\']:', code) and len(code) > 200:
                suggestions.append("Add if __name__ == '__main__': guard for script execution")
        
        # JavaScript-specific
        if lang == "javascript":
            if "var " in code:
                suggestions.append("Use 'const' or 'let' instead of 'var' for better scoping")
            
            if "==" in code:
                suggestions.append("Use '===' for strict equality comparison")
        
        # General suggestions
        if len(code.split('\n')) > 50:
            suggestions.append("Consider breaking this into smaller functions for better readability")
        
        if not re.search(r'#.*|//.*|/\*.*\*/', code):
            suggestions.append("Add comments to explain complex logic")
        
        return suggestions if suggestions else ["Code looks good! Keep it clean and readable."]
    
    def debug_help(self, error_message: str, code: Optional[str] = None) -> str:
        """Help debug an error"""
        error_lower = error_message.lower()
        
        # Identify error type
        for lang, errors in self.common_errors.items():
            for error_type, solution in errors.items():
                if error_type.lower() in error_lower:
                    response = f"**{error_type}**\n\n{solution}"
                    
                    if code:
                        lang_detected = self.detect_language(code)
                        if lang_detected:
                            response += f"\n\nDetected language: {lang_detected.upper()}"
                    
                    return response
        
        # General debugging advice
        return """**Debugging Tips:**

1. **Read the error message carefully** - It usually tells you what went wrong and where
2. **Check the line number** - The error location is your starting point
3. **Print/log variables** - See what values they have at different points
4. **Use a debugger** - Step through code line by line
5. **Google the error** - Others have likely faced the same issue
6. **Rubber duck debugging** - Explain your code line by line to find the issue

Share the error message and relevant code, and I'll help you figure it out!"""
    
    def get_template(self, template_name: str, lang: str) -> Optional[str]:
        """Get a code template"""
        lang_lower = lang.lower()
        
        if lang_lower in self.code_templates:
            template = self.code_templates[lang_lower].get(template_name)
            if template:
                return f"```{lang_lower}\n{template}\n```"
        
        return None
    
    def list_templates(self, lang: Optional[str] = None) -> str:
        """List available templates"""
        if lang and lang.lower() in self.code_templates:
            templates = self.code_templates[lang.lower()].keys()
            return f"Available {lang.upper()} templates:\n" + "\n".join(f"• {t}" for t in templates)
        else:
            result = "**Available Templates by Language:**\n\n"
            for language, templates in self.code_templates.items():
                result += f"**{language.upper()}:** {', '.join(templates.keys())}\n"
            return result
    
    def analyze_complexity(self, code: str) -> str:
        """Analyze code complexity"""
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        num_lines = len(lines)
        num_loops = len(re.findall(r'\b(for|while)\b', code))
        num_conditionals = len(re.findall(r'\bif\b', code))
        num_functions = len(re.findall(r'\b(def|function)\b', code))
        
        analysis = f"""**Code Complexity Analysis:**

• Lines of code: {num_lines}
• Functions: {num_functions}
• Loops: {num_loops}
• Conditionals: {num_conditionals}
"""
        
        # Complexity assessment
        if num_loops > 3:
            analysis += "\n⚠️ High loop count - consider optimizing"
        if num_conditionals > 5:
            analysis += "\n⚠️ Many conditionals - consider refactoring to reduce complexity"
        if num_lines > 100:
            analysis += "\n⚠️ Long code - consider breaking into smaller functions"
        
        if num_loops <= 3 and num_conditionals <= 5 and num_lines <= 100:
            analysis += "\n✓ Complexity looks reasonable"
        
        return analysis
    
    def generate_explanation(self, concept: str) -> Optional[str]:
        """Explain programming concepts"""
        concept_lower = concept.lower()
        
        concepts = {
            "variable": "A **variable** is a named container that stores a value. Think of it as a labeled box where you can put data. Example: `x = 5` creates a variable 'x' and stores the value 5 in it.",
            
            "function": "A **function** is a reusable block of code that performs a specific task. It can take inputs (parameters) and return outputs. Functions help organize code and avoid repetition.",
            
            "loop": "A **loop** repeats a block of code multiple times. Common types:\n• **for loop**: Iterate a specific number of times\n• **while loop**: Repeat while a condition is true",
            
            "array": "An **array** (or list) is an ordered collection of items. Each item has an index (position). Example: `[1, 2, 3, 4]` - you can access items by their position.",
            
            "object": "An **object** stores data as key-value pairs. It's like a dictionary where each piece of data has a name (key). Example: `{name: 'John', age: 30}`",
            
            "recursion": "**Recursion** is when a function calls itself. Useful for problems that can be broken into smaller similar problems. Must have a base case to stop!",
            
            "algorithm": "An **algorithm** is a step-by-step procedure to solve a problem. Like a recipe - you follow specific steps to get the desired result.",
            
            "api": "An **API** (Application Programming Interface) is a way for programs to communicate with each other. It defines what requests you can make and what responses you'll get.",
            
            "class": "A **class** is a blueprint for creating objects. It defines properties (attributes) and behaviors (methods) that objects of that type will have.",
            
            "async": "**Asynchronous** programming allows code to run without blocking. Operations happen in the background while other code continues executing. Essential for handling I/O operations efficiently.",
        }
        
        for key, explanation in concepts.items():
            if key in concept_lower:
                return explanation
        
        return None

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
            "typescript": [
                r"\binterface\s+\w+",
                r":\s*(string|number|boolean)",
                r"\btype\s+\w+\s*=",
                r"\.ts\b",
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
            "csharp": [
                r"\busing\s+System",
                r"\bnamespace\s+\w+",
                r"\bConsole\.WriteLine",
                r"\.cs\b",
            ],
            "go": [
                r"\bpackage\s+\w+",
                r"\bfunc\s+\w+\s*\(",
                r"\bfmt\.Print",
                r"\.go\b",
            ],
            "rust": [
                r"\bfn\s+\w+\s*\(",
                r"\blet\s+mut\s+",
                r"println!\s*\(",
                r"\.rs\b",
            ],
            "php": [
                r"<\?php",
                r"\$\w+\s*=",
                r"\becho\s+",
                r"\.php\b",
            ],
            "ruby": [
                r"\bdef\s+\w+",
                r"\bputs\s+",
                r"\bend\b",
                r"\.rb\b",
            ],
            "swift": [
                r"\bfunc\s+\w+\s*\(",
                r"\bvar\s+\w+",
                r"\bprint\s*\(",
                r"\.swift\b",
            ],
            "kotlin": [
                r"\bfun\s+\w+\s*\(",
                r"\bval\s+\w+",
                r"\.kt\b",
            ],
            "sql": [
                r"\bSELECT\s+",
                r"\bFROM\s+\w+",
                r"\bWHERE\s+",
                r"\.sql\b",
            ],
            "html": [
                r"<html>",
                r"<div",
                r"<body>",
                r"\.html\b",
            ],
            "css": [
                r"\.\w+\s*{",
                r"#\w+\s*{",
                r"color\s*:",
                r"\.css\b",
            ],
        }
    
    def _init_common_errors(self) -> Dict[str, Dict]:
        """Initialize common programming errors and solutions"""
        return {
            "python": {
                "IndentationError": "Check your indentation. Python requires consistent spacing (use 4 spaces or tabs, but not both).",
                "NameError": "Variable not defined. Make sure you've declared the variable before using it.",
                "TypeError": "Wrong data type operation. Check if you're using compatible types (e.g., can't add string + integer).",
                "SyntaxError": "Code syntax is incorrect. Check for missing colons, parentheses, quotes, or incorrect operators.",
                "IndexError": "List index out of range. Check your list boundaries. Use len() to verify list size.",
                "KeyError": "Dictionary key doesn't exist. Use .get() method or 'in' operator to check if key exists first.",
                "AttributeError": "Object doesn't have that attribute/method. Check spelling and object type.",
                "ValueError": "Correct type but inappropriate value. Example: int('abc') fails because 'abc' isn't a number.",
                "ImportError": "Module not found. Install it with pip or check the module name spelling.",
                "ZeroDivisionError": "Cannot divide by zero. Add a check: if divisor != 0 before dividing.",
                "FileNotFoundError": "File doesn't exist. Check the file path and name are correct.",
                "ModuleNotFoundError": "Python module not installed. Run: pip install <module-name>",
            },
            "javascript": {
                "ReferenceError": "Variable is not defined. Declare it with let, const, or var before using.",
                "TypeError": "Cannot read property of undefined/null. Always check if object exists: if (obj) { ... }",
                "SyntaxError": "Syntax error. Check for missing semicolons, brackets, parentheses, or quotes.",
                "RangeError": "Invalid array length or number out of range. Check array operations and number values.",
                "URIError": "URI encoding/decoding error. Check special characters in URLs.",
                "Promise rejection": "Unhandled promise rejection. Use .catch() or try-catch with async/await.",
                "Uncaught": "Error not caught. Wrap code in try-catch block to handle errors gracefully.",
            },
            "typescript": {
                "Type error": "Type mismatch. Check your type annotations match the actual values.",
                "Cannot find name": "Variable/type not declared. Import it or declare before use.",
                "Property does not exist": "Accessing undefined property. Check interface/type definitions.",
            },
            "java": {
                "NullPointerException": "Trying to use null object. Always check: if (obj != null) before accessing.",
                "ArrayIndexOutOfBoundsException": "Array index invalid. Check: index < array.length",
                "ClassNotFoundException": "Class not found in classpath. Verify imports and dependencies.",
                "NumberFormatException": "Cannot parse string to number. Validate input before parsing.",
                "ConcurrentModificationException": "Modifying collection while iterating. Use Iterator.remove() or CopyOnWriteArrayList.",
                "StackOverflowError": "Infinite recursion. Ensure recursion has a proper base case.",
            },
            "cpp": {
                "segmentation fault": "Invalid memory access. Check: null pointers, array bounds, deleted objects.",
                "undefined reference": "Function/variable not found by linker. Check spelling and linking.",
                "no matching function": "Function signature doesn't match. Check parameter types and count.",
                "invalid conversion": "Type conversion not allowed. Use explicit cast or convert type properly.",
                "expected ; before": "Missing semicolon. Add ; at the end of the statement.",
            },
            "c": {
                "segmentation fault": "Invalid memory access. Check pointers, array bounds, and memory allocation.",
                "undefined reference": "Symbol not found during linking. Check function declarations and definitions.",
                "implicit declaration": "Function used before declaration. Add prototype or include header file.",
                "format specifies type": "printf format mismatch. Use correct format specifier (%d, %s, %f, etc.).",
            },
            "csharp": {
                "NullReferenceException": "Object is null. Check with: if (obj != null) or use ?. null-conditional operator.",
                "IndexOutOfRangeException": "Array/list index out of bounds. Verify: index < collection.Count",
                "DivideByZeroException": "Division by zero. Add check: if (divisor != 0) before dividing.",
                "FormatException": "String format invalid. Validate input before parsing: int.TryParse().",
            },
            "go": {
                "panic": "Runtime panic. Use defer recover() to handle panics gracefully.",
                "nil pointer": "Nil pointer dereference. Check: if ptr != nil before accessing.",
                "index out of range": "Slice/array index invalid. Verify: index < len(slice)",
                "deadlock": "All goroutines deadlocked. Check channel operations and synchronization.",
            },
            "rust": {
                "borrow checker": "Ownership/borrowing rules violated. Review Rust ownership model - only one mutable reference.",
                "cannot move": "Value moved and reused. Either clone value or use references (&).",
                "expected type": "Type mismatch. Rust requires exact type matching - check return types.",
                "lifetime": "Lifetime annotation error. Ensure borrowed references are valid for required scope.",
            },
            "php": {
                "Parse error": "Syntax error. Check for missing semicolons, brackets, or quotes.",
                "Fatal error": "Fatal error occurred. Check error message for specific cause.",
                "Undefined variable": "Variable not initialized. Define variable before using: $var = value;",
                "Call to undefined function": "Function doesn't exist. Check spelling and include required files.",
            },
            "sql": {
                "syntax error": "SQL syntax incorrect. Check keywords, commas, and query structure.",
                "column not found": "Column name doesn't exist. Verify column names in table schema.",
                "foreign key constraint": "Cannot insert/update due to foreign key. Check referenced table has the key.",
                "duplicate entry": "Unique constraint violated. Value already exists in unique/primary key column.",
            },
            "general": {
                "logic error": "Code runs but gives wrong results. Debug by: 1) Print intermediate values, 2) Review algorithm step-by-step, 3) Test with simple inputs.",
                "infinite loop": "Program hangs. Check: 1) Loop condition eventually becomes false, 2) Counter increments/decrements properly, 3) Break conditions are reachable.",
                "memory leak": "Memory usage grows. Ensure: 1) Free allocated memory, 2) Close file handles, 3) Unsubscribe from events.",
                "race condition": "Inconsistent results with concurrent execution. Use: 1) Locks/mutexes, 2) Atomic operations, 3) Proper synchronization.",
                "stack overflow": "Too much recursion or large local variables. Solutions: 1) Add base case to recursion, 2) Use iteration instead, 3) Reduce local variable size.",
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
        """Help debug an error with comprehensive analysis"""
        error_lower = error_message.lower()
        
        # Detect language from code if provided
        detected_lang = None
        if code:
            detected_lang = self.detect_language(code)
        
        # Search for matching error patterns
        matched_errors = []
        
        # Check language-specific errors first
        for lang, errors in self.common_errors.items():
            if lang == "general":
                continue
            for error_type, solution in errors.items():
                if error_type.lower() in error_lower or any(word in error_lower for word in error_type.lower().split()):
                    matched_errors.append((lang, error_type, solution))
        
        # If no specific match, check general errors
        if not matched_errors:
            for error_type, solution in self.common_errors.get("general", {}).items():
                if error_type.lower().replace("_", " ") in error_lower:
                    matched_errors.append(("general", error_type, solution))
        
        # Build comprehensive response
        if matched_errors:
            response = "## 🐛 Debug Analysis\n\n"
            
            for lang, error_type, solution in matched_errors[:3]:  # Top 3 matches
                response += f"### **{error_type}**"
                if lang != "general" and lang != detected_lang:
                    response += f" ({lang.upper()})"
                response += "\n\n"
                response += f"**Solution:** {solution}\n\n"
            
            # Add code-specific analysis
            if code:
                response += "### 📝 Code Analysis:\n"
                if detected_lang:
                    response += f"- Detected language: **{detected_lang.upper()}**\n"
                
                # Analyze common issues in code
                code_issues = self._analyze_code_issues(code, error_lower)
                if code_issues:
                    response += "\n**Potential Issues Found:**\n"
                    for issue in code_issues:
                        response += f"- {issue}\n"
            
            # Add debugging steps
            response += "\n### 🔍 Debugging Steps:\n"
            response += "1. **Locate the error** - Check line number in error message\n"
            response += "2. **Understand the context** - What were you trying to do?\n"
            response += "3. **Verify assumptions** - Print/log variable values\n"
            response += "4. **Test hypothesis** - Make one change at a time\n"
            response += "5. **Search documentation** - Check language docs for the feature\n"
            
            return response
        
        # No specific error found - provide general debugging guidance
        return self._general_debug_guidance(error_message, code, detected_lang)
    
    def _analyze_code_issues(self, code: str, error_msg: str) -> List[str]:
        """Analyze code for common issues"""
        issues = []
        
        # Check for common patterns
        if "undefined" in error_msg or "not defined" in error_msg:
            # Look for variables that might not be defined
            variables_used = re.findall(r'\b[a-z_]\w*\b', code)
            if variables_used:
                issues.append(f"Check if variables are defined before use: {', '.join(set(variables_used[:5]))}")
        
        if "null" in error_msg or "none" in error_msg:
            # Check for null/None access
            if re.search(r'\.\w+\(', code):
                issues.append("Verify objects are not null/None before calling methods")
        
        if "index" in error_msg or "bounds" in error_msg:
            # Check array/list access
            array_accesses = re.findall(r'\w+\[\s*\d+\s*\]', code)
            if array_accesses:
                issues.append(f"Check array bounds for: {', '.join(set(array_accesses[:3]))}")
        
        if "syntax" in error_msg:
            # Check for missing brackets/parentheses
            open_parens = code.count('(')
            close_parens = code.count(')')
            if open_parens != close_parens:
                issues.append(f"Unbalanced parentheses: {open_parens} open, {close_parens} close")
            
            open_brackets = code.count('[')
            close_brackets = code.count(']')
            if open_brackets != close_brackets:
                issues.append(f"Unbalanced brackets: {open_brackets} open, {close_brackets} close")
            
            open_braces = code.count('{')
            close_braces = code.count('}')
            if open_braces != close_braces:
                issues.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")
        
        if "type" in error_msg:
            # Check for type mismatches
            if re.search(r'\d+\s*\+\s*["\']', code) or re.search(r'["\']​\s*\+\s*\d+', code):
                issues.append("Mixing strings and numbers - use str() or int() to convert")
        
        return issues
    
    def _general_debug_guidance(self, error_msg: str, code: Optional[str], lang: Optional[str]) -> str:
        """Provide general debugging guidance"""
        response = "## 🔍 Debugging Assistance\n\n"
        
        if lang:
            response += f"**Detected Language:** {lang.upper()}\n\n"
        
        response += f"**Error Message:**\n```\n{error_msg}\n```\n\n"
        
        response += "### Common Debugging Strategies:\n\n"
        response += "**1. Read the Error Carefully**\n"
        response += "- Error messages tell you WHAT went wrong and WHERE\n"
        response += "- Look for: error type, line number, and description\n\n"
        
        response += "**2. Isolate the Problem**\n"
        response += "- Comment out code sections to find where it breaks\n"
        response += "- Add print statements to track execution flow\n"
        response += "- Test with simple input first\n\n"
        
        response += "**3. Check Common Issues**\n"
        response += "- Typos in variable/function names\n"
        response += "- Missing or extra punctuation (;, }, ), ])\n"
        response += "- Wrong indentation (Python)\n"
        response += "- Null/undefined objects\n"
        response += "- Array index out of bounds\n"
        response += "- Type mismatches\n\n"
        
        response += "**4. Use Debugging Tools**\n"
        if lang == "python":
            response += "- Use `pdb` debugger: `import pdb; pdb.set_trace()`\n"
            response += "- Add print statements: `print(f'variable = {variable}')`\n"
        elif lang == "javascript":
            response += "- Use browser DevTools (F12)\n"
            response += "- Add console.log: `console.log('variable:', variable)`\n"
            response += "- Use debugger statement: `debugger;`\n"
        elif lang == "java":
            response += "- Use IDE debugger (Eclipse, IntelliJ)\n"
            response += "- Add System.out.println for debugging\n"
        else:
            response += "- Use your IDE's debugger\n"
            response += "- Add logging/print statements\n"
        
        response += "\n**5. Search for Solutions**\n"
        response += "- Google the exact error message\n"
        response += "- Check Stack Overflow\n"
        response += "- Read official documentation\n"
        response += "- Ask in programming communities\n\n"
        
        response += "💡 **Tip:** Share the complete error message and relevant code for more specific help!"
        
        return response
    
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
            
            "list": "A **list** (or array) is an ordered, mutable collection of items. You can add, remove, or modify elements. Example: `[1, 2, 3]` - very flexible data structure!",
            
            "object": "An **object** stores data as key-value pairs. It's like a dictionary where each piece of data has a name (key). Example: `{name: 'John', age: 30}`",
            
            "recursion": "**Recursion** is when a function calls itself. Useful for problems that can be broken into smaller similar problems. Must have a base case to stop!",
            
            "algorithm": "An **algorithm** is a step-by-step procedure to solve a problem. Like a recipe - you follow specific steps to get the desired result.",
            
            "api": "An **API** (Application Programming Interface) is a way for programs to communicate with each other. It defines what requests you can make and what responses you'll get.",
            
            "class": "A **class** is a blueprint for creating objects. It defines properties (attributes) and behaviors (methods) that objects of that type will have.",
            
            "async": "**Asynchronous** programming allows code to run without blocking. Operations happen in the background while other code continues executing. Essential for handling I/O operations efficiently.",
            
            "dynamic programming": "**Dynamic Programming (DP)** is an optimization technique that solves complex problems by breaking them into simpler subproblems. Key principles:\n\n• **Memoization**: Store results of expensive function calls\n• **Optimal substructure**: Optimal solution contains optimal solutions to subproblems\n• **Overlapping subproblems**: Same subproblems are solved multiple times\n\nCommon examples: Fibonacci sequence, knapsack problem, shortest path algorithms.",
            
            "oop": "**Object-Oriented Programming (OOP)** organizes code around objects rather than functions. Core principles:\n• **Encapsulation**: Bundle data and methods\n• **Inheritance**: Create new classes from existing ones\n• **Polymorphism**: Objects of different types respond to the same method\n• **Abstraction**: Hide complex implementation details",
            
            "inheritance": "**Inheritance** lets a class (child) inherit properties and methods from another class (parent). It promotes code reuse - child classes get all parent functionality and can add their own.",
            
            "polymorphism": "**Polymorphism** means 'many forms' - different classes can be treated the same way through a common interface. Example: Different shapes (circle, square) all have a `draw()` method.",
            
            "encapsulation": "**Encapsulation** bundles data and the methods that operate on that data into a single unit (class). It hides internal details and protects data from unauthorized access.",
            
            "abstraction": "**Abstraction** hides complex implementation details and shows only essential features. Like driving a car - you use the steering wheel without knowing how the engine works!",
            
            "data structure": "A **data structure** organizes and stores data efficiently. Different structures serve different purposes:\n• Arrays: Sequential access\n• Linked Lists: Dynamic size\n• Trees: Hierarchical data\n• Hash Tables: Fast lookups",
            
            "stack": "A **stack** is a Last-In-First-Out (LIFO) data structure. Like a stack of plates - you add/remove from the top. Operations: push (add), pop (remove), peek (view top).",
            
            "queue": "A **queue** is a First-In-First-Out (FIFO) data structure. Like a line at a store - first person in is first served. Operations: enqueue (add), dequeue (remove).",
            
            "linked list": "A **linked list** is a sequence of nodes where each node contains data and a reference to the next node. Unlike arrays, elements aren't stored contiguously in memory.",
            
            "tree": "A **tree** is a hierarchical data structure with a root node and child nodes. Each node can have multiple children. Common types: Binary Tree, BST, AVL Tree, Red-Black Tree.",
            
            "graph": "A **graph** consists of vertices (nodes) connected by edges. Used to represent networks, relationships, maps. Types: Directed/Undirected, Weighted/Unweighted.",
            
            "hash table": "A **hash table** (or hash map) stores key-value pairs using a hash function. Provides O(1) average time for lookups, inserts, and deletes. Very efficient!",
            
            "big o": "**Big O notation** describes algorithm efficiency - how runtime/memory grows with input size:\n• O(1): Constant\n• O(log n): Logarithmic\n• O(n): Linear\n• O(n²): Quadratic\n• O(2ⁿ): Exponential",
            
            "time complexity": "**Time complexity** measures how an algorithm's runtime grows with input size. Expressed in Big O notation. Lower is better: O(1) < O(log n) < O(n) < O(n²) < O(2ⁿ).",
            
            "space complexity": "**Space complexity** measures how much memory an algorithm uses relative to input size. Important for large datasets. Trade-off: Sometimes using more space makes algorithms faster.",
        }
        
        for key, explanation in concepts.items():
            if key in concept_lower:
                return explanation
        
        return None

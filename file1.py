# Calculator class with basic and advanced operations
from unicodedata import name


class Calculator:
    def __init__(self):
        self.result = 0
        self.history = []
        self.memory = 0
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        self.result = result
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"SUBTRACTION: {a} - {b} = {result}")
        self.result = result
        print(f"substracting {b} from {a} gives {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        self.result = result
        return result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        self.result = result
        return result
    
    def power(self, a, b):
        result = a ** b
        self.history.append(f"{a} ^ {b} = {result}")
        self.result = result
        return result
    
    def modulo(self, a, b):
        if b == 0:
            raise ValueError("Cannot modulo by zero")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        self.result = result
        return result
    
    def clear_history(self):
        self.history = []
        self.result = 0
    
    def get_history(self):
        return self.history
    
    def get_last_result(self):
        return self.result
    
    def calculate_expression(self, expression):
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            self.result = result
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def factorial(self, n):
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        self.history.append(f"{n}! = {result}")
        self.result = result
        return result
    
    def fibonacci(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        self.history.append(f"fib({n}) = {b}")
        self.result = b
        return b
    
    def memory_store(self, value):
        self.memory = value
        return self.memory
    
    def memory_recall(self):
        return self.memory
    
    def memory_add(self, value):
        self.memory += value
        return self.memory
    
    def memory_clear(self):
        self.memory = 0
        return self.memory

# Advanced calculator operations
class ScientificCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.constants = {
            'pi': 3.14159265359,
            'e': 2.71828182846
        }
    
    def sin(self, angle):
        import math
        result = math.sin(math.radians(angle))
        self.history.append(f"sin({angle}°) = {result}")
        self.result = result
        return result
    
    def cos(self, angle):
        import math
        result = math.cos(math.radians(angle))
        self.history.append(f"cos({angle}°) = {result}")
        self.result = result
        return result
    
    def tan(self, angle):
        import math
        result = math.tan(math.radians(angle))
        self.history.append(f"tan({angle}°) = {result}")
        self.result = result
        return result
    
    def log(self, x, base=10):
        import math
        result = math.log(x, base)
        self.history.append(f"log_{base}({x}) = {result}")
        self.result = result
        return result
    
    def ln(self, x):
        import math
        result = math.log(x)
        self.history.append(f"ln({x}) = {result}")
        self.result = result
        return result
    
    def sqrt(self, x):
        import math
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(x)
        self.history.append(f"√{x} = {result}")
        self.result = result
        return result

# Demonstration
if __name__ == "__main__":
    calc = Calculator()
    sci_calc = ScientificCalculator()
    
    print("Basic Calculator Operations:")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    
    print("\nScientific Calculator Operations:")
    print(f"sin(30) = {sci_calc.sin(30)}")
    print(f"cos(60) = {sci_calc.cos(60)}")
    print(f"log(100) = {sci_calc.log(100)}")
    print(f"√25 = {sci_calc.sqrt(25)}")
    
    print(f"\nCalculation history: {calc.get_history()}")
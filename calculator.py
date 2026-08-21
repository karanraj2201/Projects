#Baic Calculator program
print("||       Welcome to my basic calculator program    ||")
print("||   This program can perform basic arithmetic operations like addition, subtraction, multiplication and division  ||")
print("     Enter q to exit the program")
class Calculator():
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
    def sum(self):
        return self.a + self.b
    def subtract(self):
        return self.a - self.b
    def multiply(self):
        return self.a * self.b
    def divide(self):
        if self.b == 0:
            return "Error! Division by zero."
        else:
            return self.a / self.b
    def exit(self):
        print("Exiting the calculator. Goodbye!")
        exit()

try:
    while True:
        a=float(input("Enter first number: "))
        b=float(input("Enter second number: "))
        operation=input("Enter operation(+,-,*,/):")
        calc = Calculator(a,b)
        if operation == '+':
            print(calc.sum())
        elif operation == '-':
            print(calc.subtract())
        elif operation == '*':
            print(calc.multiply())
        elif operation == '/':
            print(calc.divide())
        elif operation == 'q':
            calc.exit()
except ValueError:
    print("Please input valid value only")
    
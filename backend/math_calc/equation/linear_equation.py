
from backend.math_calc.equation.equation import Equation

"""
This module is responsible for solving the mathematical linear
equations in the background. The form of these equations are:
a * x + b = 0"""
class Linear_equation(Equation):

    def __init__(self, equation):
        self.equation = equation
        self.a = equation[0]
        self.b = equation[1]

    def check(self):
        return self.a * self.x + self.b == 0

    def solve(self):
        self.x = (-1*(self.b))/self.a
        if self.check():
            return self.x
        return None

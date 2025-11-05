
from backend.math_calc.equation.equation import Equation
import numpy as np

"""
This module is responsible for solving the mathematical quadratic
equations in the background. The form of these equations are:
a * x^2 + b * x + c = 0"""
class Quadratic_equation(Equation):

    def __init__(self, equation):
        self.equation = equation
        self.a = equation[0]
        self.b = equation[1]
        self.c = equation[2]

    def check(self):
        return ((((self.a * (self.x[0] ** 2)) + (self.b * self.x[0]) + self.c) == 0)
                and (((self.a * (self.x[1] ** 2)) + (self.b * self.x[1]) + self.c) == 0))

    def solve(self):
        self.x = np.roots([self.a, self.b, self.c])
        if self.check():
            return self.x
        return None



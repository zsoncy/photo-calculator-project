"""
This module is the parent class, defining the equation class structure.
"""

def isint(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

class Equation:

    def __init__(self, equation):
        self.equation = equation

    def solve(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError
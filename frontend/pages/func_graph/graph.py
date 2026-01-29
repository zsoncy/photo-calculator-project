from types import NoneType

from customtkinter import *

from backend.math_calc.equation.equation import isint
from backend.math_calc.equation.quadratic_equation import Quadratic_equation

class Graph_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)


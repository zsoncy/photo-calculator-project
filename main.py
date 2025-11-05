
from backend.math_calc.equation.linear_equation import Linear_equation
from backend.math_calc.equation.quadratic_equation import Quadratic_equation

tuples_to_solve = [(2,1,-1),(11,-33),(9,3)]

for tup in tuples_to_solve:
    if len(tup) == 2:
        current_eq = Linear_equation(tup)
        print(current_eq.solve())
    elif len(tup) == 3:
        current_eq = Quadratic_equation(tup)
        print(current_eq.solve())

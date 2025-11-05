
from backend.math_calc.equation.linear_equation import Linear_equation
from backend.math_calc.equation.quadratic_equation import Quadratic_equation
from backend.math_calc.func_graph.function import Function

tuples_to_solve = [(2,1,-1),(11,-33),(9,3)]

for tup in tuples_to_solve:
    if len(tup) == 2:
        current_eq = Linear_equation(tup)
        print(current_eq.solve())
    elif len(tup) == 3:
        current_eq = Quadratic_equation(tup)
        print(current_eq.solve())


functions_to_visualize = ["2*x**2 + 3*x + 1",
                          "5*x**4 - 0.25*x**3 + 0.125*x - 1",
                          "sin(x) + sqrt(x)",
                          "0.25*x**3 - 0.75*x**2 + 1.5*x - 0.5",
                          "-x**2 + 2.5*x - 4.75",
                          "3*x**3 - 2*x**2 + x - 5",
                          "7*x**3 - x + 9",
                          "sin(x)**2 + sqrt(x) - log(x + 1)"]

for func in functions_to_visualize:
    f = Function(func)
    print(f.solve(2))
    print(f.derivative())
    f.visualize()

from backend.math_calc.equation.linear_equation import Linear_equation
from backend.math_calc.equation.quadratic_equation import Quadratic_equation
from backend.math_calc.func_graph.function import Function
from backend.math_calc.operation.operation import Operation

tuples_to_solve = [(2,1,-1),(11,-33),(9,3),(1,1,1)]

for tup in tuples_to_solve:
    if len(tup) == 2:
        current_eq = Linear_equation(tup)
        print(current_eq.solve())
    elif len(tup) == 3:
        current_eq = Quadratic_equation(tup)
        print(current_eq.solve())
        print(type(current_eq.solve()))


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


operations_to_solve = ["100 / 5 + 3 * 2",
                       "(15 - 3) * (7 + 1)",
                       "((15.5 + 4.5) * 3) / (2**3 - 2)",
                       "pow(5, 3) + round(10/3, 2)",
                       "25 // 3 + 7 % 3",
                       "80 / (2 * (5 + 3) - (10 ** 1 / 2)) * 5",
                       "((9 / 3) ** 2) * (100 / 10 + 5) - 4",
                       "((1 / 2) + (3 / 4)) * (5 + 6 / 3) - 1",
                       "100 - (5 * 4 + (2 ** 3 * 3)) / 4"]

for op in operations_to_solve:
    o = Operation(op)
    print(o.solve())
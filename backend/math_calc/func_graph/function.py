import sympy as sp

from backend.math_calc.func_graph.domain import def_domain, is_defined

"""
This module is responsible for evaluating and visualizing the functions given as string
"""
class Function:

    def __init__(self, expr_str: str):
        self.x = sp.Symbol('x')
        self.expr = sp.sympify(expr_str)

    def get_domain(self):
        return def_domain(self.expr)

    def solve(self,value):
        if is_defined(self.expr,value):
            return self.expr.subs(self.x,value)
        return None

    def visualize(self,x_range=(-10,10)):
        full_domain = def_domain(self.expr)
        if full_domain is True:
            sp.plot(self.expr, (self.x, x_range[0], x_range[1]))
            return

        lower_bound, upper_bound = x_range

        exceptions = full_domain.args if isinstance(full_domain,sp.And) else [full_domain]

        for exception in exceptions:
            if isinstance(exception, sp.Rel):
                if (exception.__class__.__name__ in ('StrictGreaterThan', 'GreaterThan')
                        and exception.lhs == self.x):
                    lower_bound = max(lower_bound, float(exception.rhs))
                if (exception.__class__.__name__ in ('StrictLessThan', 'LessThan')
                        and exception.lhs == self.x):
                    upper_bound = min(upper_bound, float(exception.rhs))

        if lower_bound < upper_bound:
            sp.plot(self.expr, (self.x,lower_bound,upper_bound))
        else:
            print("ERROR: Cant visualize the function: there is no valid domain.")



    def derivative(self):
        return sp.diff(self.expr, self.x)

    def __str__(self):
        return str(self.expr)
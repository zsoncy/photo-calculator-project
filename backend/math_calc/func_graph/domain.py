
import sympy as sp

x = sp.Symbol('x')


""" 
This module is responsible for defining the domain for the function so that 
it can prevent occasional errors caused by log- sqrt- or division functions.
This way we can plot the function on the correct domain."""
def def_domain(expr):

    constraints = []

    for sub_expr in sp.preorder_traversal(expr):
        """ 
        This statement is responsible for handling the Log(x): x > 0 restriction"""
        if isinstance(sub_expr, sp.log):
            arg = sub_expr.args[0]
            constraints.append(sp.Rel(arg, 0 , '>'))
            """
            This statement is responsible for handling the division by 0 restriction inside log"""
            if isinstance(arg, sp.Pow) and arg.args[1] == -1:
                numb = arg.args[0]
                constraints.append(sp.Ne(numb, 0))

        """
        This statement is responsible for handling the sqrt(x): x >= 0 restriction"""
        if isinstance(sub_expr, sp.Pow) and sub_expr.args[1] == sp.Rational(1, 2):
            arg = sub_expr.args[0]
            constraints.append(sp.Rel(arg, 0, '>='))

        """ 
        This statement is responsible for handling the division by 0 restriction"""
        if isinstance(sub_expr, sp.Pow) and sub_expr.args[1] == -1:
            numb = sub_expr.args[0]
            constraints.append(sp.Ne(numb, 0))

        """
        This statement is responsible for handling the division by 0 restriction inside multiplication"""
        if isinstance(sub_expr, sp.Mul):
            for arg in sub_expr.args:
                if isinstance(arg, sp.Pow) and arg.args[1] == -1:
                    numb = arg.args[0]
                    constraints.append(sp.Ne(numb, 0))


    return sp.And(*constraints) if constraints else True


def is_defined(expr, value):
    full_domain = def_domain(expr)
    try:
        return bool(full_domain.subs(x, value))
    except Exception:
        return False

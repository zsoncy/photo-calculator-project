from types import NoneType

from customtkinter import *

from backend.math_calc.equation.equation import isint
from backend.math_calc.operation.operation import iscorrectoperation, Operation
from backend.math_calc.equation.linear_equation import Linear_equation
from backend.math_calc.equation.quadratic_equation import Quadratic_equation

class Answer_Page(CTkFrame):
    def __init__(self, root, ans):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ans=ans

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"


        def operation_solve():
            op = ans[0]
            if iscorrectoperation(op):
                current_op = Operation(op)
                return current_op.solve()
            else:
                return "Wrong input!"

        def linear_solve():
            a = ans[0]
            b = ans[1]
            if isint(a) and isint(b):
                current_eq = Linear_equation((int(a), int(b)))
                result = current_eq.solve()
                return "X = " + str(result)
            else:
                return "Wrong parameters!"

        def quadratic_solve():
            a = ans[0]
            b = ans[1]
            c = ans[2]
            if isint(a) and isint(b) and isint(c):
                current_eq = Quadratic_equation((int(a), int(b), int(c)))
                result = current_eq.solve()
                if type(result) == NoneType:
                    return "No real roots!"
                else:
                    return "X1 = " + str(result[0]) + "  X2 = " + str(result[1])
            else:
                return "Wrong parameters!"



        label_result = CTkLabel(self, text="Calculating . . .", height=120, width=100, font=("Helvetica", 80),
                                corner_radius=50, text_color="#370d40", fg_color="#6D8EA0")
        label_result.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, ipadx=50, ipady=5)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=2, sticky="es", padx=(0, 100), pady=(0, 50))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("processing", direction="right"))
        button_back.grid(row=0, column=0, sticky="w",  padx=(0, 20))

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="w",  padx=(0, 20))

        final_output = "Error"

        try:
            length = len(self.ans)

            if length == 1:
                # Simple Expression
                final_output = operation_solve()
            elif length == 2:
                # Linear Equation
                final_output = linear_solve()
            elif length == 3:
                # Quadratic Equation
                final_output = quadratic_solve()
            else:
                final_output = "Unknown Format"

        except Exception as e:
            print(f"Solver Error: {e}")
            final_output = "Error"

        label_result.configure(text=final_output)




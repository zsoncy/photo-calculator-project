from types import NoneType

from customtkinter import *

from backend.math_calc.equation.equation import isint
from backend.math_calc.equation.quadratic_equation import Quadratic_equation

class Quadratic_Eq_Page(CTkFrame):
    def init(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def calc():

            label_result.configure(text="Calculating . . .")
            a = entry_a.get()
            b = entry_b.get()
            c = entry_c.get()
            if isint(a) and isint(b) and isint(c):
                current_eq = Quadratic_equation((int(a), int(b), int(c)))
                result= current_eq.solve()
                if type(result) == NoneType:
                    label_result.configure(text="No real roots!")
                else:
                    label_result.configure(text="X1 = " + str(result[0]) + "  X2 = " + str(result[1]))
            else:
                label_result.configure(text="Wrong parameters!")


        entry_a = CTkEntry(self, placeholder_text="a",  state="normal",
                           height=50, width=100, font=("Helvetica", 80),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry_a.grid(row=0, column=0, sticky="ew", padx=(100,0), pady=200)

        label_1 = CTkLabel(self, text="x²  +", height=50, width=100, font=("Helvetica", 80),
                           corner_radius=7, text_color="#DDC3C3", fg_color="#4e1d58")
        label_1.grid(row=0, column=1, sticky="ew", pady=200, ipadx=50, ipady=5)

        entry_b = CTkEntry(self,  placeholder_text="b",  state="normal",
                           height=50, width=100, font=("Helvetica", 80),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry_b.grid(row=0, column=2, sticky="ew", pady=200)

        label_2 = CTkLabel(self, text="x +", height=50, width=50, font=("Helvetica", 80),
                           corner_radius=7, text_color="#DDC3C3", fg_color="#4e1d58")
        label_2.grid(row=0, column=3, sticky="ew", pady=200, ipadx=50, ipady=5)

        entry_c = CTkEntry(self,  placeholder_text="c",  state="normal",
                           height=50, width=100, font=("Helvetica", 80),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry_c.grid(row=0, column=4, sticky="ew", pady=200)

        label_3 = CTkLabel(self, text="= 0", height=50, width=50, font=("Helvetica", 80),
                           corner_radius=7, text_color="#DDC3C3", fg_color="#4e1d58")
        label_3.grid(row=0, column=5, sticky="ew", padx=(0, 100), pady=200, ipadx=50, ipady=5)

        label_result = CTkLabel(self, text=" X = ", height=200, width=100, font=("Helvetica", 100),
                                corner_radius=50, text_color="#370d40", fg_color="orange")
        label_result.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(110,10),  ipadx=50, ipady=5)

        button_calc = CTkButton(master=self, text="Calculate", height=200, width=100, fg_color="orange",
                                text_color="#370d40", font=("Helvetica", 40), corner_radius=50, command=calc)
        button_calc.grid(row=1, column=4, columnspan=2, sticky="ew", padx=(10,110),  ipadx=50, ipady=5)


        """Button hover effect, for it to change the font color as well"""
        button_calc.bind("<Enter>", lambda event: button_calc.configure(fg_color="#4e1d58", text_color="orange"))
        button_calc.bind("<Leave>", lambda event: button_calc.configure(fg_color="orange", text_color="#370d40"))
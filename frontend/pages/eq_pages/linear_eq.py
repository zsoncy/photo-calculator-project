from customtkinter import *

from backend.math_calc.equation.equation import isint
from backend.math_calc.equation.linear_equation import Linear_equation

class Linear_Eq_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        def calc():
            label_result.configure(text="Calculating . . .")
            a = entry_a.get()
            b = entry_b.get()
            if isint(a) and isint(b):
                current_eq = Linear_equation((int(a), int(b)))
                result = current_eq.solve()
                label_result.configure(text="X = " + str(result))
            else:
                label_result.configure(text="Wrong parameters!")

        entry_a = CTkEntry(self, placeholder_text="a",  state="normal",
                           height=50, width=100, font=("Helvetica", 80),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry_a.grid(row=0, column=0, sticky="ew", padx=(100,0), pady=50)

        label_1 = CTkLabel(self, text="x  +", height=50, width=100, font=("Helvetica", 80),
                           corner_radius=7, text_color="#DDC3C3", fg_color="#4e1d58")
        label_1.grid(row=0, column=1, sticky="ew", pady=50, ipadx=50, ipady=5)

        entry_b = CTkEntry(self,  placeholder_text="b",  state="normal",
                           height=50, width=100, font=("Helvetica", 80),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry_b.grid(row=0, column=2, sticky="ew", pady=50)

        label_2 = CTkLabel(self, text="= 0", height=50, width=50, font=("Helvetica", 80),
                           corner_radius=7, text_color="#DDC3C3", fg_color="#4e1d58")
        label_2.grid(row=0, column=3, sticky="ew", padx=(0,100), pady=50, ipadx=50, ipady=5)

        label_result = CTkLabel(self, text=" X = ", height=120, width=100, font=("Helvetica", 80),
                                corner_radius=50, text_color="#370d40", fg_color="#6D8EA0")
        label_result.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(110,10),  ipadx=50, ipady=5)

        button_calc = CTkButton(master=self, text="Calculate", height=120, width=100, fg_color="#6D8EA0",
                                text_color="#370d40", font=("Helvetica", 40), corner_radius=50, command=calc)
        button_calc.grid(row=1, column=3, sticky="ew", padx=(10,110),  ipadx=50, ipady=5)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=4, sticky="e", padx=(0, 100), pady=(0,30))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50,
                             command=lambda: root.slide_to_page("select_eq", direction="right"))
        button_back.grid(row=0, column=0, sticky="e", padx=(10, 0), ipady=20, ipadx=20)

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50,
                             command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="e", padx=(10, 0), ipady=20, ipadx=20)

        """Button hover effect, for it to change the font color as well"""
        button_calc.bind("<Enter>", lambda event: button_calc.configure(fg_color="#4e1d58", text_color="#6D8EA0"))
        button_calc.bind("<Leave>", lambda event: button_calc.configure(fg_color="#6D8EA0", text_color="#370d40"))
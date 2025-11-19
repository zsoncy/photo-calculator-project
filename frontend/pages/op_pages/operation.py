from customtkinter import *

from backend.math_calc.operation.operation import iscorrectoperation, Operation

class Operation_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        def calc():
            label_result.configure(text="Calculating . . .")
            op = entry.get()
            if iscorrectoperation(op):
                current_op = Operation(op)
                label_result.configure(text=current_op.solve())
            else:
                label_result.configure(text="Wrong input!")


        entry = CTkEntry(self, placeholder_text="Enter the operation line here...",  state="normal",
                           height=40, width=100, font=("Helvetica", 50),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        entry.grid(row=0, column=0, columnspan=2, sticky="ew", padx=100, pady=(100,50), ipadx=50, ipady=50)


        label_result = CTkLabel(self, text=" . . . ", height=120, width=100, font=("Helvetica", 80),
                                corner_radius=50, text_color="#370d40", fg_color="#6D8EA0")
        label_result.grid(row=1, column=0, sticky="ew", padx=(110,10),  ipadx=50, ipady=5)

        button_calc = CTkButton(master=self, text="Calculate", height=120, width=100, fg_color="#6D8EA0",
                                text_color="#370d40", font=("Helvetica", 40), corner_radius=50, command=calc)
        button_calc.grid(row=1, column=1, sticky="ew", padx=(10,110),  ipadx=50, ipady=5)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=2, sticky="e", padx=(0, 100), pady=(0, 30))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                                text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50,
                                command=lambda: root.slide_to_page("select_calc", direction="right"))
        button_back.grid(row=0, column=0, sticky="e", padx=(10, 0), ipady=20, ipadx=20)

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                                text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50,
                                command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="e", padx=(10, 0), ipady=20, ipadx=20)


        """Button hover effect, for it to change the font color as well"""
        button_calc.bind("<Enter>", lambda event: button_calc.configure(fg_color="#4e1d58", text_color="#6D8EA0"))
        button_calc.bind("<Leave>", lambda event: button_calc.configure(fg_color="#6D8EA0", text_color="#370d40"))
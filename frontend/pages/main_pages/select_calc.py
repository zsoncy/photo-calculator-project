from customtkinter import *

class Select_Calc_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        button_1 = CTkButton(master=self, text="Equation", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("select_eq", direction="left"))
        button_1.grid(row=0, column=0, sticky="ew", padx=50, pady=(300,100), ipady=20, ipadx=20)

        button_2 = CTkButton(master=self, text="Calculator", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("operation", direction="left"))
        button_2.grid(row=0, column=1, sticky="ew", padx=50, pady=(300,100), ipady=20, ipadx=20)

        button_3 = CTkButton(master=self, text="Function graph", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50)
        button_3.grid(row=0, column=2, sticky="ew", padx=50, pady=(300,100), ipady=20, ipadx=20)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=1, column=0, columnspan=3, sticky="e", padx=50)

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("main", direction="right"))
        button_back.grid(row=0, column=0, ipady=20, ipadx=20)


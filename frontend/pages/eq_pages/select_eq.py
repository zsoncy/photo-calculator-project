from customtkinter import *

class Select_Eq_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        button_1 = CTkButton(master=self, text="Linear", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("linear", direction="left"))
        button_1.grid(row=0, column=0, sticky="ew", padx=100, pady=(300,100), ipady=20, ipadx=20)

        button_2 = CTkButton(master=self, text="Quadratic", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("quadratic", direction="left"))
        button_2.grid(row=0, column=1, sticky="ew", padx=100, pady=(300,100), ipady=20, ipadx=20)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=1, column=0, columnspan=2, sticky="e", padx=(0,100))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("select_calc", direction="right"))
        button_back.grid(row=0, column=0, sticky="e", padx=(10,0), ipady=20, ipadx=20)

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="e", padx=(10, 0), ipady=20, ipadx=20)

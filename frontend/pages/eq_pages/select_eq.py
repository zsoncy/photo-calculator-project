from customtkinter import *

class Select_Eq_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        button_1 = CTkButton(master=self, text="Linear", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("linear", direction="left"))
        button_1.grid(row=0, column=0, sticky="ew", padx=100, pady=400, ipady=20, ipadx=20)

        button_2 = CTkButton(master=self, text="Quadratic", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("quadratic", direction="left"))
        button_2.grid(row=0, column=1, sticky="ew", padx=100, pady=400, ipady=20, ipadx=20)

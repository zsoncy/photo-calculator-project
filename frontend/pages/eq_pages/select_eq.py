from customtkinter import *

class Select_Eq_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"


        container = CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0)

        button_1 = CTkButton(master=container, text="Linear", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40, "bold"), width=400,
                             height=100, corner_radius=25,
                             command=lambda: root.slide_to_page("linear", direction="left"))
        button_1.grid(row=0, column=0, padx=30)

        button_2 = CTkButton(master=container, text="Quadratic", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40, "bold"), width=400,
                             height=100, corner_radius=25,
                             command=lambda: root.slide_to_page("quadratic", direction="left"))
        button_2.grid(row=0, column=2, padx=30)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=3, sticky="es", padx=50, pady=(0, 50))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                                text_color="#DDC3C3", font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
                                command=lambda: root.slide_to_page("select_calc", direction="right"))
        button_back.grid(row=0, column=0, sticky="sw", padx=(0, 50))

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24, "bold"), height=60, corner_radius=50, command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="sw", padx=(0, 50))

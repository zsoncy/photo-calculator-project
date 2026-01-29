from types import NoneType

from customtkinter import *


class Photo_Graph_Page(CTkFrame):
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



        def function_solve():
            return




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






from types import NoneType

from customtkinter import *


class Photo_Graph_Page(CTkFrame):
    def __init__(self, root, orig, ans):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ans=ans
        self.orig = orig

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        self.lbl_title = CTkLabel(self, text="Graph Viewer",
                                  font=("Helvetica", 32, "bold"), text_color="#4e1d58")
        self.lbl_title.grid(row=0, column=0, pady=(20, 10))

        self.graph_frame = CTkFrame(self, fg_color="white", corner_radius=20)
        self.graph_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        # grid it in the update_graph()

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






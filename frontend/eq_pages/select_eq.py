from customtkinter import *

from frontend.eq_pages.linear_eq import Linear_Eq_Page
from frontend.eq_pages.quadratic_eq import Quadratic_Eq_Page
from frontend.page import Page

class Select_Eq_Page(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root,*args, **kwargs)
        self.root=root

        def page1():
            button_1.destroy()
            button_2.destroy()
            Linear_Eq_Page(self.root)

        def page2():
            button_1.destroy()
            button_2.destroy()
            Quadratic_Eq_Page(self.root)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        button_1 = CTkButton(master=root, text="Linear", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=page1)
        button_1.grid(row=0, column=0, sticky="ew", padx=100, pady=400, ipady=20, ipadx=20)

        button_2 = CTkButton(master=root, text="Quadratic", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=page2)
        button_2.grid(row=0, column=1, sticky="ew", padx=100, pady=400, ipady=20, ipadx=20)

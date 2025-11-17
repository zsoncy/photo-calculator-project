from customtkinter import *

from frontend.pages.eq_pages.linear_eq import Linear_Eq_Page
from frontend.pages.eq_pages.quadratic_eq import Quadratic_Eq_Page
from frontend.pages.eq_pages.select_eq import Select_Eq_Page
from frontend.pages.main_pages.main_page import Main_Page
from frontend.pages.main_pages.select_calc import Select_Calc_Page
from frontend.pages.op_pages.operation import Operation_Page


class App(CTk):
    def __init__(self):
        super().__init__(fg_color="#DDC3C3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title = "Photo Calculator"
        self.geometry("1600x900")
        self.minsize(1550, 850)
        self.iconbitmap("../../LOGO.ico")
        self.pages = {}
        self.current_page = None

        self.pages["main"] = Main_Page(self)
        self.pages["select_calc"] = Select_Calc_Page(self)
        self.pages["select_eq"] = Select_Eq_Page(self)
        self.pages["linear"] = Linear_Eq_Page(self)
        self.pages["quadratic"] = Quadratic_Eq_Page(self)
        self.pages["operation"] = Operation_Page(self)

        self.show_page("main")

    def show_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        self.current_page = page_name

    def slide_to_page(self, page_name, direction="left"):
        if self.current_page:
            old_page = self.pages[self.current_page]
        else:
            old_page = None

        new_page = self.pages[page_name]
        width = self.winfo_width()
        x_start = width if direction == "left" else -width
        new_page.place(x=x_start, y=0, relheight=1, relwidth=1)

        step = 30

        def animate():
            nonlocal x_start
            if direction == "left":
                x_start -= step
                if x_start <= 0:
                    x_start = 0
            else:
                x_start += step
                if x_start >= 0:
                    x_start = 0
            new_page.place(x=x_start, y=0)
            if x_start != 0:
                self.after(10, animate)
            else:
                if old_page:
                    old_page.place_forget()
                self.current_page = page_name

        animate()


if __name__ == '__main__':
    app = App()
    app.mainloop()







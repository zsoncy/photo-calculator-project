
from customtkinter import *

from utils.config import load_config, save_config
from frontend.pages.eq_pages.linear_eq import Linear_Eq_Page
from frontend.pages.eq_pages.quadratic_eq import Quadratic_Eq_Page
from frontend.pages.eq_pages.select_eq import Select_Eq_Page
from frontend.pages.main_pages.main_page import Main_Page
from frontend.pages.main_pages.select_calc import Select_Calc_Page
from frontend.pages.op_pages.operation import Operation_Page
from frontend.pages.main_pages.open_image import Open_Image_Page


class App(CTk):
    def __init__(self):
        super().__init__(fg_color="#DDC3C3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title = "Photo Calculator"
        self.geometry("1600x900")
        self.minsize(1550, 850)
        self.iconbitmap("../../LOGO.ico")
        cfg = load_config()
        self.last_dir = cfg.get("last_dir") or os.path.expanduser("~")

        self.pages = {}
        self.current_page = None

        # --- Create and register all pages ---
        self.pages["main"] = Main_Page(self)
        self.pages["select_calc"] = Select_Calc_Page(self)
        self.pages["select_eq"] = Select_Eq_Page(self)
        self.pages["linear"] = Linear_Eq_Page(self)
        self.pages["quadratic"] = Quadratic_Eq_Page(self)
        self.pages["operation"] = Operation_Page(self)
        self.pages["open_image"] = Open_Image_Page(self)



        # --- Windows-only shortcuts (no bind_all; bind on toplevel) ---
        # Ctrl+O  -> trigger Open Image dialog on the open_image page
        self.bind("<Control-o>", lambda e: self.pages["open_image"].open_image_dialog())
        # Esc     -> go back to main page with a right slide
        self.bind("<Escape>", self._on_escape)


        # Show initial page
        self.show_page("main")


    def _on_escape(self, _event=None):
        # Do nothing if we are already on main
        if self.current_page == "main":
            return
        self.slide_to_page("main", direction="right")


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

        if direction == "left":
            x_new_start = width
            x_old_start = 0
        else:
            x_new_start = -width
            x_old_start = 0

        new_page.place(x=x_new_start, y=0, relwidth=1, relheight=1)
        if old_page:
            old_page.place(x=x_old_start, y=0, relwidth=1, relheight=1)

        step = 45
        x_new = x_new_start
        x_old = x_old_start

        def animate():
            nonlocal x_new, x_old

            if direction == "left":
                x_new -= step
                x_old -= step
                if x_new <= 0:
                    x_new = 0
            else:
                x_new += step
                x_old += step
                if x_new >= 0:
                    x_new = 0

            new_page.place(x=x_new, y=0)
            if old_page:
                old_page.place(x=x_old, y=0)

            if x_new != 0:
                self.after(5, animate)
            else:
                if old_page:
                    old_page.place_forget()
                self.current_page = page_name

                # If a page defines an on_show hook (e.g., Processing_Page),
                # call it after the animation finishes.
                page_obj = self.pages.get(page_name)
                if hasattr(page_obj, "on_show"):
                    page_obj.on_show(self)

        animate()


if __name__ == '__main__':
    app = App()
    app.mainloop()

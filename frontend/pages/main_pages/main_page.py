from customtkinter import *
from PIL import Image

class Main_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"


        logo = CTkImage(Image.open("../../LOGO.png"), size=(850, 850))
        logo_label = CTkLabel(self, text="", image=logo)
        logo_label.grid(row=0, column=0, rowspan=2, sticky="nsew", pady=20)


        right_frame = CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(0,100), pady=40)
        right_frame.grid_rowconfigure((0,1,2), weight=1)
        right_frame.grid_columnconfigure(0, weight=1)


        title_label = CTkLabel(master=right_frame, text="Photo Calculator",
                               font=("Helvetica", 80, 'bold', 'underline'), text_color="#370d40")
        title_label.grid(row=0, column=0, pady=(100, 40))

        button_1 = CTkButton(master=right_frame, text="Open an image", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("open_image", direction="left"))
        button_1.grid(row=1, column=0, pady=(50, 0), ipadx=20, ipady=10)

        button_2 = CTkButton(master=right_frame, text="Continue with manual input", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 40), corner_radius=50, command=lambda: root.slide_to_page("select_calc", direction="left")
)
        button_2.grid(row=2, column=0, pady=(0, 100), ipadx=20, ipady=10)
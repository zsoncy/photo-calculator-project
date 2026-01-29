from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re
from sympy import sympify, Symbol, Poly, simplify

import numpy as np

from customtkinter import *


class Graph_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.current_canvas = None
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(2, weight=0)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"


        self.entry = CTkEntry(self, placeholder_text="Enter the polynomial function here: f(x)=",  state="normal",
                           height=80, width=100, font=("Helvetica", 50),
                           text_color="#DDC3C3", fg_color="#4e1d58")
        self.entry.grid(row=0, column=0, columnspan=2, sticky="ew", padx=100, pady=(50,10))

        button_calc = CTkButton(master=self, text="Calculate", height=80, fg_color="#6D8EA0",
                                text_color="#370d40", font=("Helvetica", 40, "bold"), corner_radius=50, command=self.calc)
        button_calc.grid(row=0, column=2, sticky="ew", padx=100, pady=(50,10) )

        self.graph_frame = CTkFrame(self, fg_color="white", corner_radius=20)
        self.graph_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=40, pady=20)

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=3, sticky="es", padx=(0, 100), pady=(50, 50))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("select_calc", direction="right"))
        button_back.grid(row=0, column=0, sticky="w",  padx=(0, 20))

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="w",  padx=(0, 20))


        # Button hover effect, for it to change the font color as well
        button_calc.bind("<Enter>", lambda event: button_calc.configure(fg_color="#4e1d58", text_color="#6D8EA0"))
        button_calc.bind("<Leave>", lambda event: button_calc.configure(fg_color="#6D8EA0", text_color="#370d40"))

    def calc(self):
        func_str = self.entry.get()

        if not func_str:
            return

        # HEALING
        clean_str = func_str.lower().replace(" ", "")
        clean_str = re.sub(r"(\d)x", r"\1*x", clean_str)  # Fix implicit mult
        clean_str = clean_str.replace("^", "**")  # Fix power syntax

        # Validate
        try:
            x = Symbol('x')
            expr = sympify(clean_str)
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            coeffs_float = [float(c) for c in coeffs]
            print(f"Plotting: {coeffs_float}")
            self.draw_graph(coeffs_float)
            # Reset color
            self.entry.configure(fg_color="#4e1d58")

        except Exception as e:
            print(f"Invalid Input: {e}")
            # Color if error
            self.entry.configure(fg_color="#B00020")

    def draw_graph(self, coeffs):

        # Clear old graph
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None

        # Default view
        x_min, x_max = -10, 10

        # Zoom in where f(x)=0 (vertex)
        if len(coeffs) == 3:
            a, b, c = coeffs
            if a != 0:
                vertex_x = -b / (2 * a)

                # Zoom in
                x_min = vertex_x - 5
                x_max = vertex_x + 5

        # Generate X values around the vertex
        x = np.linspace(x_min, x_max, 400)

        # Calculate Y
        y = np.polyval(coeffs, x)

        # Plotting
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Style
        ax.plot(x, y, color="#4e1d58", linewidth=3)
        ax.grid(True, linestyle="--", alpha=0.5)

        # Draw axes
        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)

        # Force the margins to be tight
        ax.autoscale(enable=True, axis='y', tight=True)

        # Show Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.current_canvas = canvas
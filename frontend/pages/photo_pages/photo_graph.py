from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from customtkinter import *


class Photo_Graph_Page(CTkFrame):
    def __init__(self, root, orig, ans):
        super().__init__(root)

        self.current_canvas = None
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.ans=ans
        self.orig = orig

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator"

        self.lbl_title = CTkLabel(self, text="Graph Viewer",
                                  font=("Helvetica", 50, "bold"), text_color="#4e1d58")
        self.lbl_title.grid(row=0, column=0, pady=(50, 10))

        self.graph_frame = CTkFrame(self, fg_color="white", corner_radius=20)
        self.graph_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        # grid it in the update_graph()

        bottom = CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="es", padx=(0, 100), pady=(50, 50))

        button_back = CTkButton(master=bottom, text="BACK", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("processing", direction="right"))
        button_back.grid(row=0, column=0, sticky="w",  padx=(0, 20))

        button_home = CTkButton(master=bottom, text="HOME", fg_color="#4e1d58", hover_color="#370d40",
                             text_color="#DDC3C3", font=("Helvetica", 24), height=60, corner_radius=50,
                             command=lambda: root.slide_to_page("main", direction="right"))
        button_home.grid(row=0, column=1, sticky="w",  padx=(0, 20))

    def update_data(self, orig_str, coeffs):

        self.lbl_title.configure(text=f"f(x) = {orig_str}")

        try:
            poly_coeffs = [float(c) for c in coeffs]
        except:
            print("Error converting coefficients")
            return

        self.draw_graph(poly_coeffs)

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




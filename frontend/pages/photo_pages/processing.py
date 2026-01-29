from customtkinter import *
from PIL import Image
import cv2
import numpy as np


class Processing_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator - Processing"

        # Simple Layout: Viewers take up almost all space, Buttons at bottom
        self.grid_rowconfigure(0, weight=1)  # Viewers area
        self.grid_rowconfigure(1, weight=0)  # Footer Buttons
        self.grid_columnconfigure(0, weight=1)

        # ---------- 1. Viewers (Original vs Processed) ----------
        center = CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        center.grid_rowconfigure(0, weight=0)  # Text labels (compact)
        center.grid_rowconfigure(1, weight=1)  # Images (expand)

        # Labels for context
        self.lbl_left = CTkLabel(center, text="Original Input", text_color="#4e1d58", font=("Helvetica", 16, "bold"))
        self.lbl_left.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.lbl_right = CTkLabel(center, text="Processed Image", text_color="#4e1d58",
                                  font=("Helvetica", 16, "bold"))
        self.lbl_right.grid(row=0, column=1, sticky="ew", pady=(0, 5))

        # Image Containers
        self.left = CTkLabel(center, text="", text_color="#370d40")
        self.right = CTkLabel(center, text="", text_color="#370d40")
        self.left.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        self.right.grid(row=1, column=1, sticky="nsew", padx=(12, 0))

        # Resize hooks
        self.left.bind("<Configure>", lambda e: self._redraw("left"))
        self.right.bind("<Configure>", lambda e: self._redraw("right"))

        # ---------- 2. Footer Buttons (Minimal) ----------
        footer = CTkFrame(self, fg_color="transparent")
        footer.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 50))
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)
        footer.grid_columnconfigure(2, weight=1)

        self.btn_back = CTkButton(
            footer, text="BACK",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
            command=lambda: root.slide_to_page("open_image", direction="right")
        )
        self.btn_back.grid(row=0, column=0, sticky="w", padx=(0, 20))

        self.btn_calc = CTkButton(
            footer, text="SOLVE EQUATION →",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 20, "bold"), height=50, corner_radius=50,
            command=lambda: root.slide_to_page("answer", direction="left")
        )
        self.btn_calc.grid(row=0, column=2, sticky="ew", padx=(12, 0))

        self.btn_graph = CTkButton(
            footer, text="SHOW GRAPH →",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 20, "bold"), height=50, corner_radius=50,
            command=lambda: root.slide_to_page("photo_graph", direction="left")
        )
        self.btn_graph.grid(row=1, column=2, sticky="ew", padx=(12, 0))

        # ---------- State ----------
        self.img_left = None  # PIL.Image
        self.img_right = None  # PIL.Image
        self.ctk_left = None
        self.ctk_right = None

    def on_show(self, root):
        cv_rgb = getattr(root, "cv_image_rgb", None)
        cv_bgr = getattr(root, "cv_image_bgr", None)

        if cv_rgb is None or cv_bgr is None:
            return

        # Show Original
        self.img_left = Image.fromarray(cv_rgb)
        self._redraw("left")

        # Run Auto-Processing
        self._run_auto_pipeline(cv_bgr, root)

    def _run_auto_pipeline(self, cv_bgr, root):
        # 1. Resize for consistency
        h, w = cv_bgr.shape[:2]
        target_h = 1000
        scale = target_h / float(h)
        target_w = int(w * scale)

        img_resized = cv2.resize(cv_bgr, (target_w, target_h))

        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        # 2. Gaussian Blur (The "Sunglasses")
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 3. Adaptive Threshold (The "Scanner")
        bw = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            41, 15
        )

        # 4. Morphological Open (Clean noise)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        bw_clean = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

        # Display & Store
        display = cv2.cvtColor(bw_clean, cv2.COLOR_GRAY2RGB)
        self.img_right = Image.fromarray(display)
        self._redraw("right")

        root.cv_pre_binary = bw_clean
        root.cv_pre_display = display

    def _redraw(self, which):
        target = self.left if which == "left" else self.right
        pil_img = self.img_left if which == "left" else self.img_right

        if pil_img is None:
            return

        w = max(1, target.winfo_width())
        h = max(1, target.winfo_height())

        img = pil_img.copy()
        img.thumbnail((w, h), Image.LANCZOS)

        ctk_img = CTkImage(light_image=img, dark_image=img, size=img.size)

        if which == "left":
            self.ctk_left = ctk_img
        else:
            self.ctk_right = ctk_img

        target.configure(image=ctk_img)
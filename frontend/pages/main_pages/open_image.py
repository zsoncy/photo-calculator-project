from utils.config import load_config, save_config
from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2
import os


class Open_Image_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        # Layout:
        # Row 0: Top Bar (Open Button + Label)
        # Row 1: Preview (Expands)
        # Row 2: Footer (Back / Next Buttons)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator - Open Image"

        # ---- State ----
        self.cv_image = None
        self.pil_image = None
        self.ctk_image = None
        cfg = load_config()
        self.last_dir = cfg.get("last_dir") or os.path.expanduser("~")

        # ---------- 1. Top Bar (Open File) ----------
        top = CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        top.grid_columnconfigure(0, weight=1)  # Button
        top.grid_columnconfigure(1, weight=1)  # Label space

        open_btn = CTkButton(
            master=top, text="Open Image…",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24), corner_radius=50,
            command=self.open_image_dialog
        )
        open_btn.grid(row=0, column=0, padx=(0, 12))

        self.path_label = CTkLabel(
            master=top, text="No file selected", anchor="w",
            text_color="#370d40", font=("Helvetica", 20)
        )
        self.path_label.grid(row=0, column=1, sticky="ew")

        # ---------- 2. Preview Area ----------
        self.preview = CTkLabel(self, text="Preview will appear here", text_color="#370d40")
        self.preview.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 12))
        self.preview.bind("<Configure>", self._redraw_preview)

        # ---------- 3. Footer Buttons ----------
        footer = CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=24, pady=(50, 50))
        footer.grid_columnconfigure(0, weight=1)  # Left side
        footer.grid_columnconfigure(1, weight=0)  # Space
        footer.grid_columnconfigure(2, weight=1)  # Right side

        back_btn = CTkButton(
            master=footer, text="BACK",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
            command=lambda: root.slide_to_page("main", direction="right")
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=(0, 20))

        process_btn = CTkButton(
            master=footer, text="GO TO PROCESSING →",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24, "bold"), height=60, corner_radius=50,
            command=lambda: root.slide_to_page("processing", direction="left")
        )
        process_btn.grid(row=0, column=2, sticky="e", padx=(20, 0))

    def open_image_dialog(self):
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Open Image",
            initialdir=self.last_dir,
            filetypes=filetypes
        )
        if not path:
            return
        try:
            img = self._cv_imread_unicode(path)
            if img is None:
                raise ValueError("Could not read image.")

            # Save state
            self.cv_image = img
            self.pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # Update config
            self.last_dir = os.path.dirname(path)
            save_config({"last_dir": self.last_dir})

            # Update UI
            self.path_label.configure(text=path)
            self._update_preview()

            # Share with root
            root = self.winfo_toplevel()
            root.cv_image_bgr = self.cv_image
            root.cv_image_rgb = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)

        except Exception as e:
            messagebox.showerror("Open Image Error", f"{e}")

    @staticmethod
    def _cv_imread_unicode(path):
        try:
            data = np.fromfile(path, dtype=np.uint8)
            return cv2.imdecode(data, cv2.IMREAD_COLOR)
        except Exception:
            return None

    def _update_preview(self):
        if self.pil_image is None:
            return
        w = max(1, self.preview.winfo_width())
        h = max(1, self.preview.winfo_height())

        img = self.pil_image.copy()
        img.thumbnail((w, h))

        self.ctk_image = CTkImage(light_image=img, dark_image=img, size=img.size)
        self.preview.configure(image=self.ctk_image, text="")

    def _redraw_preview(self, _event=None):
        if self.pil_image is not None:
            self._update_preview()
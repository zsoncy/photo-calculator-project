from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2
import os

class Open_Image_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        # Layout & theme
        self.grid_rowconfigure(0, weight=0)  # top bar
        self.grid_rowconfigure(1, weight=1)  # preview
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator - Open Image"

        # ---- State ----
        self.cv_image = None          # OpenCV image (BGR numpy array)
        self.pil_image = None         # PIL Image (RGB)
        self.ctk_image = None         # CTkImage for display
        self.last_dir = os.path.expanduser("~")

        # ---- Top bar ----
        top = CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="new", padx=24, pady=(24, 12))
        top.grid_columnconfigure(0, weight=0)
        top.grid_columnconfigure(1, weight=1)
        top.grid_columnconfigure(2, weight=0)

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

        back_btn = CTkButton(
            master=top, text="BACK",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24), corner_radius=50,
            command=lambda: root.slide_to_page("main", direction="right")
        )
        back_btn.grid(row=0, column=2)

        # ---- Preview area ----
        self.preview = CTkLabel(self, text="Preview will appear here", text_color="#370d40")
        self.preview.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.preview.bind("<Configure>", self._redraw_preview)

    # ---- Standard OS file dialog ----
    def open_image_dialog(self):
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("Bitmap", "*.bmp"),
            ("TIFF", "*.tiff;*.tif"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Open Image",
            initialdir=self.last_dir,
            filetypes=filetypes
        )
        if not path:
            return  # user canceled

        try:
            img = self._cv_imread_unicode(path)
            if img is None:
                raise ValueError("Could not read image (unsupported or corrupt).")

            # Save state
            self.cv_image = img
            self.pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            self.last_dir = os.path.dirname(path)
            self.path_label.configure(text=path)

            # Render preview
            self._update_preview()

            # If you want to share the image with other pages later:
            # root.cv_image = self.cv_image

            # TODO: plug Step 2 pipeline here or navigate to a processing/results page.

        except Exception as e:
            messagebox.showerror("Open Image Error", f"{e}")

    # ---- Unicode-safe OpenCV read ----
    @staticmethod
    def _cv_imread_unicode(path):
        """
        Robust loader for OpenCV that supports non-ASCII paths (Windows/macOS/Linux).
        """
        try:
            data = np.fromfile(path, dtype=np.uint8)
            return cv2.imdecode(data, cv2.IMREAD_COLOR)  # BGR
        except Exception:
            return None

    # ---- Preview rendering with aspect ratio ----
    def _update_preview(self):
        if self.pil_image is None:
            return
        w = max(1, self.preview.winfo_width())
        h = max(1, self.preview.winfo_height())

        img = self.pil_image.copy()
        img.thumbnail((w, h), Image.LANCZOS)

        # CTkImage for high-DPI + theme support; keep a reference!
        self.ctk_image = CTkImage(light_image=img, dark_image=img, size=img.size)
        self.preview.configure(image=self.ctk_image, text="")

    def _redraw_preview(self, _event=None):
        if self.pil_image is not None:
            self._update_preview()

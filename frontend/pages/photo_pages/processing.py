from customtkinter import *
from PIL import Image
import cv2

class Processing_Page(CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.configure(fg_color="#DDC3C3")
        self.title = "Photo Calculator - Processing"

        self.grid_rowconfigure(0, weight=0)  # navbar
        self.grid_rowconfigure(1, weight=0)  # controls
        self.grid_rowconfigure(2, weight=1)  # viewers
        self.grid_columnconfigure(0, weight=1)

        # ---------- Navbar ----------
        top = CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="new", padx=24, pady=(24, 12))
        top.grid_columnconfigure(0, weight=0)
        top.grid_columnconfigure(1, weight=0)
        top.grid_columnconfigure(2, weight=1)  # spacer to push controls row below

        back_btn = CTkButton(
            top, text="BACK",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24), corner_radius=50,
            command=lambda: root.slide_to_page("open_image", direction="right")
        )
        back_btn.grid(row=0, column=0, padx=(0, 12))

        calc_btn = CTkButton(
            top, text="Calculate",
            fg_color="#4e1d58", hover_color="#370d40", text_color="#DDC3C3",
            font=("Helvetica", 24), corner_radius=50,
            command=lambda: root.slide_to_page("operation", direction="left")  # change target if needed
        )
        calc_btn.grid(row=0, column=1)

        # ---------- Compact controls ----------
        controls = CTkFrame(self, fg_color="transparent")
        controls.grid(row=1, column=0, sticky="new", padx=24, pady=(0, 8))
        # Two columns: Size | C
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)

        size_col = CTkFrame(controls, fg_color="transparent")
        size_col.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.size_label = CTkLabel(size_col, text="size (s): 20", text_color="#370d40", font=("Helvetica", 16))
        self.size_label.pack(anchor="w")
        self.s_slider = CTkSlider(size_col, from_=0, to=50, number_of_steps=50, command=self._on_params_changed)
        self.s_slider.set(20)
        self.s_slider.pack(fill="x", pady=(4, 0))

        c_col = CTkFrame(controls, fg_color="transparent")
        c_col.grid(row=0, column=1, sticky="ew", padx=(12, 0))
        self.c_label = CTkLabel(c_col, text="c: 10", text_color="#370d40", font=("Helvetica", 16))
        self.c_label.pack(anchor="w")
        self.c_slider = CTkSlider(c_col, from_=0, to=100, number_of_steps=100, command=self._on_params_changed)
        self.c_slider.set(10)
        self.c_slider.pack(fill="x", pady=(4, 0))

        # ---------- Two viewers: Original ↔ Processed ----------
        center = CTkFrame(self, fg_color="transparent")
        center.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        center.grid_rowconfigure(0, weight=1)

        self.left = CTkLabel(center, text="Original", text_color="#370d40")
        self.right = CTkLabel(center, text="Processed", text_color="#370d40")
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self.left.bind("<Configure>", lambda e: self._redraw("left"))
        self.right.bind("<Configure>", lambda e: self._redraw("right"))

        # ---------- State ----------
        self.img_left = None    # PIL.Image
        self.img_right = None   # PIL.Image
        self.ctk_left = None
        self.ctk_right = None
        self._debounce_id = None

    # Called automatically by App after slide animation
    def on_show(self, root):
        """Load the image, set defaults, and run once automatically."""
        cv_rgb = getattr(root, "cv_image_rgb", None)
        cv_bgr = getattr(root, "cv_image_bgr", None)
        if cv_rgb is None or cv_bgr is None:
            self.img_left = None
            self.img_right = None
            self._redraw("left")
            self._redraw("right")
            return

        # Show original
        self.img_left = Image.fromarray(cv_rgb)
        self._redraw("left")

        # Choose a sensible default for s from image size (like your auto version)
        h, w = cv_bgr.shape[:2]
        k_auto = max(15, min(61, int(min(h, w) / 40) * 2 + 1))
        s_auto = max(0, min(50, (k_auto - 1) // 2))

        # Set sliders (this will also update labels via callback; we guard to avoid double compute)
        self.s_slider.set(s_auto)
        self.c_slider.set(10)
        self.size_label.configure(text=f"size (s): {int(self.s_slider.get())}")
        self.c_label.configure(text=f"c: {int(self.c_slider.get())}")

        # Run once with defaults
        self._run_pipeline()

    # ----- Slider change handler with tiny debounce -----
    def _on_params_changed(self, _value):
        # Update labels
        self.size_label.configure(text=f"size (s): {int(self.s_slider.get())}")
        self.c_label.configure(text=f"c: {int(self.c_slider.get())}")

        # Debounce reprocessing to keep UI smooth while dragging
        if self._debounce_id is not None:
            try:
                self.after_cancel(self._debounce_id)
            except Exception:
                pass
        self._debounce_id = self.after(60, self._run_pipeline)

    # ----- Minimal pipeline using ONLY the learned ops -----
    def _run_pipeline(self):
        self._debounce_id = None
        root = self.winfo_toplevel()
        cv_bgr = getattr(root, "cv_image_bgr", None)
        cv_rgb = getattr(root, "cv_image_rgb", None)
        if cv_bgr is None or cv_rgb is None:
            return

        gray = cv2.cvtColor(cv_bgr, cv2.COLOR_BGR2GRAY)

        # 1) Light denoise (median)
        gray = cv2.medianBlur(gray, 3)  # keep small; preserves strokes

        # 2) Adaptive threshold (MEAN_C, THRESH_BINARY) with user-controlled params
        s = int(round(self.s_slider.get()))
        c = int(round(self.c_slider.get()))
        block_size = max(2 * s + 1, 3)   # must be odd and >= 3

        bw = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size, c
        )

        # 3) Small morphology open (clean tiny noise)
        se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        bw_clean = cv2.morphologyEx(bw, cv2.MORPH_OPEN, se)

        # Update right viewer
        display = cv2.cvtColor(bw_clean, cv2.COLOR_GRAY2RGB)
        self.img_right = Image.fromarray(display)
        self._redraw("right")

        # Share outputs for next steps
        root.cv_pre_binary = bw_clean          # 0/255 (black text, white background)
        root.cv_pre_display = display          # RGB for UI

    # ----- Viewer redraw helpers -----
    def _redraw(self, which):
        target = self.left if which == "left" else self.right
        pil_img = self.img_left if which == "left" else self.img_right

        if pil_img is None:
            target.configure(image=None, text=("Original" if which == "left" else "Processed"))
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
        target.configure(image=ctk_img, text="")


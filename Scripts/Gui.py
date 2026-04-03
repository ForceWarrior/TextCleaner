import tkinter as tk
from tkinter import ttk

import Config
from .Pages.Cleaner_Page import build_cleaner_page
from .Pages.Settings_Page import build_settings_page
from .Pages.Help_Page import build_help_page


def create_app() -> tk.Tk:
    root = tk.Tk()
    root.title(Config.APP_TITLE)
    root.configure(bg=Config.BG_MAIN)
    root.resizable(True, True)
    root.minsize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    base_width = Config.WINDOW_WIDTH
    base_height = Config.WINDOW_HEIGHT
    current_scale = 1.0
    resize_job = None

    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    pos_x = int((screen_w - Config.WINDOW_WIDTH) / 2)
    pos_y = int((screen_h - Config.WINDOW_HEIGHT) / 3)
    default_geometry = f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{pos_x}+{pos_y}"

    root.geometry(Config.WINDOWED_GEOMETRY or default_geometry)

    style = ttk.Style()
    style.theme_use("clam")

    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    top_bar = tk.Frame(root, bg=Config.BG_MAIN)
    top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
    top_bar.columnconfigure(0, weight=1)

    def start_move(event):
        root._drag_offset_x = event.x_root - root.winfo_x()
        root._drag_offset_y = event.y_root - root.winfo_y()

    def do_move(event):
        if Config.WINDOW_MODE == "Fullscreen":
            return
        dx = getattr(root, "_drag_offset_x", 0)
        dy = getattr(root, "_drag_offset_y", 0)
        root.geometry(f"+{event.x_root - dx}+{event.y_root - dy}")

    top_bar.bind("<ButtonPress-1>", start_move)
    top_bar.bind("<B1-Motion>", do_move)

    title_label = ttk.Label(top_bar, text=Config.APP_TITLE)
    title_label.grid(row=0, column=0, sticky="w")

    tabs_frame = tk.Frame(top_bar, bg=Config.BG_MAIN)
    tabs_frame.grid(row=0, column=1, sticky="e", padx=(0, 4))

    exit_button = ttk.Button(
        top_bar,
        text="X",
        width=3,
        command=root.destroy,
        style="Exit.TButton",
        takefocus=False,
    )

    content = tk.Frame(root, bg=Config.BG_MAIN)
    content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    content.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=1)

    cleaner_page_data = build_cleaner_page(content, Config)
    settings_page_data = build_settings_page(content, Config)
    help_page_data = build_help_page(content, Config)

    pages = {
        "cleaner": cleaner_page_data["frame"],
        "settings": settings_page_data["frame"],
        "help": help_page_data["frame"],
    }

    for page in pages.values():
        page.grid(row=0, column=0, sticky="nsew")

    cleaner_tab = ttk.Button(tabs_frame, text="Text Cleaner", style="ActiveTab.TButton")
    cleaner_tab.grid(row=0, column=0, padx=(0, 4))

    settings_tab = ttk.Button(tabs_frame, text="Settings", style="Tab.TButton")
    settings_tab.grid(row=0, column=1, padx=(0, 4))

    help_tab = ttk.Button(tabs_frame, text="Help", style="Tab.TButton")
    help_tab.grid(row=0, column=2)

    tab_buttons = {
        "cleaner": cleaner_tab,
        "settings": settings_tab,
        "help": help_tab,
    }

    def set_active_tab(name: str) -> None:
        for tab_name, button in tab_buttons.items():
            button.configure(style="ActiveTab.TButton" if tab_name == name else "Tab.TButton")

    def show_page(name: str) -> None:
        pages[name].tkraise()
        set_active_tab(name)
        if name == "cleaner":
            cleaner_page_data["update_output"]()

    cleaner_tab.configure(command=lambda: show_page("cleaner"))
    settings_tab.configure(command=lambda: show_page("settings"))
    help_tab.configure(command=lambda: show_page("help"))

    def apply_styles() -> None:
        root.configure(bg=Config.BG_MAIN)
        top_bar.configure(bg=Config.BG_MAIN)
        tabs_frame.configure(bg=Config.BG_MAIN)
        content.configure(bg=Config.BG_MAIN)

        for page in pages.values():
            page.configure(bg=Config.BG_MAIN)

        style.configure(
            "TLabel",
            background=Config.BG_MAIN,
            foreground=Config.FG_LABEL,
            font=Config.FONT_UI,
        )

        style.configure(
            "Tab.TButton",
            background=Config.BG_MAIN,
            foreground=Config.FG_LABEL,
            font=Config.FONT_UI,
            relief="flat",
            padding=(10, 4),
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
        )
        style.map(
            "Tab.TButton",
            background=[("active", Config.ACCENT)],
            foreground=[("active", "#ffffff")],
        )

        style.configure(
            "ActiveTab.TButton",
            background=Config.ACCENT,
            foreground="#ffffff",
            font=Config.FONT_UI,
            relief="flat",
            padding=(10, 4),
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
        )
        style.map("ActiveTab.TButton", background=[], foreground=[])

        style.configure(
            "Action.TButton",
            background=Config.BG_TEXT,
            foreground=Config.FG_LABEL,
            font=Config.FONT_UI,
            relief="flat",
            padding=(8, 2),
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
        )
        style.map(
            "Action.TButton",
            background=[("active", "#101010"), ("pressed", "#080808")],
        )

        style.configure(
            "Exit.TButton",
            background=Config.BG_MAIN,
            foreground=Config.FG_LABEL,
            font=Config.FONT_UI_BOLD,
            relief="flat",
            padding=(6, 2),
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
        )
        style.map(
            "Exit.TButton",
            background=[("active", "#aa0000"), ("pressed", "#880000")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )

        style.configure(
            "TCheckbutton",
            background=Config.BG_PANEL,
            foreground=Config.FG_LABEL,
            font=Config.FONT_UI,
        )
        style.map(
            "TCheckbutton",
            background=[
                ("active", Config.BG_PANEL),
                ("selected", Config.BG_PANEL),
                ("!active", Config.BG_PANEL),
            ],
            foreground=[
                ("active", Config.FG_LABEL),
                ("selected", Config.FG_LABEL),
            ],
        )

        style.configure(
            "Settings.Vertical.TScrollbar",
            background=Config.BG_TEXT,
            troughcolor=Config.BG_MAIN,
            bordercolor=Config.BG_MAIN,
            arrowcolor=Config.FG_LABEL,
            relief="flat",
            width=14,
        )
        style.map(
            "Settings.Vertical.TScrollbar",
            background=[("active", "#333333")],
        )

        cp = cleaner_page_data
        cp["input_box"].configure(
            bg=Config.BG_TEXT,
            fg=Config.FG_TEXT,
            insertbackground=Config.FG_LABEL,
            font=Config.FONT_CODE,
        )
        cp["output_box"].configure(
            bg=Config.BG_TEXT,
            fg=Config.FG_TEXT,
            insertbackground=Config.FG_LABEL,
            font=Config.FONT_CODE,
        )
        cp["log_box"].configure(
            bg=Config.BG_TEXT,
            fg=Config.FG_TEXT,
            font=Config.FONT_CODE,
        )
        cp["stats_label"].configure(font=Config.FONT_UI)

        sp = settings_page_data
        sp["settings_canvas"].configure(bg=Config.BG_PANEL)
        sp["settings_inner"].configure(bg=Config.BG_PANEL)
        sp["scrollbar"].configure(style="Settings.Vertical.TScrollbar")

        hp = help_page_data
        hp["help_inner"].configure(bg=Config.BG_PANEL)
        hp["help_label"].configure(
            bg=Config.BG_PANEL,
            fg=Config.FG_TEXT,
            font=Config.FONT_UI,
        )

    def apply_window_mode() -> None:
        Config.WINDOW_MODE = settings_page_data["window_var"].get()

        if Config.WINDOW_MODE == "Fullscreen":
            root.overrideredirect(False)
            root.attributes("-fullscreen", True)
            exit_button.grid(row=0, column=2, sticky="e", padx=(4, 0))
        else:
            root.attributes("-fullscreen", False)
            root.overrideredirect(False)
            exit_button.grid_remove()
            root.geometry(Config.WINDOWED_GEOMETRY or default_geometry)

        Config.save_settings()

    def toggle_fullscreen(event=None):
        settings_page_data["window_var"].set(
            "Fullscreen" if Config.WINDOW_MODE == "Windowed" else "Windowed"
        )
        apply_window_mode()

    def on_font_change(event=None):
        settings_page_data["apply_font"]()
        apply_styles()
        cleaner_page_data["update_output"]()

    def on_theme_change(event=None):
        settings_page_data["apply_theme_choice"]()
        apply_styles()

    def on_normalize_flags_change():
        settings_page_data["apply_settings_flags"]()
        cleaner_page_data["update_output"]()

    settings_page_data["font_combo"].bind("<<ComboboxSelected>>", on_font_change)
    settings_page_data["theme_combo"].bind("<<ComboboxSelected>>", on_theme_change)
    settings_page_data["window_combo"].bind("<<ComboboxSelected>>", lambda e: apply_window_mode())

    for check in settings_page_data["norm_checks"]:
        check.configure(command=on_normalize_flags_change)

    def update_scaled_fonts():
        nonlocal current_scale

        width = max(root.winfo_width(), 1)
        height = max(root.winfo_height(), 1)

        scale_w = width / base_width
        scale_h = height / base_height
        scale = min(scale_w, scale_h)
        scale = max(1.0, min(scale, 1.6))

        if abs(scale - current_scale) < 0.05:
            return

        current_scale = scale

        ui_size = int(10 * current_scale)
        code_size = int(10 * current_scale)

        Config.FONT_UI = ("Segoe UI", ui_size)
        Config.FONT_UI_BOLD = ("Segoe UI", ui_size, "bold")
        Config.CODE_FONT_SIZE = code_size
        Config.FONT_CODE = (Config.CODE_FONT_NAME, Config.CODE_FONT_SIZE)

        apply_styles()

    def on_configure(event):
        nonlocal resize_job

        if event.widget is not root:
            return

        if Config.WINDOW_MODE == "Windowed":
            Config.WINDOWED_GEOMETRY = root.geometry()
            Config.save_settings()

        if resize_job is not None:
            root.after_cancel(resize_job)
        resize_job = root.after(60, update_scaled_fonts)

    def on_reset():
        settings_page_data["reset_defaults"]()
        apply_styles()
        apply_window_mode()
        cleaner_page_data["update_output"]()

    settings_page_data["reset_button"].configure(command=on_reset)

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Configure>", on_configure)

    handlers = {
        "open": cleaner_page_data["open_file"],
        "clear": cleaner_page_data["clear_text"],
        "copy": cleaner_page_data["handle_copy"],
        "update": cleaner_page_data["update_output"],
        "show_cleaner": lambda: show_page("cleaner"),
        "show_settings": lambda: show_page("settings"),
        "show_help": lambda: show_page("help"),
    }
    Config.bind_all(root, handlers)

    for sequence in ("<Control-v>", "<Control-V>", "<<Paste>>"):
        try:
            root.unbind_all(sequence)
        except tk.TclError:
            pass

    apply_styles()
    apply_window_mode()
    show_page("cleaner")
    cleaner_page_data["input_box"].focus_set()

    return root
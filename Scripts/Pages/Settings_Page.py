import tkinter as tk
from tkinter import ttk


def build_settings_page(parent, Config):
    page = tk.Frame(parent, bg=Config.BG_MAIN)
    page.grid(row=0, column=0, sticky="nsew")
    page.rowconfigure(0, weight=0)
    page.rowconfigure(1, weight=1)
    page.columnconfigure(0, weight=1)

    settings_title = ttk.Label(page, text="SETTINGS")
    settings_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

    settings_canvas = tk.Canvas(
        page,
        bg=Config.BG_PANEL,
        highlightthickness=0,
        borderwidth=0,
    )
    settings_canvas.grid(row=1, column=0, sticky="nsew")

    settings_scrollbar = ttk.Scrollbar(
        page,
        orient="vertical",
        command=settings_canvas.yview,
    )
    settings_scrollbar.grid(row=1, column=1, sticky="ns")

    settings_canvas.configure(yscrollcommand=settings_scrollbar.set)

    settings_inner = tk.Frame(settings_canvas, bg=Config.BG_PANEL)
    inner_window = settings_canvas.create_window((0, 0), window=settings_inner, anchor="nw")

    def _on_settings_configure(event):
        settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))

    settings_inner.bind("<Configure>", _on_settings_configure)

    def _on_canvas_configure(event):
        settings_canvas.itemconfig(inner_window, width=event.width)

    settings_canvas.bind("<Configure>", _on_canvas_configure)

    def _on_mousewheel(event):
        delta = int(-1 * (event.delta / 120))
        settings_canvas.yview_scroll(delta, "units")

    def _bind_mousewheel(event):
        settings_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_mousewheel(event):
        settings_canvas.unbind_all("<MouseWheel>")

    settings_inner.bind("<Enter>", _bind_mousewheel)
    settings_inner.bind("<Leave>", _unbind_mousewheel)

    group1_label = ttk.Label(settings_inner, text="Normalization groups")
    group1_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

    group1_desc = ttk.Label(
        settings_inner,
        text="Toggle which character groups are normalized.",
    )
    group1_desc.grid(row=1, column=0, sticky="w", pady=(0, 8))

    cyr_var = tk.BooleanVar(value=Config.ENABLE_CYRILLIC)
    greek_var = tk.BooleanVar(value=Config.ENABLE_GREEK)
    full_var = tk.BooleanVar(value=Config.ENABLE_FULLWIDTH)
    spec_var = tk.BooleanVar(value=Config.ENABLE_SPECIALS)

    cyr_check = ttk.Checkbutton(
        settings_inner, text="Cyrillic homoglyphs", variable=cyr_var
    )
    cyr_check.grid(row=2, column=0, sticky="w", pady=(0, 2))

    greek_check = ttk.Checkbutton(
        settings_inner, text="Greek / lookalike letters", variable=greek_var
    )
    greek_check.grid(row=3, column=0, sticky="w", pady=(0, 2))

    full_check = ttk.Checkbutton(
        settings_inner, text="Full‑width Latin characters", variable=full_var
    )
    full_check.grid(row=4, column=0, sticky="w", pady=(0, 2))

    spec_check = ttk.Checkbutton(
        settings_inner, text="Special characters / spaces", variable=spec_var
    )
    spec_check.grid(row=5, column=0, sticky="w", pady=(0, 2))

    font_group_label = ttk.Label(settings_inner, text="Editor font")
    font_group_label.grid(row=6, column=0, sticky="w", pady=(12, 4))

    font_desc = ttk.Label(
        settings_inner,
        text="Choose a monospaced font for the input and output editors.",
    )
    font_desc.grid(row=7, column=0, sticky="w", pady=(0, 6))

    font_var = tk.StringVar(value=Config.CODE_FONT_NAME)

    font_combo = ttk.Combobox(
        settings_inner,
        textvariable=font_var,
        values=Config.CODE_FONT_CHOICES,
        state="readonly",
        width=24,
    )
    font_combo.grid(row=8, column=0, sticky="w", pady=(0, 4))

    theme_group_label = ttk.Label(settings_inner, text="Theme")
    theme_group_label.grid(row=9, column=0, sticky="w", pady=(12, 4))

    theme_desc = ttk.Label(
        settings_inner,
        text="Switch between predefined color themes.",
    )
    theme_desc.grid(row=10, column=0, sticky="w", pady=(0, 6))

    theme_var = tk.StringVar(value=Config.CURRENT_THEME)

    theme_combo = ttk.Combobox(
        settings_inner,
        textvariable=theme_var,
        values=list(Config.THEMES.keys()),
        state="readonly",
        width=24,
    )
    theme_combo.grid(row=11, column=0, sticky="w", pady=(0, 4))

    win_label = ttk.Label(settings_inner, text="Window mode")
    win_label.grid(row=12, column=0, sticky="w", pady=(12, 4))

    win_desc = ttk.Label(
        settings_inner,
        text="Choose how the window is displayed.",
    )
    win_desc.grid(row=13, column=0, sticky="w", pady=(0, 6))

    window_var = tk.StringVar(value=Config.WINDOW_MODE)

    window_combo = ttk.Combobox(
        settings_inner,
        textvariable=window_var,
        values=["Windowed", "Fullscreen"],
        state="readonly",
        width=24,
    )
    window_combo.grid(row=14, column=0, sticky="w", pady=(0, 4))

    reset_button = ttk.Button(
        settings_inner,
        text="Reset settings to defaults",
    )
    reset_button.grid(row=15, column=0, sticky="w", pady=(12, 0))

    def apply_settings_flags() -> None:
        Config.ENABLE_CYRILLIC = bool(cyr_var.get())
        Config.ENABLE_GREEK = bool(greek_var.get())
        Config.ENABLE_FULLWIDTH = bool(full_var.get())
        Config.ENABLE_SPECIALS = bool(spec_var.get())
        Config.save_settings()

    def apply_font() -> None:
        name = font_var.get().strip()
        if not name:
            return
        Config.CODE_FONT_NAME = name
        Config.FONT_CODE = (Config.CODE_FONT_NAME, Config.CODE_FONT_SIZE)
        Config.save_settings()

    def apply_theme_choice() -> None:
        Config.CURRENT_THEME = theme_var.get()
        Config.apply_theme_constants()
        Config.save_settings()

    def reset_defaults() -> None:
        Config.CURRENT_THEME = "Dark"
        Config.CODE_FONT_NAME = "Consolas"
        Config.FONT_CODE = (Config.CODE_FONT_NAME, Config.CODE_FONT_SIZE)
        Config.ENABLE_CYRILLIC = True
        Config.ENABLE_GREEK = True
        Config.ENABLE_FULLWIDTH = True
        Config.ENABLE_SPECIALS = True
        Config.WINDOW_MODE = "Windowed"
        Config.WINDOWED_GEOMETRY = ""
        theme_var.set(Config.CURRENT_THEME)
        font_var.set(Config.CODE_FONT_NAME)
        window_var.set(Config.WINDOW_MODE)
        cyr_var.set(True)
        greek_var.set(True)
        full_var.set(True)
        spec_var.set(True)
        Config.apply_theme_constants()
        Config.save_settings()

    for chk in (cyr_check, greek_check, full_check, spec_check):
        chk.configure(command=apply_settings_flags)

    font_combo.bind("<<ComboboxSelected>>", lambda e: apply_font())
    theme_combo.bind("<<ComboboxSelected>>", lambda e: apply_theme_choice())
    reset_button.configure(command=reset_defaults)

    return {
        "frame": page,
        "settings_canvas": settings_canvas,
        "settings_inner": settings_inner,
        "scrollbar": settings_scrollbar,
        "cyr_var": cyr_var,
        "greek_var": greek_var,
        "full_var": full_var,
        "spec_var": spec_var,
        "font_var": font_var,
        "font_combo": font_combo,
        "theme_var": theme_var,
        "theme_combo": theme_combo,
        "window_var": window_var,
        "window_combo": window_combo,
        "reset_button": reset_button,
        "norm_checks": [
            cyr_check,
            greek_check,
            full_check,
            spec_check,
        ],
        "apply_settings_flags": apply_settings_flags,
        "apply_font": apply_font,
        "apply_theme_choice": apply_theme_choice,
        "reset_defaults": reset_defaults,
    }
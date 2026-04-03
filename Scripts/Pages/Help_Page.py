import tkinter as tk
from tkinter import ttk


def build_help_page(parent, Config):
    page = tk.Frame(parent, bg=Config.BG_MAIN)
    page.grid(row=0, column=0, sticky="nsew")
    page.rowconfigure(0, weight=0)
    page.rowconfigure(1, weight=1)
    page.columnconfigure(0, weight=1)

    help_title = ttk.Label(page, text="HELP")
    help_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

    help_inner = tk.Frame(page, bg=Config.BG_PANEL)
    help_inner.grid(row=1, column=0, sticky="nsew")
    help_inner.columnconfigure(0, weight=1)

    help_text = (
        "Text Cleaner normalizes suspicious Unicode characters.\n\n"
        "Text Cleaner tab:\n"
        "- Paste, type, or open a .txt file.\n"
        "- Cleaned version appears below with stats and a changes log.\n\n"
        "Settings tab:\n"
        "- Toggle normalization groups (Cyrillic, Greek, etc.).\n"
        "- Change editor font and theme.\n"
        "- Switch window mode (Windowed/Fullscreen).\n\n"
        "Keyboard shortcuts:\n"
        "- Ctrl+O: Open file\n"
        "- Ctrl+L: Clear\n"
        "- Ctrl+Shift+C: Copy cleaned\n"
        "- Ctrl+1/2/3: Switch tabs\n"
        "- Ctrl+Q or Esc: Quit"
    )

    help_label = tk.Label(
        help_inner,
        text=help_text,
        bg=Config.BG_PANEL,
        fg=Config.FG_TEXT,
        font=Config.FONT_UI,
        justify="left",
        wraplength=700,
        anchor="nw",
    )
    help_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    return {
        "frame": page,
        "help_inner": help_inner,
        "help_label": help_label,
    }
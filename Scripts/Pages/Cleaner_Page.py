import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ..Cleaner import normalize


def build_cleaner_page(parent, Config):
    frame = tk.Frame(parent, bg=Config.BG_MAIN)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(5, weight=1)
    frame.columnconfigure(0, weight=1)

    header_input = tk.Frame(frame, bg=Config.BG_MAIN)
    header_input.grid(row=0, column=0, sticky="ew")
    header_input.columnconfigure(0, weight=1)

    input_label = ttk.Label(header_input, text="Paste your text here:")
    input_label.grid(row=0, column=0, sticky="w")

    paste_button = ttk.Button(header_input, text="Paste")
    paste_button.grid(row=0, column=1, padx=(8, 0))

    clear_button = ttk.Button(header_input, text="Clear")
    clear_button.grid(row=0, column=2, padx=(4, 0))

    open_button = ttk.Button(header_input, text="Open .txt")
    open_button.grid(row=0, column=3, padx=(4, 0))

    input_box = tk.Text(
        frame,
        height=8,
        bg=Config.BG_TEXT,
        fg=Config.FG_TEXT,
        insertbackground=Config.FG_LABEL,
        font=Config.FONT_CODE,
        wrap="word",
        relief="flat",
        bd=1,
    )
    input_box.grid(row=2, column=0, sticky="nsew", pady=(4, 8))

    header_frame = tk.Frame(frame, bg=Config.BG_MAIN)
    header_frame.grid(row=3, column=0, sticky="ew", pady=(4, 0))
    header_frame.columnconfigure(0, weight=1)

    output_label = ttk.Label(header_frame, text="Cleaned text:")
    output_label.grid(row=0, column=0, sticky="w")

    copy_button = ttk.Button(header_frame, text="Copy")
    copy_button.grid(row=0, column=1, sticky="e")

    output_box = tk.Text(
        frame,
        height=8,
        bg=Config.BG_TEXT,
        fg=Config.FG_TEXT,
        insertbackground=Config.FG_LABEL,
        font=Config.FONT_CODE,
        wrap="word",
        relief="flat",
        bd=1,
        state=tk.DISABLED,
    )
    output_box.grid(row=5, column=0, sticky="nsew", pady=(4, 0))

    stats_frame = tk.Frame(frame, bg=Config.BG_MAIN)
    stats_frame.grid(row=6, column=0, sticky="ew", pady=(8, 0))

    stats_label = ttk.Label(stats_frame, text="Chars: 0   Words: 0   Replacements: 0")
    stats_label.pack(anchor="w", pady=(0, 4))

    log_label = ttk.Label(stats_frame, text="Changes log:")
    log_label.pack(anchor="w")

    log_box = tk.Text(
        stats_frame,
        height=4,
        bg=Config.BG_TEXT,
        fg=Config.FG_TEXT,
        font=Config.FONT_CODE,
        wrap="word",
        relief="flat",
        state=tk.DISABLED,
    )
    log_box.pack(fill="x", pady=(2, 0))

    def update_output() -> None:
        text = input_box.get("1.0", tk.END).strip()
        output_box.config(state=tk.NORMAL)

        if not text:
            output_box.delete("1.0", tk.END)
            output_box.config(state=tk.DISABLED)
            stats_label.config(text="Chars: 0   Words: 0   Replacements: 0")
            log_box.config(state=tk.NORMAL)
            log_box.delete("1.0", tk.END)
            log_box.config(state=tk.DISABLED)
            return

        cleaned, changes = normalize(text)

        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", cleaned)
        output_box.config(state=tk.DISABLED)

        char_count = len(cleaned)
        word_count = len(cleaned.split())
        rep_count = len(changes)
        stats_label.config(
            text=f"Chars: {char_count}   Words: {word_count}   Replacements: {rep_count}"
        )

        log_box.config(state=tk.NORMAL)
        log_box.delete("1.0", tk.END)
        if changes:
            log_box.insert("1.0", "\n".join(changes[:20]))
            if len(changes) > 20:
                log_box.insert("end", f"\n... and {len(changes)-20} more")
        else:
            log_box.insert("1.0", "No replacements made.")
        log_box.config(state=tk.DISABLED)

    def handle_paste(event=None) -> None:
        try:
            clip = frame.clipboard_get()
        except tk.TclError:
            clip = ""
        if clip:
            input_box.delete("1.0", tk.END)
            input_box.insert("1.0", clip)
        update_output()

    def handle_key_release(event=None) -> None:
        update_output()

    def handle_copy() -> None:
        cleaned = output_box.get("1.0", tk.END).strip()
        if not cleaned:
            return
        frame.clipboard_clear()
        frame.clipboard_append(cleaned)

    def clear_text() -> None:
        input_box.delete("1.0", tk.END)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.config(state=tk.DISABLED)
        stats_label.config(text="Chars: 0   Words: 0   Replacements: 0")
        log_box.config(state=tk.NORMAL)
        log_box.delete("1.0", tk.END)
        log_box.config(state=tk.DISABLED)

    def open_file() -> None:
        path = filedialog.askopenfilename(
            title="Open text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            return
        input_box.delete("1.0", tk.END)
        input_box.insert("1.0", content)
        update_output()

    input_box.bind("<KeyRelease>", handle_key_release)
    input_box.bind("<<Paste>>", lambda e: handle_paste())

    copy_button.configure(command=handle_copy)
    paste_button.configure(command=handle_paste)
    clear_button.configure(command=clear_text)
    open_button.configure(command=open_file)

    return {
        "frame": frame,
        "input_box": input_box,
        "output_box": output_box,
        "stats_label": stats_label,
        "log_box": log_box,
        "update_output": update_output,
        "handle_copy": handle_copy,
        "clear_text": clear_text,
        "open_file": open_file,
    }
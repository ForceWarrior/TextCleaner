from pathlib import Path
import json


# App / paths

APP_TITLE = "Text Cleaner"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
DATA_DIR.mkdir(exist_ok=True)
SETTINGS_FILE = DATA_DIR / "settings.json"


# Typography / spacing

FONT_UI = ("Segoe UI", 10)
FONT_UI_BOLD = ("Segoe UI", 10, "bold")

DEFAULT_CODE_FONT_NAME = "Consolas"
CODE_FONT_SIZE = 10
CODE_FONT_CHOICES = [
    "Consolas",
    "Cascadia Code",
    "Fira Code",
    "JetBrains Mono",
    "Courier New",
]

PADDING_X = 20
PADDING_Y = 20


# Themes

THEMES = {
    "Carbon": {
        "BG_MAIN": "#121212",
        "BG_TEXT": "#1e1e1e",
        "BG_PANEL": "#181818",
        "FG_TEXT": "#e0e0e0",
        "FG_LABEL": "#ffffff",
        "ACCENT": "#3a86ff",
        "BORDER_COLOR": "#2c2c2c",
    },
    "Ember": {
        "BG_MAIN": "#161311",
        "BG_TEXT": "#211c19",
        "BG_PANEL": "#1b1613",
        "FG_TEXT": "#e7ddd6",
        "FG_LABEL": "#fff7f2",
        "ACCENT": "#cb4b16",
        "BORDER_COLOR": "#3a2c24",
    },
    "Solarized Dark": {
        "BG_MAIN": "#002b36",
        "BG_TEXT": "#073642",
        "BG_PANEL": "#002b36",
        "FG_TEXT": "#93a1a1",
        "FG_LABEL": "#fdf6e3",
        "ACCENT": "#268bd2",
        "BORDER_COLOR": "#586e75",
    },
    "Light": {
        "BG_MAIN": "#f2f2f2",
        "BG_TEXT": "#ffffff",
        "BG_PANEL": "#e5e5e5",
        "FG_TEXT": "#222222",
        "FG_LABEL": "#000000",
        "ACCENT": "#0078d7",
        "BORDER_COLOR": "#cccccc",
    },
}

CURRENT_THEME = "Carbon"

BG_MAIN = THEMES[CURRENT_THEME]["BG_MAIN"]
BG_TEXT = THEMES[CURRENT_THEME]["BG_TEXT"]
BG_PANEL = THEMES[CURRENT_THEME]["BG_PANEL"]
FG_TEXT = THEMES[CURRENT_THEME]["FG_TEXT"]
FG_LABEL = THEMES[CURRENT_THEME]["FG_LABEL"]
ACCENT = THEMES[CURRENT_THEME]["ACCENT"]
BORDER_COLOR = THEMES[CURRENT_THEME]["BORDER_COLOR"]


def apply_theme_constants():
    global BG_MAIN, BG_TEXT, BG_PANEL, FG_TEXT, FG_LABEL, ACCENT, BORDER_COLOR

    theme = THEMES.get(CURRENT_THEME, THEMES["Carbon"])
    BG_MAIN = theme["BG_MAIN"]
    BG_TEXT = theme["BG_TEXT"]
    BG_PANEL = theme["BG_PANEL"]
    FG_TEXT = theme["FG_TEXT"]
    FG_LABEL = theme["FG_LABEL"]
    ACCENT = theme["ACCENT"]
    BORDER_COLOR = theme["BORDER_COLOR"]


# Cleaner feature flags

ENABLE_CYRILLIC = True
ENABLE_GREEK = True
ENABLE_FULLWIDTH = True
ENABLE_SPECIALS = True


# Window state

WINDOW_MODE = "Windowed"   # "Windowed" or "Fullscreen"
WINDOWED_GEOMETRY = ""


# Editor / code font

CODE_FONT_NAME = DEFAULT_CODE_FONT_NAME
FONT_CODE = (CODE_FONT_NAME, CODE_FONT_SIZE)


# Settings

def load_settings():
    global CURRENT_THEME, CODE_FONT_NAME
    global ENABLE_CYRILLIC, ENABLE_GREEK, ENABLE_FULLWIDTH, ENABLE_SPECIALS
    global WINDOW_MODE, WINDOWED_GEOMETRY

    if not SETTINGS_FILE.exists():
        return

    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return

    CURRENT_THEME = data.get("theme", CURRENT_THEME)
    if CURRENT_THEME not in THEMES:
        CURRENT_THEME = "Carbon"

    CODE_FONT_NAME = data.get("code_font", CODE_FONT_NAME)
    if CODE_FONT_NAME not in CODE_FONT_CHOICES:
        CODE_FONT_NAME = DEFAULT_CODE_FONT_NAME

    ENABLE_CYRILLIC = data.get("enable_cyrillic", ENABLE_CYRILLIC)
    ENABLE_GREEK = data.get("enable_greek", ENABLE_GREEK)
    ENABLE_FULLWIDTH = data.get("enable_fullwidth", ENABLE_FULLWIDTH)
    ENABLE_SPECIALS = data.get("enable_specials", ENABLE_SPECIALS)

    WINDOW_MODE = data.get("window_mode", WINDOW_MODE)
    WINDOWED_GEOMETRY = data.get("windowed_geometry", WINDOWED_GEOMETRY)


def save_settings():
    data = {
        "theme": CURRENT_THEME,
        "code_font": CODE_FONT_NAME,
        "enable_cyrillic": ENABLE_CYRILLIC,
        "enable_greek": ENABLE_GREEK,
        "enable_fullwidth": ENABLE_FULLWIDTH,
        "enable_specials": ENABLE_SPECIALS,
        "window_mode": WINDOW_MODE,
        "windowed_geometry": WINDOWED_GEOMETRY,
    }

    SETTINGS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

# Shortcuts

def bind_all(root, handlers):
    root.bind_all("<Control-q>", lambda e: (print("Ctrl-q"), root.destroy()))

    root.bind_all("<Control-o>", lambda e: (print("Ctrl-o"), handlers["open"]()))
    root.bind_all("<Return>",    lambda e: (print("Return"), handlers["update"]()))

    root.bind_all("<Control-Key-1>", lambda e: (print("Ctrl-1"), handlers["show_cleaner"]()))
    root.bind_all("<Control-Key-2>", lambda e: (print("Ctrl-2"), handlers["show_settings"]()))
    root.bind_all("<Control-Key-3>", lambda e: (print("Ctrl-3"), handlers["show_help"]()))

# Initialize derived values

load_settings()
FONT_CODE = (CODE_FONT_NAME, CODE_FONT_SIZE)
apply_theme_constants()
# TextCleaner

TextCleaner is a small app built with Python and Tkinter for cleaning copied text, normalizing homoglyphs, and removing invisible or misleading Unicode characters.

## Features

- Cleans pasted text quickly
- Normalizes common Cyrillic homoglyphs
- Normalizes common Greek homoglyphs
- Converts fullwidth Latin letters and digits
- Removes invisible and special Unicode formatting characters
- Shows cleaned output and change details
- Includes a Windows executable build

## Download

If you just want to use the app, download the latest `.exe` from the **Releases** page.

## Run from source

### Requirements

- Python 3.10+
- Windows recommended

### Start the app

```bash
python Main.py
```

## Build the EXE

This project uses PyInstaller.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name TextCleaner.py
```

The built executable will be created in:

```text
dist/TextCleaner.exe
```

## Project structure

```text
TextCleaner/
├── Main.py
├── Config.py
├── Scripts/
│   ├── Cleaner.py
│   ├── Gui.py
│   └── Pages/
└── Data/
```

## What it cleans

TextCleaner is designed to handle things like:

- Zero-width characters
- Special spacing characters
- Fullwidth text
- Common Greek and Cyrillic lookalikes
- Other copied text junk that can break chat messages, formatting, or readability

## Notes

- AI assistance was used

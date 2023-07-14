import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
from tkinter.ttk import Scrollbar, Notebook
import pkg_resources

# Define the default theme colors for light mode
default_bg = "#ffffff"
default_fg = "#000000"
default_highlight_bg = "#f0f0f0"
default_highlight_fg = "#000000"

# Define the dark theme colors
dark_bg = "#1c1c1c"
dark_fg = "#f0f0f0"
dark_highlight_bg = "#333333"
dark_highlight_fg = "#ffffff"

# Variable to track the current theme mode
dark_mode = False

current_folder_path = ""


def toggle_theme():
    global dark_mode

    if dark_mode:
        # Switch to light mode
        root.configure(bg=default_bg)
        root.option_add("*Background", default_bg)
        root.option_add("*Foreground", default_fg)
        root.option_add("*TEntry.Background", default_bg)
        root.option_add("*TEntry.Foreground", default_fg)
        root.option_add("*TEntry.HighlightBackground", default_highlight_bg)
        root.option_add("*TEntry.HighlightColor", default_highlight_fg)
        dark_mode = False
    else:
        # Switch to dark mode
        root.configure(bg=dark_bg)
        root.option_add("*Background", dark_bg)
        root.option_add("*Foreground", dark_fg)
        root.option_add("*TEntry.Background", dark_bg)
        root.option_add("*TEntry.Foreground", dark_fg)
        root.option_add("*TEntry.HighlightBackground", dark_highlight_bg)
        root.option_add("*TEntry.HighlightColor", dark_highlight_fg)
        dark_mode = True


def create_file():
    global current_folder_path

    file_name = simpledialog.askstring("Create New File", "Enter the name of the file:")
    if file_name:
        file_path = f"{current_folder_path}/{file_name}"
        with open(file_path, "w") as file:
            file.write('print("PyIDE by Sahil Thakur")')

        # Update file list
        file_list.insert(tk.END, file_name)


root = tk.Tk()
root.title("Python Compiler")
root.geometry("800x600")

# Create the toolbar frame
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

# Compile Button
compile_button = tk.Button(toolbar_frame, text="Compile")
compile_button.pack(side=tk.LEFT, padx=5)

# Save Button
save_button = tk.Button(toolbar_frame, text="Save")
save_button.pack(side=tk.LEFT, padx=5)

# Dark Mode Button
dark_mode_button = tk.Button(toolbar_frame, text="Dark Mode", command=toggle_theme)
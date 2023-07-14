import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
from tkinter.ttk import Scrollbar, Notebook


def compile_code():
    current_tab_index = notebook.index(notebook.select())
    code_text_widget = code_text_widgets[current_tab_index]
    code = code_text_widget.get("1.0", tk.END).strip()
    if code:
        try:
            process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, error = process.communicate()
            output_text.configure(state="normal")
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, output)
            output_text.configure(state="disabled")
            if error:
                messagebox.showerror("Error", error)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "No code to compile!")


def open_folder():
    global current_folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_list.delete(0, tk.END)  # Clear the file list
        for file_name in os.listdir(folder_path):
            file_list.insert(tk.END, file_name)
        current_folder_path = folder_path


def open_file(event=None):
    selection = file_list.curselection()
    if selection:
        file_name = file_list.get(selection[0])
        file_path = os.path.join(current_folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                code = file.read()
                create_new_tab(file_path, code)


def save_file():
    current_tab_index = notebook.index(notebook.select())
    code_text_widget = code_text_widgets[current_tab_index]
    current_file_path = tab_file_paths[current_tab_index]
    if current_file_path:
        with open(current_file_path, "w") as file:
            code = code_text_widget.get("1.0", tk.END).strip()
            file.write(code)
    else:
        save_as_file()


def save_as_file():
    current_tab_index = notebook.index(notebook.select())
    initial_file_path = tab_file_paths[current_tab_index]
    file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")], initialfile=initial_file_path)
    if file_path:
        with open(file_path, "w") as file:
            code_text_widget = code_text_widgets[current_tab_index]
            code = code_text_widget.get("1.0", tk.END).strip()
            file.write(code)
        notebook.tab(current_tab_index, text=os.path.basename(file_path))
        tab_file_paths[current_tab_index] = file_path


def create_new_file():
    global current_folder_path

    if current_folder_path:
        new_file_name = simpledialog.askstring("Create New File", "Enter the name of the new file:")
        if new_file_name:
            new_file_path = os.path.join(current_folder_path, new_file_name)
            if not os.path.exists(new_file_path):
                with open(new_file_path, "w") as file:
                    file.write('print("PyIDE By Sahil Thakur")')
                file_list.insert(tk.END, new_file_name)
                file_list.selection_clear(0, tk.END)
                file_list.selection_set(tk.END)
                open_file()
                messagebox.showinfo("File Created", f"The file '{new_file_name}' has been created.")
            else:
                messagebox.showwarning("File Already Exists", "A file with the same name already exists in the folder.")
        else:
            messagebox.showwarning("File Name Not Provided", "Please enter a valid file name.")
    else:
        messagebox.showwarning("Folder Not Selected", "Please open a folder using the 'Open Folder' button.")


def create_new_tab(file_path=None, code=""):
    tab_frame = tk.Frame(notebook)
    notebook.add(tab_frame)

    if file_path:
        tab_title = os.path.basename(file_path)
    else:
        tab_title = "Untitled"

    close_button = tk.Button(tab_frame, text="X", command=close_tab, bg="red", fg="white")
    close_button.pack(side=tk.RIGHT, padx=(0, 5))

    code_frame = tk.Frame(tab_frame)
    code_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    code_label = tk.Label(code_frame, text="Code Area")
    code_label.pack(side=tk.TOP, pady=(0, 10))

    code_text = tk.Text(code_frame, font=("Courier New", 12), height=20, width=80)
    code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    code_text.insert(tk.END, code)

    code_scroll = Scrollbar(code_frame, command=code_text.yview)
    code_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    code_text.configure(yscrollcommand=code_scroll.set)

    notebook.tab(notebook.index(tab_frame), text=tab_title)
    notebook.select(tab_frame)

    code_text_widgets.append(code_text)

    tab_file_paths.append(file_path)


def close_tab():
    current_tab_index = notebook.index(notebook.select())
    if current_tab_index >= 0:
        notebook.forget(current_tab_index)
        code_text_widgets.pop(current_tab_index)
        tab_file_paths.pop(current_tab_index)


root = tk.Tk()
root.title("Python Compiler")

# Create the toolbar frame
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

# Compile Button
compile_button = tk.Button(toolbar_frame, text="Compile", command=compile_code)
compile_button.pack(side=tk.LEFT, padx=5)

# Save Button
save_button = tk.Button(toolbar_frame, text="Save", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

# Save As Button
save_as_button = tk.Button(toolbar_frame, text="Save As", command=save_as_file)
save_as_button.pack(side=tk.LEFT, padx=5)

# Open Folder Button
open_folder_button = tk.Button(toolbar_frame, text="Open Folder", command=open_folder)
open_folder_button.pack(side=tk.LEFT, padx=5)

# Create New File Button
create_file_button = tk.Button(toolbar_frame, text="Create New File", command=create_new_file)
create_file_button.pack(side=tk.LEFT, padx=5)

# Create the main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the sidebar frame
sidebar_frame = tk.Frame(main_frame, width=200)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# Create the file list
file_list = tk.Listbox(sidebar_frame, font=("Courier New", 12))
file_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
file_list.bind("<Double-Button-1>", open_file)

# Create the code editor frame
code_frame = tk.Frame(main_frame)
code_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

notebook = Notebook(code_frame)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

code_text_widgets = []
tab_file_paths = []

# Create the output area
output_frame = tk.Frame(root)
output_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10)

output_label = tk.Label(output_frame, text="Output Area")
output_label.pack(side=tk.TOP, pady=(10, 5))

output_text = tk.Text(output_frame, font=("Courier New", 12), height=5)
output_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

output_scroll = Scrollbar(output_frame, command=output_text.yview)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
output_text.configure(yscrollcommand=output_scroll.set)

current_folder_path = ""

root.mainloop()
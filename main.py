import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
from threading import Thread
from tkinter.ttk import Progressbar, Scrollbar
import pkg_resources
from tqdm import tqdm


def compile_code():
    code = code_text.get("1.0", tk.END).strip()
    if code:
        try:
            process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, error = process.communicate()
            output_text.configure(state="normal")  # Enable editing temporarily
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, output)
            output_text.configure(state="disabled")  # Disable editing again
            if error:
                messagebox.showerror("Error", error)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "No code to compile!")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, code)


def save_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "w") as file:
            code = code_text.get("1.0", tk.END).strip()
            file.write(code)


def install_package_thread(package_name, progress_window, progress_bar, progress_speed_label):
    try:
        process = subprocess.Popen(['pip', 'install', package_name], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        progress_bar["value"] = 0
        progress_speed_label.config(text="")

        while process.poll() is None:
            output = process.stdout.readline().strip()
            if output:
                if "Installing" in output:
                    progress_bar["value"] = 0
                elif "Successfully installed" in output:
                    progress_bar["value"] = 100
                elif "Collecting" in output:
                    collected = output.split("Collecting ")[-1]
                    total = len(collected.split("/"))
                    progress_bar["value"] = int((total / 100) * 80)
                elif "Installing collected" in output:
                    progress_bar["value"] = 90

        progress_window.destroy()

        output, _ = process.communicate()
        if output:
            messagebox.showinfo("Installation Output", output)
        else:
            messagebox.showinfo("Installation Complete", f"The package '{package_name}' is installed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def install_package():
    package_name = simpledialog.askstring("Install Package", "Enter the name of the Python package to install:")
    if package_name:
        package_found = package_name in [dist.key for dist in pkg_resources.working_set]
        if package_found:
            messagebox.showinfo("Package Already Installed", f"The package '{package_name}' is already installed.")
            return

        progress_window = tk.Toplevel(root)
        progress_window.title("Installing Package")
        progress_window.geometry("300x100")

        progress_bar = Progressbar(progress_window, length=200, mode="determinate")
        progress_bar.pack(pady=10)

        progress_speed = tk.Label(progress_window, text="")
        progress_speed.pack(pady=5)

        install_thread = Thread(target=install_package_thread,
                                args=(package_name, progress_window, progress_bar, progress_speed))
        install_thread.start()


def show_installed_packages():
    installed_packages = [dist.key for dist in pkg_resources.working_set]

    package_list_window = tk.Toplevel(root)
    package_list_window.title("Installed Packages")
    package_list_window.geometry("300x200")

    package_list_text = tk.Text(package_list_window, font=("Courier New", 12))
    package_list_text.pack(fill=tk.BOTH, expand=True)

    package_list_scroll = Scrollbar(package_list_window)
    package_list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    package_list_text.config(yscrollcommand=package_list_scroll.set)
    package_list_scroll.config(command=package_list_text.yview)

    for package in installed_packages:
        package_list_text.insert(tk.END, package + "\n")

    package_list_text.configure(state="disabled")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


root = tk.Tk()
root.title("Python Compiler")
root.attributes("-fullscreen", False)  # Open in full-screen mode
root.title("pyIDE @geeksahil")
photo = tk.PhotoImage(file = "logo.png")
root.iconphoto(False,photo)
# Create the toolbar
toolbar = tk.Frame(root)
toolbar.pack(side=tk.TOP, padx=10, pady=10)

open_button = tk.Button(toolbar, text="Open", command=open_file)
open_button.pack(side=tk.LEFT)

save_button = tk.Button(toolbar, text="Save", command=save_file)
save_button.pack(side=tk.LEFT)

compile_button = tk.Button(toolbar, text="Compile", command=compile_code)
compile_button.pack(side=tk.LEFT)

install_button = tk.Button(toolbar, text="Install Package", command=install_package)
install_button.pack(side=tk.LEFT)

show_packages_button = tk.Button(toolbar, text="Show Installed Packages", command=show_installed_packages)
show_packages_button.pack(side=tk.LEFT)

# Create the code editor
code_text = tk.Text(root, font=("Courier New", 12))
code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)

code_scroll = Scrollbar(root, command=code_text.yview)
code_scroll.pack(side=tk.RIGHT, fill=tk.Y)
code_text.configure(yscrollcommand=code_scroll.set)

# Create the output frame
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_text = tk.Text(output_frame, font=("Courier New", 12), state="disabled")
output_text.pack(fill=tk.BOTH, expand=True)

output_scroll = Scrollbar(output_frame, command=output_text.yview)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
output_text.configure(yscrollcommand=output_scroll.set)

# Configure invisible scrollbars
code_scroll.configure(orient="vertical", command=code_text.yview)
output_scroll.configure(orient="vertical", command=output_text.yview)

# Create the project label
project_label = tk.Label(root, text="Project by GeekSahil", font=("Arial", 10))
project_label.pack(side=tk.BOTTOM, pady=10)

# Minimize and Close buttons
minimize_button = tk.Button(root, text="Minimize", command=root.iconify)
minimize_button.pack(side=tk.RIGHT)

close_button = tk.Button(root, text="Close", command=on_closing)
close_button.pack(side=tk.RIGHT)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

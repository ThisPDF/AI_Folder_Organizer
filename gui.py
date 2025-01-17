import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ctypes
from pathlib import Path
from app import *
from settings import load_settings, save_settings
import threading
from PIL import Image, ImageTk  # Import Pillow modules

# Initialize settings
settings = load_settings()

# GUI Class
class FolderOrganizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Folder Organizer")
        self.geometry("600x500")

        # Determine the icon path dynamically
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "app_icon.ico")  # Bundled EXE environment
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")  # Development environment

        # Set the window icon
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            print(f"Icon file not found: {icon_path}")

        # Apply the theme before creating widgets
        self.configure_gui()
        self.create_widgets()
        self.apply_theme()  # Apply theme after widgets are created

        # Set the taskbar icon
        self.after(0, self.set_app_taskbar_icon, icon_path)

    def set_app_taskbar_icon(self, icon_path):
        if sys.platform.startswith('win') and os.path.exists(icon_path):
            icon_flags = 0x00000010  # LR_LOADFROMFILE flag for loading icons
            hicon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, icon_flags)
            if hicon:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)
            else:
                print("Failed to load icon for taskbar.")
        else:
            print("Platform is not Windows or icon path does not exist.")

    def configure_gui(self):
        # Set initial theme based on settings
        if settings["theme"] == "dark":
            self.configure(bg="#2e2e2e")
        else:
            self.configure(bg="#ffffff")

    def apply_theme(self):
        # Colors based on the theme
        is_dark_mode = settings["theme"] == "dark"
        bg_color = "#2e2e2e" if is_dark_mode else "#ffffff"
        fg_color = "#ffffff" if is_dark_mode else "#000000"
        accent_color = "#76c7c0" if is_dark_mode else "#0078d4"  # Accent color for dark/light mode

        # Set the background color of the main window
        self.configure(bg=bg_color)

        # Create and configure a style object for ttk widgets
        style = ttk.Style()
        style.theme_use("clam")

        # Apply specific styles for each ttk widget type
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
        style.configure("TRadiobutton", background=bg_color, foreground=fg_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background=bg_color, foreground=fg_color)
        style.configure("TProgressbar", troughcolor=bg_color, background=accent_color)
        style.configure("TButton", background=accent_color, foreground=fg_color)

        # Ensure that `tk` widgets are also updated
        self.update_widgets_theme(self, bg_color, fg_color)

    def update_widgets_theme(self, parent, bg_color, fg_color):
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Widget):
                try:
                    widget.configure(bg=bg_color, fg=fg_color)
                except tk.TclError:
                    pass
            # Recursively apply theme to child widgets
            self.update_widgets_theme(widget, bg_color, fg_color)

    def create_widgets(self):
        # Tab control
        self.tab_control = ttk.Notebook(self)
        self.main_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)

        # Add tabs
        self.tab_control.add(self.main_tab, text="Organizer")
        self.tab_control.add(self.settings_tab, text="Settings")
        self.tab_control.pack(expand=1, fill="both")

        # Organizer Tab
        self.create_main_tab_widgets()

        # Settings Tab
        self.create_settings_tab_widgets()

    def create_main_tab_widgets(self):
        # Folder selection
        ttk.Label(self.main_tab, text="Select Folder to Organize:").pack(pady=5)
        self.folder_var = tk.StringVar()
        ttk.Entry(self.main_tab, textvariable=self.folder_var, width=40).pack(pady=5)
        ttk.Button(self.main_tab, text="Browse", command=self.browse_folder).pack(pady=5)

        # Learning paths
        ttk.Label(self.main_tab, text="Select Directories to Learn Patterns From:").pack(pady=10)

        # Replace Listbox with Treeview
        self.tree = ttk.Treeview(self.main_tab, columns=("path"), show='headings', height=5)
        self.tree.heading("path", text="Paths")
        self.tree.column("path", width=450)
        self.tree.pack(pady=5)

        button_frame = ttk.Frame(self.main_tab)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Add Directory", command=self.add_learning_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_learning_path).pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_tab, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, fill="x", padx=20)

        # Status label for training progress
        self.status_var = tk.StringVar()
        ttk.Label(self.main_tab, textvariable=self.status_var, font=("Arial", 10)).pack(pady=5)

        # Organize button with specific width and padding
        ttk.Button(self.main_tab, text="Start Organizing", command=self.start_organizing, width=20).pack(pady=20, padx=20)

    def create_settings_tab_widgets(self):
        # Theme selection
        ttk.Label(self.settings_tab, text="Select Theme:").pack(pady=10)
        self.theme_var = tk.StringVar(value=settings["theme"])
        dark_mode_btn = ttk.Radiobutton(
            self.settings_tab, text="Dark Mode", variable=self.theme_var, value="dark",
            command=self.change_theme
        )
        light_mode_btn = ttk.Radiobutton(
            self.settings_tab, text="Light Mode", variable=self.theme_var, value="light",
            command=self.change_theme
        )
        dark_mode_btn.pack(pady=5)
        light_mode_btn.pack(pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)

    def add_learning_path(self):
        path_selected = filedialog.askdirectory()
        if path_selected:
            # Add the path to the Treeview
            self.tree.insert('', 'end', values=(path_selected,))

    def remove_learning_path(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

    def start_organizing(self):
        folder_path = Path(self.folder_var.get())
        if not folder_path.exists() or not folder_path.is_dir():
            messagebox.showerror("Error", "Please select a valid folder to organize.")
            return

        learning_paths = [Path(self.tree.item(child)["values"][0]) for child in self.tree.get_children()]

        self.status_var.set("Initializing model training...")
        self.progress_var.set(0)
        self.update_idletasks()

        # Run the organizing process in a separate thread
        threading.Thread(target=self.run_organizing_process, args=(folder_path, learning_paths)).start()

    def run_organizing_process(self, folder_path, learning_paths):
        model, vectorizer = load_model()

        if learning_paths:
            self.status_var.set("Training model based on selected directories...")
            self.update_idletasks()
            model, vectorizer = analyze_user_patterns(learning_paths)
        elif model is None:
            self.status_var.set("No training data found. Using default model.")
            self.update_idletasks()
            model, vectorizer = train_default_model()
        else:
            self.status_var.set("Using existing model for organization.")
            self.update_idletasks()

        if model is None or vectorizer is None:
            self.status_var.set("Failed to train or load the model.")
            messagebox.showerror("Error", "Failed to train or load the model.")
            return

        self.status_var.set("Organizing files...")
        self.update_idletasks()

        organize_items_ml(folder_path, model, vectorizer, progress_callback=self.update_progress)
        self.status_var.set("Organization complete!")
        messagebox.showinfo("Completed", "Folder organization complete!")

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.update_idletasks()

    def change_theme(self):
        settings["theme"] = self.theme_var.get()
        save_settings(settings)
        self.apply_theme()


# Run GUI
if __name__ == "__main__":
    app = FolderOrganizerGUI()
    app.mainloop()

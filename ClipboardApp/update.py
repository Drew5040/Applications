from os import getcwd, chdir
from logging import info, warning
from tkinter import END, messagebox, filedialog


# Append the processed ID's to text display
def update_text_display(app, text):
    app.text_display.insert(END, text + "\n", "center")
    app.text_display.see(index=END)


def redo_text_display(app, text):
    with open(file=app.filepath, mode="r") as file:
        lines = file.readlines()
        section_index = lines.index("APPROVALS\n") + 2
        while not lines[section_index].startswith("NEW_MASTERS"):
            section_index += 1
        section_index -= 1


# Update label to display the current working directory
def update_directory_label(app):
    app.directory_label.config(text=app.display_current_directory())


# Update counter label for unique master IDs
def update_counter_label(app):
    app.counter_label.config(text=f"Unique Master ID count: {app.master_id_counter}")


# Grab current working directory
def display_current_directory(app):
    app.current_directory = getcwd()
    return app.current_directory


# Select working directory functionality
def set_working_directory(app):
    new_directory = filedialog.askdirectory()
    if new_directory:
        chdir(path=new_directory)
        app.update_directory_label()
        messagebox.showinfo("Working directory set", f"Working directory set to: {new_directory}")
        info(f"Working directory set to: {new_directory}")
    else:
        messagebox.showwarning("No directory", "No directory selected.")
        warning("No directory selected")


# Grab, set, check, strip, & append master ID entry to file
def set_master_id(app):
    app.master_id = app.master_id_entry.get().strip()
    if not app.master_id:
        messagebox.showwarning("No Master ID", "Please enter a Master ID.")
        warning("No Master ID entered")
    else:
        info(f"Master ID set to: {app.master_id}")

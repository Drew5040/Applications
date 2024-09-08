from os import getcwd, chdir, startfile
from logging import info, warning, error, debug
from traceback import format_exc
from tkinter import END, messagebox, filedialog


# Open working file
def open_file() -> None:
    # Open file dialog & get the 'file_path'
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    # Open selected file locally in native text editor
    if file_path:
        try:
            startfile(file_path)

        except (OSError, IOError) as e:
            # Handle file related exceptions
            error(f"An exception occurred when opening the file: {e}")
            error(format_exc())

        except Exception as e:
            # Handle unexpected exceptions
            error(f"An unexpected exception occurred when opening the file: {e}")
            error(format_exc())
    else:
        # Log that no file was selected
        info("No file selected")


# Append processed ID's to text display
def update_text_display(app, text: str) -> None:
    # Insert 'text' into 'text_display' widget
    app.text_display.insert(END, text + "\n", "center")

    # Scroll to end of 'text_display'
    app.text_display.see(index=END)


# Update current working directory label
def update_directory_label(app) -> None:
    app.working_directory = getcwd()
    app.dir_label.config(text=app.working_directory)


# Update counter label for unique master IDs
def update_counter_label(app) -> None:
    app.counter_label.config(text=f"Unique Master ID count: {app.master_id_counter}")


# Grab, set, check, strip, 'master_id' entry
def set_master_id(app) -> None:
    # Get 'master_id' from entry field & strip whitespace
    app.master_id = app.master_id_entry.get().strip()

    # Check if 'master_id' is empty & show warning if needed
    if not app.master_id:
        messagebox.showwarning("No Master ID", "Please enter a Master ID.")
        warning("No Master ID entered")
    else:
        # Log the 'master_id' that was set
        info(f"Master ID set to: {app.master_id}")

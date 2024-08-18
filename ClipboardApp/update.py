from os import getcwd, chdir, startfile
from logging import info, warning, error
from traceback import format_exc
from tkinter import END, messagebox, filedialog
from ttkthemes import ThemedTk


# Grab current working directory
def display_current_directory(app):
    # Get current working directory
    app.current_directory = getcwd()

    # Return 'current_directory'
    return app.current_directory


# Open working file
def open_file():
    # Open file dialog & get 'file_path'
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    # Open selected file locally
    if file_path:
        try:
            startfile(file_path)
        except (OSError, IOError, FileNotFoundError) as e:
            # Handle file related exceptions
            error(f"An exception occurred when opening the file: {e}")
            error(format_exc())
        except Exception as e:
            # Handle unexpected exceptions
            error(f"An unexpected exception occurred when opening the file: {e}")
    else:
        # Log that no file was selected
        info("No file selected")


# Append processed ID's to text display
def update_text_display(app, text):
    # Insert 'text' into 'text_display' widget
    app.text_display.insert(END, text + "\n", "center")

    # Scroll to end of 'text_display'
    app.text_display.see(index=END)


# Update label to display the current working directory
def update_directory_label(app):
    app.dir_label.config(text=display_current_directory(app))


# Update counter label for unique master IDs
def update_counter_label(app):
    app.counter_label.config(text=f"Unique Master ID count: {app.master_id_counter}")


# Set working directory functionality
def set_working_directory(app):
    # Open dialog to select new directory
    new_directory = filedialog.askdirectory()

    # If a directory is selected, change to it & update label
    if new_directory:
        chdir(path=new_directory)
        update_directory_label(app)

        # Show confirmation message & log the change
        messagebox.showinfo("Working directory set", f"Working directory set to: {new_directory}")
        info(f"Working directory set to: {new_directory}")
    else:
        # Show warning if no directory is selected
        messagebox.showwarning("No directory", "No directory selected.")
        warning("No directory selected")


# Grab, set, check, strip, & append 'master_id' entry to file
def set_master_id(app):
    # Get 'master_id' from entry field & strip whitespace
    app.master_id = app.master_id_entry.get().strip()

    # Check if 'master_id' is empty & show warning if needed
    if not app.master_id:
        messagebox.showwarning("No Master ID", "Please enter a Master ID.")
        warning("No Master ID entered")
    else:
        # Log the 'master_id' that was set
        info(f"Master ID set to: {app.master_id}")


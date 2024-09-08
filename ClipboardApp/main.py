from os import path, getcwd, chdir
from sys import exit
from logging import info, basicConfig, DEBUG, INFO, debug
from datetime import datetime
from tkinter import messagebox
from gui import setup_gui, set_window_size, adjust_topmost, check_time_and_close, working_directory_msg
from styles import style_gui
from ttkthemes import ThemedTk
from typing import Union, Tuple, List, Optional, Any, Dict
from states import (
    start_listening, stop_listening, undo_last_action,
    redo_last_action, restore_application_state, save_current_state,
    update_button_states, save_application_state, load_application_state,
    save_stack_states, load_stack_states, get_app_data_dir,
    set_working_directory
)
from clipboard import check_clipboard, process_master_id
from append import (
    append_new_master_id, append_split_candidate,
    append_merge_candidate, append_to_file, append_note,
    append_duplicate_entry
)
from update import (
    update_text_display, update_counter_label, set_master_id, open_file, update_directory_label
)


# noinspection PyAttributeOutsideInit,PyShadowingNames
class App:
    def __init__(self, root: ThemedTk) -> None:
        info("Constructor instantiated")
        # Root window for the GUI
        self.root = root

        # Set custom icon for GUI
        icon_path = path.join(path.dirname(__file__), "favicon.ico")
        self.root.iconbitmap(icon_path)

        # Set title of root window
        self.root.title("Data Steward Clipboard Manager")

        # Set bridge between constructor & Tkinter eventloop to adjust_topmost
        self.root.bind('<Configure>', lambda e: adjust_topmost(self))

        # Flag to control loop in the separate thread
        self.running = False
        # Flag to track application close events
        self.closed = 0
        # Master ID set by user
        self.master_id = None
        # New master id set by user
        self.new_master_id = None
        # Split candidate set by user
        self.split_candidate = None
        # Merge candidate set by user
        self.merge_candidate = None
        # Initial working directory
        self.working_directory = None
        # Keeps track of the previous clipboard content
        self.previous_clipboard = ""
        # Stores the last event time
        self.last_event_time = 0
        # List to store intervals between copy events
        self.note = None
        # Set to store unique master IDs
        self.unique_master_ids = set()
        # Counter for unique master IDs
        self.master_id_counter = 0
        # Variable for duplicate entry
        self.last_processed_entry = None
        # Undo functionality stack
        self.undo_stack = []
        # Redo functionality stack
        self.redo_stack = []
        # Define filepath
        self.filepath = None
        # Grab current date & format
        self.current_date = datetime.now().strftime("%Y.%m.%d")
        # Create filepath
        self.filepath = f"{self.current_date}.approvals.txt"

        # Open the application
        self.open_app()




    ## Instance methods for 'state' management ##
    def start_listening(self) -> None:
        start_listening(self)

    def stop_listening(self) -> None:
        stop_listening(self)

    def undo_last_action(self) -> None:
        undo_last_action(self)

    def redo_last_action(self) -> None:
        redo_last_action(self)

    def restore_application_state(self, state: Optional[Tuple[list, list, int, Optional[str], Optional[str], Optional[str]]]) -> None:
        restore_application_state(self, state)

    def update_button_states(self) -> None:
        update_button_states(self)

    def append_note(self) -> None:
        append_note(self)


    ## Instance methods for clipboard processing ##
    def check_clipboard(self) -> None:
        check_clipboard(self)

    def process_master_id(self, unique_id: str) -> None:
        process_master_id(self, unique_id)


    ## Instance methods for appending entries ##
    def append_new_master_id(self) -> None:
        append_new_master_id(self)

    def append_split_candidate(self) -> None:
        append_split_candidate(self)

    def append_merge_candidate(self) -> None:
        append_merge_candidate(self)

    def append_to_file(self, text: str, section: str) -> None:
        append_to_file(self, text, section)

    def append_duplicate_entry(self) -> None:
        append_duplicate_entry(self)


    ## Instance methods for updating GUI ##
    def update_text_display(self, text: str) -> None:
        update_text_display(self, text)

    def update_directory_label(self) -> None:
        update_directory_label(self)

    def update_counter_label(self) -> None:
        update_counter_label(self)

    def set_working_directory(self) -> None:
        set_working_directory(self)

    def set_master_id(self) -> None:
        set_master_id(self)


    ## Instance method for opening app ##
    def open_app(self) -> None:

        # Set up the GUI
        setup_gui(self)

        # Load the application state
        load_application_state(self)

        # Instantiate GUI style
        style_gui(self)

        # Load stack 'states'
        load_stack_states(self)

        # Delay working directory msg for 5 secs
        self.root.after(1500, working_directory_msg, self)



    ## Instance method for closing app ##
    def close_app(self) -> None:
        if path.isfile(self.filepath):
            debug(f"App closing, file exists, self.filepath: {self.filepath}")
            save_application_state(self)
            save_stack_states(self)
        else:
            debug("App closing, file does not exist")

        self.running = False
        self.root.quit()
        self.root.destroy()


# Main function for application entry into Tkinter 'event-loop'
def main() -> None:
    try:
        app_data_dir = get_app_data_dir()
    except RuntimeError as e:
        # Handle unsupported OS error
        error(f"Application cannot run: {e}")
        messagebox.showerror("Unsupported OS", f"Your operating system is not supported: {system()}")
        # Exit application gracefully
        exit(1)

    # Create main window with stated theme
    root = ThemedTk(theme="vista")

    # Create app
    app = App(root=root)

    # Check time & close app if 5:30pm
    check_time_and_close(root, 13, 42)

    # Handle window close event
    root.protocol(name="WM_DELETE_WINDOW", func=app.close_app)

    # Run main event loop
    root.mainloop()


if __name__ == "__main__":
    # Setup logging
    basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # Run the application
    main()


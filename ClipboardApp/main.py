from logging import info, basicConfig, DEBUG
from datetime import datetime
from gui import setup_gui
from styles import widget_styling
from ttkthemes import ThemedTk
from states import (
    start_listening, stop_listening, undo_last_action,
    redo_last_action, restore_state, save_current_state,
    update_button_states, save_text_display_state, load_text_display_state,
    save_stacks_state, load_stacks_state
)
from clipboard import check_clipboard, process_master_id
from append import (
    append_new_master_id, append_split_candidate,
    append_merge_candidate, append_to_file
)
from update import (
    update_text_display, update_directory_label, update_counter_label,
    display_current_directory, set_working_directory, set_master_id
)


# noinspection PyAttributeOutsideInit,PyShadowingNames
class App:
    def __init__(self, root):
        info("Constructor instantiated")
        # Root window for the GUI
        self.root = root

        # Set the custom icon for the window
        self.root.iconbitmap("favicon.ico")

        # Flag to control the while loop in the separate thread
        self.running = False
        # Master ID set by user
        self.master_id = None
        # New master id set by user
        self.new_master_id = None
        # Split candidate set by user
        self.split_candidate = None
        # Merge candidate set by user
        self.merge_candidate = None
        # Keeps track of the previous clipboard content
        self.previous_clipboard = ""
        # Stores the last event time
        self.last_event_time = None
        # List to store intervals between copy events
        self.intervals = []
        # Set to store unique master IDs
        self.unique_master_ids = set()
        # Counter for unique master IDs
        self.master_id_counter = 0
        # Undo functionality stack
        self.undo_stack = []
        # Redo functionality stack
        self.redo_stack = []

        # Define filepath
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y.%m.%d")
        self.filepath = f"{formatted_time}.approvals.txt"

        # Set up the GUI components
        setup_gui(self)
        widget_styling(self)
        load_text_display_state(self)
        load_stacks_state(self)

    # Close application gracefully
    def close(self):
        save_text_display_state(self)
        save_stacks_state(self)
        self.running = False
        self.root.quit()

    ## Methods for state management ##
    def start_listening(self):
        start_listening(self)

    def stop_listening(self):
        stop_listening(self)

    def undo_last_action(self):
        undo_last_action(self)

    def redo_last_action(self):
        redo_last_action(self)

    def restore_state(self, state):
        restore_state(self, state)

    def update_button_states(self):
        update_button_states(self)


    ## Methods for clipboard processing ##
    def check_clipboard(self):
        check_clipboard(self)

    def process_master_id(self, unique_id):
        process_master_id(self, unique_id)

    # Methods for appending entries
    def append_new_master_id(self):
        append_new_master_id(self)

    def append_split_candidate(self):
        append_split_candidate(self)

    def append_merge_candidate(self):
        append_merge_candidate(self)

    def append_to_file(self, text, section):
        append_to_file(self, text, section)

    # Methods for updating GUI
    def update_text_display(self, text):
        update_text_display(self, text)

    def update_directory_label(self):
        update_directory_label(self)

    def update_counter_label(self):
        update_counter_label(self)

    def display_current_directory(self):
        return display_current_directory(self)

    def set_working_directory(self):
        set_working_directory(self)

    def set_master_id(self):
        set_master_id(self)


if __name__ == "__main__":
    # Setup logging
    basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # Create main window with stated theme
    root = ThemedTk(theme="vista")
    # Create app
    app = App(root=root)
    # Handle window close event
    root.protocol(name="WM_DELETE_WINDOW", func=app.close)
    # Run main loop
    root.mainloop()
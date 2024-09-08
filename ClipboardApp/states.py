from os import path, makedirs, environ, chdir
from datetime import datetime
from json import load, dump, JSONDecodeError
from logging import info, debug, warning, error
from traceback import format_exc
from tkinter import filedialog, messagebox, NORMAL, DISABLED, END
from platform import system
from threading import Thread
from typing import Optional, Tuple
from update import update_directory_label


# Set working directory functionality
def set_working_directory(app) -> None:
    # Open dialog to select new directory
    new_directory = filedialog.askdirectory()

    # If a directory is selected, change it & update current directory label
    if new_directory:
        chdir(path=new_directory)
        update_directory_label(app)

        # Store new directory
        app.working_directory = new_directory
        debug(f'set_working_directory to: {app.working_directory}')

        # Show confirmation message & log the change
        messagebox.showinfo("Working directory set", f"Working directory set to: {new_directory}")

    else:
        # Show warning if no directory is selected
        messagebox.showwarning("No directory", "No directory selected.")
        warning("No directory selected")


# Check user OS & create JSON files to save application states
def get_app_data_dir() -> str:
    app_name = "Data Steward Clipboard Manager"
    systehm = system()

    # Determine save directory based on OS
    if systehm == 'Windows':
        path_to_dir = path.join(environ['LOCALAPPDATA'], app_name)
        return path_to_dir
    elif systehm == 'Darwin':
        return path.join(path.expanduser('~'), 'Library', 'Application Support', app_name)
    elif systehm == 'Linux':
        return path.join(path.expanduser('~'), '.config', app_name)
    else:
        # Raise error if OS is unsupported
        raise RuntimeError('Unsupported OS')


# Validate & configure 'Start Listening' & 'Stop Listening' button functionality when thread is operating
def start_listening(app) -> None:
    # Check if 'master_id' is set
    if not app.master_id:
        messagebox.showwarning("No Master ID", "Please set the Master ID before starting.")
        warning("Attempted to start listening without 'Master ID'")
        return

    # Set 'running' flag to True
    app.running = True

    # Disable 'start_button' & enable 'stop_button'
    app.start_button.config(state=DISABLED)
    app.stop_button.config(state=NORMAL)

    # Update 'status_label' to indicate listening state
    app.status_label.config(state=NORMAL)
    app.status_label.delete("1.0", END)
    app.status_label.insert("1.0", "   Status: ", "black")
    app.status_label.insert("end", "LISTENING", "green")
    app.status_label.config(state=DISABLED)

    # Clear initial clipboard content right before starting thread
    app.root.clipboard_clear()

    # Start separate thread for clipboard listening
    app.clipboard_thread = Thread(target=app.check_clipboard)
    # Allow termination of separate thread
    app.clipboard_thread.daemon = True
    # Start thread
    app.clipboard_thread.start()

    # Log that clipboard listening has started
    info("Clipboard listening...")


# Validate & configure 'Stop Listening' & 'Start Listening' button functionality when thread is not operating
def stop_listening(app) -> None:
    # Set 'running' flag to False
    app.running = False

    # Enable 'start_button' & disable 'stop_button'
    app.start_button.config(state=NORMAL)
    app.stop_button.config(state=DISABLED)

    # Update 'status_label' to indicate stopped state
    app.status_label.config(state=NORMAL)
    app.status_label.delete("1.0", END)
    app.status_label.insert("1.0", "   Status: ", "black")
    app.status_label.insert("end", "STOPPED", "red")
    app.status_label.config(state=DISABLED)

    # Log clipboard listener has stopped
    info("Clipboard listener stopped")


# Disable/enable undo & redo buttons based on stack content
def update_button_states(app) -> None:
    # Log current sizes of 'undo_stack' & 'redo_stack'
    debug(f"Updating button states. 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")

    # Enable undo button if 'redo_stack' has content, otherwise disable it
    app.undo_button.config(state=NORMAL if app.redo_stack else DISABLED)

    # Enable redo button if 'undo_stack' has more than one 'state', otherwise disable it
    app.redo_button.config(state=NORMAL if len(app.undo_stack) > 1 else DISABLED)


# Undo previous action
def undo_last_action(app) -> None:
    if len(app.undo_stack) > 1:
        # Save current 'state' before undoing
        current_state = save_current_state(app, app.filepath)
        debug(f"Undo: Current 'state' saved. Pushing to 'redo_stack'. 'State': {current_state}")

        # Append 'current_state' to 'redo_stack'
        app.redo_stack.append(current_state)

        # Pop previous 'state' off 'undo_stack' & restore it
        previous_state = app.undo_stack.pop()
        debug(
            f"Undo: Popping from 'undo_stack' & restoring 'state': {previous_state} Length of 'undo_stack': {len(app.undo_stack)}")

        # Restore previous 'state'
        app.restore_application_state(previous_state)
        info("Undid last action")

    # Check if 'undo_stack' is down to one 'state' & disable the undo button
    if len(app.undo_stack) < 2:
        app.undo_button.config(state=DISABLED)

    # Log sizes of 'undo_stack' & 'redo_stack' after undo action
    debug(f"After undo action: 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")
    update_button_states(app)


# Redo previous action
def redo_last_action(app) -> None:
    if app.redo_stack:
        # Save current 'state' before redoing
        current_state = save_current_state(app, app.filepath)
        debug(f"Redo: Current 'state' saved. Pushing to undo stack. 'State': {current_state}")

        # Append 'current_state' to 'undo_stack'
        app.undo_stack.append(current_state)

        # Pop next 'state' off 'redo_stack'
        next_state = app.redo_stack.pop()

        # Restore next 'state'
        debug(f"Redo: Popping from 'redo_stack' & restoring 'state': {next_state}")
        app.restore_application_state(next_state)

        # Log successful 'redo' action
        info("Redid last action")

    # After redo action, check if 'redo_stack' is empty & update button states
    debug(f"After redo action: 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")
    update_button_states(app)


# Save current state of text display in file
def save_current_state(app, filepath: str) -> Optional[Tuple[list, list, int, Optional[str], Optional[str], Optional[str]]]:
    try:
        # Check if 'filepath' exists
        if not path.exists(filepath):
            error(f"File not found: {filepath}")
            return None

        # Read & save 'file_state'
        with open(file=filepath, mode="r") as file:
            file_state = file.readlines()

        # Save current 'text_display_state'
        text_display_state = app.text_display.get("1.0", END).splitlines(keepends=True)

        # Return 'file_state', 'text_display_state', 'master_id_counter', & 'last_processed_entry'
        return file_state, text_display_state, app.master_id_counter, app.last_processed_entry, app.working_directory, \
            app.current_date

    # Handle file related errors
    except (OSError, IOError) as e:
        error(f"An exception occurred while saving txt file's current state: {e}")
        error(format_exc())

    # Handle any other unexpected errors
    except Exception as e:
        error(f"An unexpected exception occurred while saving txt file's current state: {e}")
        error(format_exc())


# Save application 'state' data for persistence
def save_application_state(app) -> None:
    try:
        # Determine directory 'application_state' will be saved in & create if needed
        app_data_dir = get_app_data_dir()
        makedirs(app_data_dir, exist_ok=True)

        # Create path to 'text_display_state.json' file
        filepath = path.join(app_data_dir, 'application_state_data.json')

        # Capture current 'state' of file, text display, counter, and last processed entry
        file_state, text_display_state, master_id_counter_state, app.last_processed_entry, app.working_directory, \
            app.current_date = save_current_state(app, app.filepath)

        # Prepare 'application_state' data for saving
        state = {
            'file_state': file_state,
            'text_display_state': text_display_state,
            'master_id_counter_state': master_id_counter_state,
            'duplicate_entry_stack_state': app.last_processed_entry,
            'working_directory_state': app.working_directory,
            'current_date': app.current_date,
        }

        # Save 'application_state' data to JSON file
        with open(filepath, 'w') as f:
            dump(state, f)

        # Log successful save of 'application_state'
        debug(f"All states saved to: {filepath}.")

    except (OSError, IOError) as e:
        # Handle file related errors
        error(f"An exception occurred while saving text display state: {e}")
        error(format_exc())

    except Exception as e:
        # Handle unexpected errors
        error(f"An unexpected exception occurred while saving text display state: {e}")
        error(format_exc())


# Restore content of application file & text display to a previously saved 'state'
def restore_application_state(app, state: Tuple) -> Optional[Tuple[list, list, int, Optional[str], Optional[str], Optional[str]]]:
    try:
        # Check if 'state' is None
        if state is None:
            error("Cannot restore state: 'state' is None")
            return

        # Unpack tuple of 'application_state' data
        file_state, text_state, master_id_counter, last_processed_entry, working_directory, current_date = state

        # Write 'file_state' to specified file
        with open(app.filepath, "w") as file:
            file.writelines(file_state)

        # Clear current text display & insert saved 'text_state'
        app.text_display.delete("1.0", END)
        for line in text_state:
            if line.strip():
                app.text_display.insert(END, line.strip() + "\n", "center")
        app.text_display.see(END)

        # Update master ID counter & update counter label
        app.master_id_counter = master_id_counter
        app.update_counter_label()

        # Restore last processed entry & update button 'states'
        app.last_processed_entry = last_processed_entry
        update_button_states(app)

        # Restore, switch, & update working directory & label
        app.working_directory = working_directory
        chdir(path=app.working_directory)
        update_directory_label(app)

        # Restore value of 'current_date' attribute
        app.current_date = current_date

    except (OSError, IOError) as e:
        # Handle file-related errors
        error(f"An exception occurred while restoring content of txt file & txt display: {e}")
        error(format_exc())

    except Exception as e:
        # Handle any other unexpected errors
        error(f"An unexpected exception occurred while restoring content of txt file & txt display: {e}")
        error(format_exc())


# Load last 'state' of application
def load_application_state(app) -> bool:
    # Grab directory & filepath for saved application 'state' data file
    app_data_dir = get_app_data_dir()
    filepath = path.join(app_data_dir, 'application_state_data.json')

    try:

        # Open & load application 'state' from JSON file
        with open(filepath, 'r') as file:
            state = load(file)

            # Grab current_date
            current_date = datetime.now().strftime('%Y.%m.%d')

            # Extract last saved value of 'app.current_date' attribute from 'application_state_data' .json file
            saved_date = state.get('current_date', None)

            # Check if application 'state' file exists
            if path.isfile(filepath) and current_date == saved_date:
                # Extract saved states from dict
                file_state = state.get('file_state', [])
                text_state = state.get('text_display_state', [])
                master_id_counter_state = state.get('master_id_counter_state', 0)
                last_processed_entry = state.get('last_processed_entry', None)
                working_directory_state = state.get('working_directory_state', None)

                # Restore the application 'state'
                app.restore_application_state((
                    file_state,
                    text_state,
                    master_id_counter_state,
                    last_processed_entry,
                    working_directory_state,
                    saved_date
                ))

                # Initialize undo stack with loaded 'state'
                app.undo_stack = [(
                    file_state,
                    text_state,
                    master_id_counter_state,
                    last_processed_entry,
                    working_directory_state,
                    saved_date
                )]

                # Update 'state' of undo, redo, & duplicate entry buttons
                update_button_states(app)

                # Log application loaded
                debug(f"Date not different, application loaded")

                return True

            # Check if file exists & if date is different
            elif path.isfile(filepath) and current_date != saved_date:

                # Clear all states
                file_state = []
                text_state = []
                master_id_counter_state = 0
                last_processed_entry = None
                working_directory_state = None
                saved_date = None

                # Restore the application 'state'
                app.restore_application_state((
                    file_state,
                    text_state,
                    master_id_counter_state,
                    last_processed_entry,
                    working_directory_state,
                    saved_date
                ))

                # Initialize undo stack with loaded default and empty 'state'
                app.undo_stack = [(
                    file_state,
                    text_state,
                    master_id_counter_state,
                    last_processed_entry,
                    working_directory_state,
                    saved_date
                )]

                # Update 'state' of undo, redo, & duplicate entry buttons
                update_button_states(app)

                # Log application loaded
                debug(f"Date is different, application loaded")

                return True

    # Handle exceptions
    except (OSError, IOError, JSONDecodeError) as e:
        error(f"An exception occurred when restoring application state {e}")
        error(format_exc())

    except Exception as e:
        error(f"An unexpected exception occurred when restoring application state {e}")
        error(format_exc())

        return False


# Save current stack 'states' (undo/redo)
def save_stack_states(app) -> None:
    try:
        # Prepare 'state' data to be saved
        stacks_state = {
            'undo_stack': app.undo_stack,
            'redo_stack': app.redo_stack
        }

        # Determine directory for saving 'state' files
        app_data_dir = get_app_data_dir()

        # Ensure directory exists
        makedirs(app_data_dir, exist_ok=True)

        # Define filepath for stack 'state' file
        filepath = path.join(app_data_dir, 'stacks_state.json')

        # Save stack 'states' to JSON file
        with open(filepath, 'w') as file:
            dump(stacks_state, file)

        debug(f"Stacks state saved to {filepath}.")

    except (OSError, IOError) as e:
        # Handle file related errors
        error(f"An exception occurred while saving current stack states: {e}")
        error(format_exc())

    except Exception as e:
        # Handle unexpected errors
        error(f"An unexpected exception occurred while saving current stack states: {e}")
        error(format_exc())


# Load previously saved stack 'states' (undo & redo)
def load_stack_states(app) -> bool:
    try:
        # Determine directory & filepath for stack 'state' file
        app_data_dir = get_app_data_dir()

        # Grab directory & filepath for saved application 'state' data file
        app_data = path.join(app_data_dir, 'application_state_data.json')

        with open(app_data, 'r') as file:
            state = load(file)
            # Extract last saved value of 'app.current_date' attribute from 'application_state_data' .json file
            saved_date = state.get('current_date', None)

        # Grab current date
        current_date = datetime.now().strftime('%Y.%m.%d')

        filepath = path.join(app_data_dir, 'stacks_state.json')

        # Check if stack 'state' file exists
        if path.exists(filepath) and current_date == saved_date:
            # Open & load stack 'state' from JSON file
            with open(filepath, 'r') as file:
                stacks_state = load(file)

            # Restore undo & redo stacks from loaded 'state'
            app.undo_stack = stacks_state.get('undo_stack', [])
            app.redo_stack = stacks_state.get('redo_stack', [])

            # Log number of items loaded into each stack
            debug(f"Loaded undo_stack with {len(app.undo_stack)} items & redo_stack with {len(app.redo_stack)} items.")

            # Update button 'states' based on loaded stacks
            app.update_button_states()

            return True

        elif path.exists(filepath) and current_date != saved_date:

            app.undo_stack = []
            app.redo_stack = []

            # Log number of items loaded into each stack
            debug(f"Loaded undo_stack with {len(app.undo_stack)} items & redo_stack with {len(app.redo_stack)} items.")

            # Update button 'states' based on loaded stacks
            app.update_button_states()

            return True

        else:
            # Log warning if stack 'state' file not found
            warning(f"Stack state file not found: {filepath}")
            return False

    # Handle file related & JSON decoding errors
    except (OSError, IOError, JSONDecodeError, FileNotFoundError) as e:
        error(f"An error occurred while loading saved stack states: {e}")
        return False

    # Handle unexpected errors
    except Exception as e:
        error(f"An unexpected error occurred while loading saved stack states: {e}")
        return False

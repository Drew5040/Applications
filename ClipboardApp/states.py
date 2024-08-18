from os import path, makedirs, environ
from json import load, dump, JSONDecodeError
from logging import info, debug, warning, error
from traceback import format_exc
from tkinter import messagebox, NORMAL, DISABLED, END
from ttkthemes import ThemedTk
from platform import system
from threading import Thread


# Check user OS & create JSON files to save application states
def get_app_data_dir():
    app_name = "Data Steward Clipboard Manager"
    systehm = system()

    # Determine save directory based on OS
    if systehm == 'Windows':
        path_to_dir = path.join(environ['LOCALAPPDATA'], app_name)
        info(f"State files should be in: {path_to_dir}")
        return path_to_dir
    elif systehm == 'Darwin':
        return path.join(path.expanduser('~'), 'Library', 'Application Support', app_name)
    elif systehm == 'Linux':
        return path.join(path.expanduser('~'), '.config', app_name)
    else:
        # Raise error if OS is unsupported
        raise RuntimeError('Unsupported OS')


# Validate & configure 'Start Listening' & 'Stop Listening' button functionality when thread is operating
def start_listening(app):
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

    # Clear or set clipboard to a dummy value to ignore current content
    root = ThemedTk()
    root.withdraw()
    root.clipboard_clear()
    root.update()
    root.destroy()

    # Start separate thread for clipboard listening
    app.clipboard_thread = Thread(target=app.check_clipboard)
    app.clipboard_thread.daemon = True
    app.clipboard_thread.start()

    # Log that clipboard listening has started
    info("Clipboard listening...")


# Validate & configure 'Stop Listening' & 'Start Listening' button functionality when thread is not operating
def stop_listening(app):
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


# Save current state of text display in file
def save_current_state(app, filepath):
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

        # Return 'file_state', 'text_display_state', & 'master_id_counter'
        return file_state, text_display_state, app.master_id_counter

    # Handle file-related errors
    except (OSError, IOError) as e:
        error(f"An exception occurred while saving txt file's current state: {e}")
        error(format_exc())

    # Handle any other unexpected errors
    except Exception as e:
        error(f"An unexpected exception occurred while saving txt file's current state: {e}")
        error(format_exc())


# Disable/enable undo & redo buttons based on stack content
def update_button_states(app):
    # Log current sizes of 'undo_stack' & 'redo_stack'
    debug(f"Updating button states. 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")

    # Enable undo button if 'redo_stack' has content, otherwise disable it
    app.undo_button.config(state=NORMAL if app.redo_stack else DISABLED)

    # Enable redo button if 'undo_stack' has more than one 'state', otherwise disable it
    app.redo_button.config(state=NORMAL if len(app.undo_stack) > 1 else DISABLED)


# Undo previous action
def undo_last_action(app):
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
        app.restore_state(previous_state)
        info("Undid last action")

    # Check if 'undo_stack' is down to one 'state' & disable the undo button
    if len(app.undo_stack) < 2:
        app.undo_button.config(state=DISABLED)

    # Log sizes of 'undo_stack' & 'redo_stack' after undo action
    debug(f"After undo action: 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")
    update_button_states(app)


# Redo previous action
def redo_last_action(app):
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
        app.restore_state(next_state)

        # Log successful 'redo' action
        info("Redid last action")

    # After redo action, check if 'redo_stack' is empty & update button states
    debug(f"After redo action: 'Undo_stack' size: {len(app.undo_stack)}, 'Redo_stack' size: {len(app.redo_stack)}")
    update_button_states(app)


# Restore content of application file & text display to a previously saved 'state'
def restore_state(app, state):
    try:
        # Check if 'state' is None
        if state is None:
            error("Cannot restore state: 'state' is None")
            return

        file_state, text_state, master_id_counter = state

        # Write 'file_state' to specified file
        with open(app.filepath, "w") as file:
            file.writelines(file_state)

        # Clear current text display & insert saved 'text_state'
        app.text_display.delete("1.0", END)
        for line in text_state:
            if line.strip():
                app.text_display.insert(END, line.strip() + "\n", "center")
        app.text_display.see(END)

        # Update master ID counter
        app.master_id_counter = master_id_counter
        app.update_counter_label()

    except (OSError, IOError) as e:
        # Handle file-related errors
        error(f"An exception occurred while restoring content of txt file & txt display: {e}")
        error(format_exc())
    except Exception as e:
        # Handle any other unexpected errors
        error(f"An unexpected exception occurred while restoring content of txt file & txt display: {e}")
        error(format_exc())


# Save application 'state' data for persistence
def save_application_state(app):
    try:
        # Determine directory & create it if needed
        app_data_dir = get_app_data_dir()
        makedirs(app_data_dir, exist_ok=True)
        filepath = path.join(app_data_dir, 'text_display_state.json')

        # Capture current 'state' of file & text display
        file_state, text_display_state, master_id_counter_state = save_current_state(app, app.filepath)

        # Prepare 'state' data for saving
        state = {
            'file_state': file_state,
            'text_display_state': text_display_state,
            'master_id_counter_state': master_id_counter_state,
        }

        # Save 'state' data to JSON file
        with open(filepath, 'w') as f:
            dump(state, f)

        # Log successful save off 'state'
        info(f"Text display state saved to {filepath}.")

    except (OSError, IOError) as e:
        # Handle file related errors
        error(f"An exception occurred while saving text display state: {e}")
        error(format_exc())
    except Exception as e:
        # Handle unexpected errors
        error(f"An unexpected exception occurred while saving text display state: {e}")
        error(format_exc())


# Load last 'state' of application
def load_application_state(app):
    # Determine directory & filepath for application 'state' file
    app_data_dir = get_app_data_dir()
    filepath = path.join(app_data_dir, 'text_display_state.json')

    # Check if application 'state' file exists
    if path.exists(filepath):
        # Open & load application 'state' from JSON file
        with open(filepath, 'r') as f:
            state = load(f)

        # Default value for unique master id counter 'state'
        master_id_counter_state = state.get('master_id_counter_state', 0)

        # Restore last 'state'
        app.restore_state((state['file_state'], state['text_display_state'], master_id_counter_state))

        # Initialize undo stack with loaded 'state'
        app.undo_stack = [(state['file_state'], state['text_display_state'], master_id_counter_state)]

        # Update 'state' of undo & redo buttons
        app.update_button_states()

        return True

    return False


# Save current stack 'states' (undo/redo)
def save_stack_states(app):
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
        with open(filepath, 'w') as f:
            dump(stacks_state, f)

        info(f"Stacks state saved to {filepath}.")

    except (OSError, IOError) as e:
        # Handle file related errors
        error(f"An exception occurred while saving current stack states: {e}")
        error(format_exc())
    except Exception as e:
        # Handle unexpected errors
        error(f"An unexpected exception occurred while saving current stack states: {e}")
        error(format_exc())


# Load previously saved stack 'states' (undo & redo)
def load_stack_states(app):
    try:
        # Determine directory & filepath for stack 'state' file
        app_data_dir = get_app_data_dir()
        filepath = path.join(app_data_dir, 'stacks_state.json')

        # Check if stack 'state' file exists
        if path.exists(filepath):
            # Open & load stack 'state' from JSON file
            with open(filepath, 'r') as f:
                stacks_state = load(f)

            # Restore undo & redo stacks from loaded 'state'
            app.undo_stack = stacks_state.get('undo_stack', [])
            app.redo_stack = stacks_state.get('redo_stack', [])

            # Log number of items loaded into each stack
            debug(f"Loaded undo_stack with {len(app.undo_stack)} items & redo_stack with {len(app.redo_stack)} items.")

            # Update button 'states' based on loaded stacks
            app.update_button_states()
            return True
        else:
            # Log warning if stack 'state' file not found
            warning(f"Stack state file not found: {filepath}")
            return False

    # Handle file-related & JSON decoding errors
    except (OSError, IOError, JSONDecodeError) as e:
        error(f"An error occurred while loading saved stack states: {e}")
        return False
    # Handle unexpected errors
    except Exception as e:
        error(f"An unexpected error occurred while loading saved stack states: {e}")
        return False

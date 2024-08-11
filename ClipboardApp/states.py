from os import path, makedirs, environ
from json import load, dump
from logging import info, debug, warning
from tkinter import messagebox, NORMAL, DISABLED, END
from platform import system
from threading import Thread


# Validate & configure start & stop button functionality when thread is listening
def start_listening(app):
    if not app.master_id:
        messagebox.showwarning("No Master ID", "Please set the Master ID before starting.")
        warning("Attempted to start listening without Master ID")
        return

    # Set running flag to True
    app.running = True
    app.start_button.config(state=DISABLED)
    app.stop_button.config(state=NORMAL)
    app.status_label.config(state=NORMAL)
    app.status_label.delete("1.0", END)
    app.status_label.insert("1.0", "   Status: ", "black")
    app.status_label.insert("end", "LISTENING", "green")
    app.status_label.config(state=DISABLED)

    # Start separate thread for listening
    app.clipboard_thread = Thread(target=app.check_clipboard)
    app.clipboard_thread.daemon = True
    app.clipboard_thread.start()

    info("Clipboard listening...")


# Validate & configure start & stop button functionality when thread is not listening
def stop_listening(app):
    app.running = False
    app.start_button.config(state=NORMAL)
    app.stop_button.config(state=DISABLED)

    # Update status label
    app.status_label.config(state=NORMAL)
    app.status_label.delete("1.0", END)
    app.status_label.insert("1.0", "   Status: ", "black")
    app.status_label.insert("end", "STOPPED", "red")
    app.status_label.config(state=DISABLED)

    info("Clipboard listener stopped")


# Save current state of text file for display
def save_current_state(app, filepath):
    with open(file=filepath, mode="r") as file:
        file_state = file.readlines()
    # Save current text display state
    text_display_state = app.text_display.get("1.0", END).splitlines(keepends=True)
    return file_state, text_display_state


# Disable or enable undo & redo buttons based on stack content
def update_button_states(app):
    debug(
        f"Updating button states. Undo stack size: {len(app.undo_stack)}, Redo stack size: {len(app.redo_stack)}")
    app.undo_button.config(state=NORMAL if app.redo_stack else DISABLED)
    app.redo_button.config(state=NORMAL if len(app.undo_stack) > 1 else DISABLED)


# Undo latest action
def undo_last_action(app):
    if len(app.undo_stack) > 1:  # Ensure there's a state to undo to
        # Save current state before undoing (necessary for redo)
        current_state = save_current_state(app, app.filepath)
        debug(f"Undo: Current state saved. Pushing to redo stack. State: {current_state}")

        # Append current_state to redo stack
        app.redo_stack.append(current_state)

        # Pop previous state off stack and restore it
        previous_state = app.undo_stack.pop()
        debug(
            f"Undo: Popping from undo stack and restoring state: {previous_state} Length of undo_stack {len(app.undo_stack)}")

        # Restore previous state
        app.restore_state(previous_state)
        info("Undid last action")

    # Check if undo stack is down to one state and disable the undo button
    if len(app.undo_stack) < 2:
        app.undo_button.config(state=DISABLED)

    debug(f"After undo action: Undo stack size: {len(app.undo_stack)}, Redo stack size: {len(app.redo_stack)}")
    update_button_states(app)


# Redo previous action
def redo_last_action(app):
    if app.redo_stack:
        # Save current state before redoing (necessary for undo)
        current_state = save_current_state(app, app.filepath)
        debug(f"Redo: Current state saved. Pushing to undo stack. State: {current_state}")

        # Append current_state to undo stack
        app.undo_stack.append(current_state)

        # Pop next state off the redo stack
        next_state = app.redo_stack.pop()

        # Restore next state
        debug(f"Redo: Popping from redo stack and restoring state: {next_state}")
        app.restore_state(next_state)

        info("Redid last action")

    # After redo action, check if redo stack is empty & update button states
    debug(f"After redo action: Undo stack size: {len(app.undo_stack)}, Redo stack size: {len(app.redo_stack)}")
    update_button_states(app)


# Restore application file & text display to a previously saved state
def restore_state(app, state):
    file_state, text_state = state
    with open(app.filepath, "w") as file:
        file.writelines(file_state)
    app.text_display.delete("1.0", END)
    for line in text_state:
        if line.strip():
            app.text_display.insert(END, line.strip() + "\n", "center")
    app.text_display.see(END)


# Check which OS user is operating. Create .json files to save stack states
def get_app_data_dir():
    app_name = "ClipboardApp"
    systehm = system()

    if systehm == 'Windows':
        return path.join(environ['LOCALAPPDATA'], app_name)
    elif systehm == 'Darwin':
        return path.join(path.expanduser('~'), 'Library', 'Application Support', app_name)
    elif systehm == 'Linux':
        return path.join(path.expanduser('~'), '.config', app_name)
    else:
        raise RuntimeError('Unsupported OS')


# Save text display state for reloading if application closes over the course of the day
def save_text_display_state(app):
    app_data_dir = get_app_data_dir()
    makedirs(app_data_dir, exist_ok=True)
    filepath = path.join(app_data_dir, 'text_display_state.json')

    file_state, text_display_state = save_current_state(app, app.filepath)

    state = {
        'file_state': file_state,
        'text_display_state': text_display_state,
    }

    with open(filepath, 'w') as f:
        dump(state, f)


# Save current stack states
def save_stacks_state(app):
    stacks_state = {
        'undo_stack': app.undo_stack,
        'redo_stack': app.redo_stack
    }
    app_data_dir = get_app_data_dir()
    filepath = path.join(app_data_dir, 'stacks_state.json')

    with open(filepath, 'w') as f:
        dump(stacks_state, f)

    info("Stacks state saved.")


# Load last state of stacks
def load_stacks_state(app):
    app_data_dir = get_app_data_dir()
    filepath = path.join(app_data_dir, 'stacks_state.json')

    if path.exists(filepath):
        with open(filepath, 'r') as f:
            stacks_state = load(f)

        app.undo_stack = stacks_state.get('undo_stack', [])
        app.redo_stack = stacks_state.get('redo_stack', [])

        debug(f"Loaded undo_stack with {len(app.undo_stack)} items and redo_stack with {len(app.redo_stack)} items.")
        app.update_button_states()  # Ensure buttons reflect the stack states
        return True

    return False


# Load the last state of text display
def load_text_display_state(app):
    app_data_dir = get_app_data_dir()
    filepath = path.join(app_data_dir, 'text_display_state.json')

    if path.exists(filepath):
        with open(filepath, 'r') as f:
            state = load(f)

        # Restore the last state
        app.restore_state((state['file_state'], state['text_display_state']))

        # Initialize the undo stack with the loaded state
        app.undo_stack = [(state['file_state'], state['text_display_state'])]

        # Update the state of the undo and redo buttons
        app.update_button_states()

        return True

    return False

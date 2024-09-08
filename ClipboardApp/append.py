from os import path
from logging import info, warning, debug, error
from traceback import format_exc
from datetime import datetime
from typing import List, Union
from states import save_current_state, update_button_states
from tkinter import messagebox, END, DISABLED


# Initialize file
def initialize_file(filepath: str) -> List[str]:
    # Check if 'filepath' exists & initialize if not
    if not path.exists(filepath):
        # Define 'initial_state' of file with headers
        initial_state = ["\nAPPROVALS\n\n\n", "NEW_MASTERS\n\n\n", "SPLIT\n\n\n", "MERGE\n\n\n", "NOTES\n\n"]

        # Open 'filepath' & write 'initial_state' to file
        with open(file=filepath, mode="w") as file:
            file.writelines(initial_state)

        # Return 'initial_state'
        return initial_state
    else:
        # Read & return existing file content
        with open(file=filepath, mode="r") as file:
            return file.readlines()


# Grab, check, strip, & append 'new_master_id' entry
def append_new_master_id(app) -> None:
    # Get 'new_master_id' from entry field & strip whitespace
    app.new_master_id = app.new_master_id_entry.get().strip()

    # Check if 'new_master_id' entry box is empty & show warning if needed
    if not app.new_master_id:
        messagebox.showwarning(title="No new Master ID", message="Please enter a new Master ID")
        warning("No new Master ID entered")
    else:
        # Append 'new_master_id' to file under 'NEW_MASTERS' section
        app.append_to_file(text=app.new_master_id, section="NEW_MASTERS")

        # Clear 'new_master_id_entry' after appending
        app.new_master_id_entry.delete(first=0, last=END)

        # Log that new 'new_master_id' was recorded
        info(f"New Master ID recorded: {app.new_master_id}")


# Grab, check, strip, & append 'split_candidate' entry to file, then clear entry box
def append_split_candidate(app) -> None:
    # Get 'split_candidate' from entry field & strip whitespace
    app.split_candidate = app.split_candidate_entry.get().strip()

    # Check if 'split_candidate' is empty & show warning if needed
    if not app.split_candidate:
        messagebox.showwarning(title="No new Split Candidate", message="Please enter a new Split Candidate")
        warning("No new Split Candidate entered")
    else:
        # Append 'split_candidate' to file under 'SPLIT' section
        app.append_to_file(text=app.split_candidate, section="SPLIT")

        # Clear 'split_candidate_entry' after appending
        app.split_candidate_entry.delete(first=0, last=END)

        # Log that new 'split_candidate' was recorded
        info(f"New Split Candidate recorded: {app.split_candidate}")


# Grab, check, strip, & append 'merge_candidate' entry to file, then clear entry
def append_merge_candidate(app) -> None:
    # Get 'merge_candidate' from entry field & strip whitespace
    app.merge_candidate = app.merge_candidate_entry.get().strip()

    # Check if 'merge_candidate' is empty & show warning if needed
    if not app.merge_candidate:
        messagebox.showwarning(title="No new Merge Candidate", message="Please enter a new Merge Candidate")
        warning("No new Merge Candidate entered")
    else:
        # Append 'merge_candidate' to file under 'MERGE' section
        app.append_to_file(text=app.merge_candidate, section="MERGE")

        # Clear 'merge_candidate_entry' after appending
        app.merge_candidate_entry.delete(first=0, last=END)

        # Log that new 'merge_candidate' was recorded
        info(f"New Merge Candidate recorded: {app.merge_candidate}")


def append_duplicate_entry(app) -> None:
    # Check if 'master_id' is empty & show warning if needed
    if not app.master_id:
        messagebox.showwarning(title="No Master ID Warning", message="Please enter a Master ID.")
        warning("No Master ID entered")
    elif app.last_processed_entry is None:
        messagebox.showwarning(title="Duplicates", message="You can only duplicate entries once.")
    else:
        # Append the last processed entry to the file again
        app.append_to_file(text=app.last_processed_entry, section="APPROVALS")
        info(f"Duplicated entry: {app.last_processed_entry}")

        # Reset 'last_processed_entry'
        app.last_processed_entry = None


# Grab, check, strip, & append 'notes' entry to file. Then clear entry
def append_note(app) -> None:
    # Get notes from the 'note_display' Text widget
    notes = app.note_display.get("1.0", END).strip()

    # Check if notes are empty & show warning if needed
    if not notes:
        messagebox.showwarning("No Note", "Please enter a note before appending.")
        warning("No note entered")
    else:
        # Append notes to file under 'NOTES' section
        app.append_to_file(text=notes, section="NOTES")

        # Clear 'note_display' after appending
        app.note_display.delete("1.0", END)

        # Log that notes were recorded & appended
        info("Notes recorded and appended to file")


# Initialize file & append processed ID's under their appropriate headers
def append_to_file(app, text: str, section: str) -> None:
    # Create file name
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y.%m.%d")
    app.filepath = f"{formatted_time}.approvals.txt"

    # Check if file exists & initialize if not
    if not path.exists(app.filepath):
        initial_state = initialize_file(app.filepath)
        app.undo_stack.append(initial_state)

    try:
        # Save current file & display state to 'undo_stack'
        current_state = save_current_state(app, app.filepath)
        app.undo_stack.append(current_state)

        # Clear 'redo_stack' since a new action was taken
        app.redo_stack.clear()

        with open(app.filepath, "r+") as file:
            # Read & process file contents
            lines = file.readlines()

            # Find line index to insert processed IDs under correct headers
            if section == "APPROVALS":
                section_index = lines.index("APPROVALS\n") + 2
                while not lines[section_index].startswith("NEW_MASTERS"):
                    section_index += 1
                section_index -= 1

            elif section == "NEW_MASTERS":
                section_index = lines.index("NEW_MASTERS\n") + 2
                while not lines[section_index].startswith("SPLIT"):
                    section_index += 1
                section_index -= 1

            elif section == "SPLIT":
                section_index = lines.index("SPLIT\n") + 2
                while not lines[section_index].startswith("MERGE"):
                    section_index += 1
                section_index -= 1

            elif section == "MERGE":
                section_index = lines.index("MERGE\n") + 2
                while not lines[section_index].startswith("NOTES"):
                    section_index += 1
                section_index -= 1

            else:
                section_index = lines.index("NOTES\n") + 2

            # Insert new entry under correct header
            lines.insert(section_index, text + "\n")

            # Bring pointer back to start of file
            file.seek(0)
            file.writelines(lines)

            # Log that text was appended to file
            info(f"Appended to file: {text}")

        # Update text display with new ID
        app.text_display.insert(END, text + "\n", "center")
        app.text_display.see(END)

    # Handle file related exceptions
    except (OSError, IOError) as e:
        error(f"An exception occurred while appending to the file: {e}")
        error(format_exc())

    except Exception as e:
        error(f"An unexpected exception occurred while appending to the file: {e}")
        error(format_exc())

    # Update button states after appending
    update_button_states(app)

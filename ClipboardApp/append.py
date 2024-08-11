from os import path
from logging import info, warning, debug, error
from time import sleep
from datetime import datetime
from states import save_current_state
from tkinter import messagebox, END


# Initialize file
def initialize_file(filepath):
    if not path.exists(filepath):
        initial_state = ["\nAPPROVALS\n\n\n", "NEW_MASTERS\n\n\n", "SPLIT\n\n\n", "MERGE\n\n"]
        # Open file & record initial state
        with open(file=filepath, mode="w") as file:
            file.writelines(initial_state)
        return initial_state
    else:
        with open(file=filepath, mode="r") as file:
            return file.readlines()


# Functionality for processing & combining copied master id's
def process_master_id(app, unique_id):
    debug(f"process_identifier called with unique_id: {unique_id}")
    # Delay to ensure file accessibility
    sleep(0.1)
    try:
        # Combine master ID with unique ID & append to file
        combined_id = f"{app.master_id} ({unique_id})"
        info(f"Processing identifier: {combined_id}")

        # Append combined ids
        app.append_to_file(text=combined_id, section="APPROVALS")

        # Check if master ID is unique & update unique id counter
        if app.master_id not in app.unique_master_ids:
            app.unique_master_ids.add(app.master_id)
            app.master_id_counter += 1
            app.update_counter_label()

    except Exception as e:
        error(f"Error processing identifier: {e}")


# Grab, check, strip, & append new master ID to file
def append_new_master_id(app):
    app.new_master_id = app.new_master_id_entry.get().strip()
    if not app.new_master_id:
        messagebox.showwarning("No new Master ID", "Please enter a new Master ID")
        warning("No new Master ID entered")
    else:
        app.append_to_file(text=app.new_master_id, section="NEW_MASTERS")
        app.new_master_id_entry.delete(first=0, last=END)
        info(f"New Master ID recorded: {app.new_master_id}")


# Grab, check, strip, & append split candidate to file. Then, clear entry
def append_split_candidate(app):
    app.split_candidate = app.split_candidate_entry.get().strip()
    if not app.split_candidate:
        messagebox.showwarning("No new Split Candidate", "Please enter a new Split Candidate")
        warning("No new Split Candidate entered")
    else:
        app.append_to_file(text=app.split_candidate, section="SPLIT")
        app.split_candidate_entry.delete(first=0, last=END)
        info(f"New Master ID recorded: {app.split_candidate}")


#  Grab, check, strip, & append merge candidate to file. Then clear entry
def append_merge_candidate(app):
    app.merge_candidate = app.merge_candidate_entry.get().strip()
    if not app.merge_candidate:
        messagebox.showwarning("No new Merge Candidate", "Please enter a new Merge Candidate")
        warning("No new Merge Candidate entered")
    else:
        app.append_to_file(text=app.merge_candidate, section="MERGE")
        app.merge_candidate_entry.delete(first=0, last=END)
        info(f"New Merge Candidate recorded: {app.merge_candidate}")


# Initialize file & append processed ID's under their appropriate headers
def append_to_file(app, text, section):
    # Create file name
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y.%m.%d")
    app.filepath = f"{formatted_time}.approvals.txt"

    # Initialize file & save initial state if undo_stack is empty
    if not app.undo_stack:
        initial_file_state = initialize_file(app.filepath)
        app.undo_stack.append(initial_file_state)

    try:
        # Save current file & display state to undo stack
        current_state = save_current_state(app, app.filepath)
        app.undo_stack.append(current_state)

        # Clear the redo stack because a new action was taken
        app.redo_stack.clear()

        with open(app.filepath, "r+") as file:
            # Read & process file contents
            lines = file.readlines()

            # Find correct index to insert id under headers
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

            # Insert new entry under correct header
            lines.insert(section_index, text + "\n")

            # Bring pointer back to start of file
            file.seek(0)
            file.writelines(lines)

            info(f"Appended to file: {text}")

        # Update text display with new ID
        app.text_display.insert(END, text + "\n", "center")
        app.text_display.see(END)

    except FileNotFoundError:
        # If file doesn't exist, initialize it
        initial_state = initialize_file(app.filepath)
        app.undo_stack.append((initial_state, ["\n"]))

        with open(app.filepath, "r+") as file:
            # Append text to correct section
            lines = file.readlines()

            # Find line index of header
            if section == "APPROVALS":
                section_index = lines.index("APPROVALS\n") + 2
            elif section == "NEW_MASTERS":
                section_index = lines.index("NEW_MASTERS\n") + 2
            elif section == "SPLIT":
                section_index = lines.index("SPLIT\n") + 2
            elif section == "MERGE":
                section_index = lines.index("MERGE\n") + 2

            # Insert new entry under correct header
            lines.insert(section_index, text + "\n")

            # Write updated content back to file
            file.seek(0)
            file.writelines(lines)

        info(f"Created file and appended to {section}: {text}")

        # Update the text display
        app.text_display.insert(END, text + "\n", "center")
        app.text_display.see(END)

    # After appending, make sure to update button states
    app.update_button_states()

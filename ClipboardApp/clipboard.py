from tkinter import NORMAL
from logging import info, error, debug
from time import sleep
from pyperclip import paste


def check_clipboard(app) -> None:
    # Continuously check clipboard for changes
    debug("Entered check_clipboard loop")

    while app.running:
        try:
            # Get current clipboard content
            app.current_clipboard = paste().strip()
            debug(f"Current clipboard content: {app.current_clipboard}")

            # Check clipboard content is not previous 'master_id', not just whitespace, & is new
            if app.current_clipboard != app.master_id and \
                    app.current_clipboard != app.previous_clipboard:
                info(f"New clipboard content detected: {app.current_clipboard}")

                if not app.current_clipboard == "":
                    # Process 'master_id'
                    app.process_master_id(unique_id=app.current_clipboard)

                    # Update 'previous_clipboard' content
                    app.previous_clipboard = app.current_clipboard

        # Handle exceptions during clipboard checking
        except Exception as e:
            error(f"Error checking clipboard: {e}")

        # Sleep for 100 milliseconds before rechecking
        sleep(0.1)


# Functionality for processing & combining copied 'master_id's
def process_master_id(app, unique_id: str) -> None:
    debug(f"process_identifier called with unique_id: {unique_id}")
    # Delay to ensure file accessibility
    sleep(0.1)
    try:
        # Combine master ID with unique ID & append to file
        combined_id = f"{app.master_id} ({unique_id})"
        info(f"Processing identifier: {combined_id}")

        # Store the last processed entry
        app.last_processed_entry = combined_id

        # Append combined ids
        app.append_to_file(text=combined_id, section="APPROVALS")

        # Enable Duplicate Entry button when a new ID was created
        app.duplicate_entry_button.config(state=NORMAL)

        # Check if master ID is unique & update unique id counter
        if app.master_id not in app.unique_master_ids:
            app.unique_master_ids.add(app.master_id)
            app.master_id_counter += 1
            app.update_counter_label()

    except Exception as e:
        error(f"Error processing identifier: {e}")



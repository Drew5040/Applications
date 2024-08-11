from logging import info, error, debug
from time import sleep
from pyperclip import paste


def check_clipboard(app):
    # Continuously check clipboard for changes
    debug("Entered check_clipboard loop")
    while app.running:
        try:
            # Get current clipboard content
            app.current_clipboard = paste().strip()
            debug(f"Current clipboard content: {app.current_clipboard}")
            # Check clipboard content is not master id being processed, not just whitespace, and is new
            if app.current_clipboard != app.master_id.strip() and app.current_clipboard.strip() and \
                    app.current_clipboard != app.previous_clipboard:
                info(f"New clipboard content detected: {app.current_clipboard}")
                app.process_master_id(unique_id=app.current_clipboard.strip())
                # Update previous clipboard content
                app.previous_clipboard = app.current_clipboard
        except Exception as e:
            error(f"Error checking clipboard: {e}")
        # Sleep for 100 milliseconds
        sleep(0.1)

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

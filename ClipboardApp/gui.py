from datetime import datetime
from tkinter import ttk, Text, DISABLED, messagebox
from ttkthemes import ThemedTk
from screeninfo import get_monitors
from context_menu import create_context_menu, highlight_text, bind_context_menu
from update import open_file, update_directory_label


# Working directory message for .after() method
def working_directory_msg(app) -> None:
    # Show confirmation message & log the change
    msg = messagebox.showinfo("Working Directory", "Please set working directory before proceeding.")


# Set size of GUI & make it fixed
def set_window_size(app) -> None:
    app.root.geometry("544x792")
    app.root.resizable(False, False)


# Decide if app is the topmost application depending on monitor
def adjust_topmost(app) -> None:
    # Get window position
    x = app.root.winfo_x()

    # Iterate over list of monitors
    for index, monitor in enumerate(get_monitors()):
        # Check if top left-most corner of GUI falls between left & right edge of monitor
        if monitor.x <= x <= monitor.x + monitor.width:
            # If it's on the second monitor (index > 0), always keep GUI on top
            if index > 0:
                app.root.attributes('-topmost', True)
            else:
                # If GUI is on the first (primary) monitor, don't
                app.root.attributes('-topmost', False)


# Close application if left open at 5:30pm
def check_time_and_close(root: ThemedTk, target_hour: int, target_minute: int) -> None:
    current_time = datetime.now()
    if current_time.hour == target_hour and current_time.minute >= target_minute:
        root.quit()
    else:
        root.after(60000, check_time_and_close, root, target_hour, target_minute)


# Create & place Label, Entry field, & Button to set master ID
def set_master_id(app) -> None:
    ttk.Label(
        master=app.root,
        text="Master ID:",
        style="Custom.TLabel"
    ).grid(row=0, column=0, padx=10, pady=10)
    app.master_id_entry = ttk.Entry(master=app.root, width=50, style="Custom.TEntry")
    app.master_id_entry.grid(row=0, column=1, padx=10, pady=10)
    app.master_id_entry.bind('<FocusIn>', highlight_text)
    create_context_menu(app.root, app.master_id_entry)
    ttk.Button(
        master=app.root,
        text="Set Master ID",
        command=app.set_master_id
    ).grid(row=0, column=2, padx=10, pady=10)


# Create & place Label, Entry field, & Button to record new master ID
def new_master_id(app) -> None:
    ttk.Label(
        master=app.root,
        text="New Master ID:",
        style="Custom.TLabel"
    ).grid(row=1, column=0, padx=10, pady=10)
    app.new_master_id_entry = ttk.Entry(master=app.root, width=50, style="Custom.TEntry")
    app.new_master_id_entry.grid(row=1, column=1, padx=10, pady=10)
    app.new_master_id_entry.bind('<FocusIn>', highlight_text)
    create_context_menu(app.root, app.new_master_id_entry)
    ttk.Button(
        master=app.root,
        text="append",
        command=app.append_new_master_id
    ).grid(row=1, column=2, padx=10, pady=10)


# Create & place Label, Entry field, & Button to record new split candidate
def split_candidate(app) -> None:
    ttk.Label(
        master=app.root,
        text="Split Candidate:",
        style="Custom.TLabel"
    ).grid(row=2, column=0, padx=10, pady=10)
    app.split_candidate_entry = ttk.Entry(master=app.root, width=50, style="Custom.TEntry")
    app.split_candidate_entry.grid(row=2, column=1, padx=10, pady=10)
    app.split_candidate_entry.bind('<FocusIn>', highlight_text)
    create_context_menu(app.root, app.split_candidate_entry)
    ttk.Button(
        master=app.root,
        text="append",
        command=app.append_split_candidate
    ).grid(row=2, column=2, padx=10, pady=10)


# Create & place Label, Entry field, & Button to record new merge candidate
def merge_candidate(app) -> None:
    ttk.Label(
        master=app.root,
        text="Merge Candidate:",
        style="Custom.TLabel"
    ).grid(row=3, column=0, padx=10, pady=10)
    app.merge_candidate_entry = ttk.Entry(master=app.root, width=50, style="Custom.TEntry")
    app.merge_candidate_entry.grid(row=3, column=1, padx=10, pady=10)
    app.merge_candidate_entry.bind('<FocusIn>', highlight_text)
    create_context_menu(app.root, app.merge_candidate_entry)
    ttk.Button(
        master=app.root,
        text="append",
        command=app.append_merge_candidate
    ).grid(row=3, column=2, padx=10, pady=10)


# Create & place start & stop buttons
def start_and_stop_buttons(app) -> None:
    frame1 = ttk.Frame(app.root, style="Custom.TFrame")
    frame1.grid(row=4, column=0, columnspan=3, pady=10)
    app.start_button = ttk.Button(master=frame1, text="Start Listening", command=app.start_listening)
    app.start_button.grid(row=0, column=0, padx=10)
    app.stop_button = ttk.Button(
        master=frame1, text="Stop Listening", command=app.stop_listening, state=DISABLED
    )
    app.stop_button.grid(row=0, column=1, padx=10)


# Create, place, & style thread status label
def thread_status_label(app) -> None:
    status_frame = ttk.Frame(app.root, style="Custom.TFrame")
    status_frame.grid(row=6, column=0, columnspan=3, pady=10)
    app.status_label = Text(
        status_frame, height=1, width=20, borderwidth=0, background=app.root.cget("background")
    )
    app.status_label.grid(row=0, column=0, sticky="ew")
    app.status_label.tag_configure("black", foreground="black")
    app.status_label.tag_configure("red", foreground="red")
    app.status_label.tag_configure("green", foreground="green")
    app.status_label.insert("1.0", "   Status: ", "black")
    app.status_label.insert("end", "STOPPED", "red")
    app.status_label.config(state=DISABLED)


# Create & place unique master ID counter label
def unique_master_id_label(app) -> None:
    app.counter_label = ttk.Label(
        master=app.root, text="Unique Master IDs processed today: 0", style="Custom.TLabel"
    )
    app.counter_label.grid(row=7, column=0, columnspan=3, pady=10)


# Create & place undo/redo buttons
def edit_buttons(app) -> None:
    frame2 = ttk.Frame(app.root, style="Custom.TFrame")
    frame2.grid(row=8, column=0, columnspan=3, pady=10)
    app.redo_button = ttk.Button(master=frame2, text="<<<", command=lambda: app.undo_last_action())
    app.redo_button.grid(row=0, column=0, padx=10)
    app.duplicate_entry_button = ttk.Button(master=frame2, text="Duplicate Entry", command=app.append_duplicate_entry)
    app.duplicate_entry_button.grid(row=0, column=1, pady=10)
    app.undo_button = ttk.Button(master=frame2, text=">>>", command=lambda: app.redo_last_action())
    app.undo_button.grid(row=0, column=2, padx=10)


# Create & place ID display
def id_display(app) -> None:
    app.text_display = Text(master=app.root, height=5, width=30, undo=True)
    app.text_display.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    app.text_display.tag_configure(tagName="center", justify="center")


# Create & place note display with a Label
def note_display(app) -> None:
    app.append_note_button = ttk.Button(master=app.root, text="append_note", command=app.append_note)
    app.append_note_button.grid(row=10, column=1, padx=10, sticky="ew")
    app.note_display = Text(master=app.root, height=8, width=30, undo=True)
    app.note_display.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="ew")


# Create & place set working directory button
def set_working_directory_button(app) -> None:
    app.dir_button = ttk.Button(
        master=app.root, text="Change Working Directory", command=app.set_working_directory
    )
    app.dir_button.grid(row=12, column=0, columnspan=3, pady=10)


def open_file_button(app) -> None:
    app.open_file_button = ttk.Button(
        master=app.root, text="Open File", command=open_file
    )
    app.open_file_button.grid(row=13, column=0, columnspan=3, pady=10)


# Create & place working directory label
def working_directory_label(app) -> None:
    app.dir_label = ttk.Label(master=app.root, text='Initializing...', style="Custom.TLabel")
    app.dir_label.grid(row=14, column=0, columnspan=3, padx=20, pady=10)
    update_directory_label(app)


# Initialize GUI components
def setup_gui(app) -> None:
    set_window_size(app)
    set_master_id(app)
    new_master_id(app)
    split_candidate(app)
    merge_candidate(app)
    start_and_stop_buttons(app)
    thread_status_label(app)
    unique_master_id_label(app)
    edit_buttons(app)
    id_display(app)
    note_display(app)
    set_working_directory_button(app)
    open_file_button(app)
    working_directory_label(app)

    # Bind context menu's to Entry widgets
    widgets = [
        app.master_id_entry,
        app.new_master_id_entry,
        app.split_candidate_entry,
        app.merge_candidate_entry,
        app.note_display,
    ]

    bind_context_menu(app.root, widgets)

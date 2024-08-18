from tkinter import Menu, END


# Create a context menu for 'Copy', 'Cut', & 'Paste'
def create_context_menu(root, widget):
    # Initialize context 'menu' with 'root' as master
    menu = Menu(master=root, tearoff=0)

    # Add 'Copy' command to 'menu'
    menu.add_command(label="copy", command=lambda: widget.event_generate("<<Copy>>"))

    # Add 'Cut' command to 'menu'
    menu.add_command(label="cut", command=lambda: widget.event_generate("<<Cut>>"))

    # Add 'Paste' command to 'menu'
    menu.add_command(label="paste", command=lambda: widget.event_generate("<<Paste>>"))

    # Add 'Clear' command to 'menu' to delete all text in 'widget'
    menu.add_command(label="clear", command=lambda: widget.delete(0, END))

    # Bind right-click ('<Button-3>') to display the 'menu'
    widget.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))


# Set highlighting in 'Entry' fields
def highlight_text(event):
    # Select all text in the 'Entry' field
    event.widget.select_range(0, 'end')

    # Move the cursor to the end of the text
    event.widget.icursor('end')


# Bind context menu to individual 'Entry' widgets
def bind_context_menu(root, widgets):
    # Iterate over each 'widget' in 'widgets' list
    for widget in widgets:
        # Create context menu & bind it to 'widget'
        create_context_menu(root, widget)

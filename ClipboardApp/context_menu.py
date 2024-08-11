from tkinter import Menu, END


# Create a context menu for Copy, Cut, & Paste
def create_context_menu(root, widget):
    menu = Menu(master=root, tearoff=0)
    menu.add_command(label="copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="paste", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="clear", command=lambda: widget.delete(0, END))
    widget.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))


# Set highlighting in Entry fields
def highlight_text(event):
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')


# Bind context menu's to individual Entry widgets
def bind_context_menu(root, widgets):
    for widget in widgets:
        create_context_menu(root, widget)

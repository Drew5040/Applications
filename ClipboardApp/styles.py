from tkinter import ttk


# Initialize 'style' & set background color for frames & labels
def style_gui(app):
    # Create style object for the application
    app.style = ttk.Style()

    # Get background color of root window
    app.bg_color = app.root.cget("background")

    # Configure 'Custom.TFrame' style with background color
    app.style.configure("Custom.TFrame", background=app.bg_color)

    # Configure 'Custom.TLabel' style with background color & black text
    app.style.configure("Custom.TLabel", background=app.bg_color, foreground="black")

    # Configure 'Custom.TEntry' style with background color & black text
    app.style.configure(
        "Custom.TEntry",
        fieldbackground=app.bg_color,
        background=app.bg_color,
        foreground="black"
    )


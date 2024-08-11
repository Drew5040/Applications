from tkinter import ttk


# Initialize the style & set the background color for frames and labels
def widget_styling(app):
    app.style = ttk.Style()
    app.bg_color = app.root.cget("background")
    app.style.configure("Custom.TFrame", background=app.bg_color)
    app.style.configure("Custom.TLabel", background=app.bg_color, foreground="black")

    app.style.configure(
        "Custom.TEntry",
        fieldbackground=app.bg_color,
        background=app.bg_color,
        foreground="black"
    )

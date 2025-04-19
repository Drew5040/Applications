from tkinter import Tk, Entry, Button, Checkbutton, Label, StringVar, BooleanVar, messagebox
from conversion import convert_currency
from clipboard_features import ClipboardFeatures
from config import load_api_key
from reportlab.pdfgen import canvas
from config import save_api_key
from os import startfile
from os import path, getenv
from os.path import exists
from typing import Tuple
from datetime import datetime, time
from logs import log_conversion, log_error
import logging
from logging.handlers import RotatingFileHandler
import time
import tempfile


def create_gui() -> Tuple[StringVar, StringVar, StringVar, StringVar, StringVar]:
    """
       Create a Currency Converter GUI using Tkinter.

       This GUI allows users to input an API key, source currency, target currency, and amount.
       It performs currency conversion using the FreeCurrencyAPI and displays the result.
       Users can also save the conversion result as a PDF.

       Returns:
       tuple: A tuple containing Tkinter variables (api_key_var, source_currency_var, target_currency_var,
              amount_var, result_var).

       Example:
       api_key_var, source_currency_var, target_currency_var, amount_var, result_var = create_gui()

       """
    # Create GUI window
    root = Tk()
    # Title of GUI window
    root.title("Anwoo's Currency Converter")

    def is_valid_currency(currency: str) -> bool:
        currency_symbols = [
            'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'CNY', 'INR', 'BRL',
            'ZAR', 'RUB', 'MXN', 'SGD', 'HKD', 'NZD', 'SEK', 'NOK', 'DKK', 'TRY',
            'ARS', 'CLP', 'COP', 'EGP', 'IDR', 'MYR', 'THB', 'KRW', 'ILS', 'SAR',
            'AED', 'CHF'
        ]

        if currency in currency_symbols:
            return True
        else:
            return False

    def is_valid_amount(amount: str) -> bool:
        try:
            float_amount = float(amount)
            return True
        except ValueError as e:
            # Log the error
            log_error(type(e).__name__, str(e))
            return False

    def convert_button_clicked():
        # Check if all entry fields are filled, if not produce error box
        if check_entry_fields_are_filled():
            # If all entry fields are filled get the source_currency Tkinter variable
            source_currency_str = source_currency_var.get()

            target_currency_str = target_currency_var.get()

            # If all entry fields are filled get the target_currency Tkinter variable
            amount_str = amount_var.get()

            if not is_valid_amount(amount_str):
                messagebox.showerror('Error', 'Invalid amount')
                return None
            else:
                amount = float(amount_str)

            if not is_valid_currency(source_currency_str):
                messagebox.showerror('Error', 'invalid  source currency')
                return None

            if not is_valid_currency(target_currency_str):
                messagebox.showerror('Error', 'invalid target currency')
                return None

            # Run the convert_currency() function
            converted_amount = convert_currency(api_key_var.get(), source_currency_str, target_currency_str, amount)

            # Set the result variable if one is returned
            if converted_amount is not None:
                result_var.set(f'{amount} {source_currency_str} = {converted_amount:.5f} {target_currency_str}')
                log_conversion(source_currency_str, target_currency_str, amount_str, converted_amount)
                return True
            else:
                # If there is no conversion set result var to string
                result_var.set('Failed to fetch exchange rate')
                return False

    def cancel_button_clicked() -> None:
        # Close window when cancel button is clicked
        root.destroy()

    def open_pdf(pdf_file_path: str) -> None:
        try:
            # Open the PDF with the default PDF viewer
            startfile(pdf_file_path)
        # Raise exception if file does not exist
        except FileNotFoundError as e:
            # Log the error
            log_error(type(e).__name__, str(e))
            # Print the error
            print(f"Error opening PDF: {e}")

    def print_pdf() -> None:
        # Check if all entry fields are filled prior to printing
        if check_entry_fields_are_filled():
            result_text = result_var.get()
            filename = f'Currency_Conversion_{source_currency_var.get()}_to_{target_currency_var.get()}'

            # Create a temporary text file to store the result
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
                temp_file_path = temp_file.name

                try:
                    # Write the result to the temporary file
                    temp_file.write(result_text)

                    # Create PDF file
                    pdf_file_path = temp_file_path.replace('.txt', f'_{filename}.pdf')
                    pdf = canvas.Canvas(pdf_file_path)
                    pdf_file_title = filename
                    pdf.setTitle(pdf_file_title)

                    # Write the results to PDF file
                    try:

                        for line_num in range(10):
                            pdf.drawCentredString(x=10, y=10, text=" ")
                            if line_num == 7:
                                pdf.drawCentredString(x=300, y=600,
                                                      text=f'Timestamp: {datetime.fromtimestamp(time.time())}')
                            elif line_num == 8:
                                pdf.drawCentredString(x=300, y=580, text='Conversion done by: '
                                                                         'https://api.freecurrencyapi.com/v1/latest')
                        # Set size and font of PDF file
                        pdf.setFont(psfontname='Helvetica', size=18)
                        pdf.drawCentredString(x=300, y=560, text=result_text)

                    # Catch various exceptions if they occur
                    except Exception as e:
                        # Log the error
                        log_error(type(e).__name__, str(e))
                        print(f"Error during PDF creation: {e}")

                    finally:
                        # Save the PDF
                        pdf.save()
                        print(f'Result saved to {pdf_file_path}')

                except IOError as e:
                    # Log the error
                    log_error(type(e).__name__, str(e))
                    print(f"IOError while writing to temporary file: {e}")

                except UnicodeEncodeError as e:
                    # Log the error
                    log_error(type(e).__name__, str(e))
                    print(f"UnicodeEncodeError while writing to temporary file: {e}")

                finally:
                    # Delete the temporary txt file
                    temp_file.close()

            # Open the PDF
            open_pdf(pdf_file_path)

    def check_entry_fields_are_filled() -> bool:
        # Check if all entry fields are filled
        if not api_key_var.get() or not source_currency_var.get() or not target_currency_var.get() or not amount_var.get():
            # If any field is missing, show an error message
            messagebox.showerror("Error", "All fields must be filled.")
            return False
        else:
            return True

    # Tkinter input variables from entry fields
    api_key_var = StringVar()
    source_currency_var = StringVar()
    target_currency_var = StringVar()
    amount_var = StringVar()
    result_var = StringVar()
    remember_var = BooleanVar()

    # Load the API key when the GUI is created
    config_file_path = path.join(getenv('APPDATA'), "Anwoo's Currency Converter Tool", 'config.json')
    if exists(config_file_path):
        loaded_api_key = load_api_key()

        if loaded_api_key:
            api_key_var.set(loaded_api_key)

    # API-Key entry field
    api_key_label = Label(root, text='API Key: ')
    api_key_label.grid(row=0, column=0, padx=5, pady=5)
    api_key_entry = Entry(root, textvariable=api_key_var, state='normal')
    api_key_entry.grid(row=0, column=1, padx=5, pady=5)

    # If API key was already saved and loaded into entry field, switch entry field to read-only
    if exists(config_file_path):
        api_key_entry.configure(state='readonly')

    # Source currency entry field
    source_currency_label = Label(root, text='Source Currency: ')
    source_currency_label.grid(row=1, column=0, padx=5, pady=5)
    source_currency_entry = Entry(root, textvariable=source_currency_var, state='normal')
    source_currency_entry.grid(row=1, column=1, padx=5, pady=5)

    # Target currency entry field
    target_currency_label = Label(root, text='Target Currency: ')
    target_currency_label.grid(row=2, column=0, padx=5, pady=5)
    target_currency_entry = Entry(root, textvariable=target_currency_var, state='normal')
    target_currency_entry.grid(row=2, column=1, padx=5, pady=5)

    # Amount entry field
    amount_label = Label(root, text='Amount: ')
    amount_label.grid(row=3, column=0, padx=5, pady=5)
    amount_entry = Entry(root, textvariable=amount_var, state='normal')
    amount_entry.grid(row=3, column=1, padx=5, pady=5)

    # Instantiate ClipboardFeatures and pass the entry widget
    ClipboardFeatures(api_key_entry, root)
    ClipboardFeatures(source_currency_entry, root)
    ClipboardFeatures(target_currency_entry, root)
    ClipboardFeatures(amount_entry, root)

    # Save API-Key checkbox
    remember_checkbox = Checkbutton(root, text='Remember API Key',
                                    variable=remember_var,
                                    command=lambda: save_api_key(api_key_var, remember_var))
    remember_checkbox.grid(row=4, column=0, columnspan=2, pady=10)

    # 'Convert' call-to-action button
    convert_button = Button(root, text='Convert', command=convert_button_clicked)
    convert_button.grid(row=5, column=0, columnspan=1, pady=1)

    # Open PDF button
    print_button = Button(root, text='Open PDF', command=print_pdf)
    print_button.grid(row=5, column=1, columnspan=2, pady=10)

    # 'Edit' button to enable editing of API key
    edit_button = Button(root, text='Edit', command=lambda: api_key_entry.config(state='normal'))
    edit_button.grid(row=6, column=0, columnspan=1, pady=1)

    # 'Cancel' call-to-action button
    close_button = Button(root, text='Close', command=cancel_button_clicked)
    close_button.grid(row=6, column=1, columnspan=2, pady=10)

    # Print result to GUI
    result_label = Label(root, textvariable=result_var)
    result_label.grid(row=8, column=0, columnspan=2, pady=5)

    # Open GUI
    root.mainloop()

    return api_key_var, source_currency_var, target_currency_var, amount_var, result_var

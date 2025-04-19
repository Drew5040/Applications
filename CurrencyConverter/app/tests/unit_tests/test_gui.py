import pytest
from tkinter import Tk, StringVar
from unittest.mock import patch
from app.gui import create_gui

# Disable GUI during test run
Tk().withdraw()


@pytest.fixture
def tk_variables():
    # Create a Tkinter root window
    root = Tk()

    return {
        'api_key_var': StringVar(master=root),
        'source_currency_var': StringVar(master=root),
        'target_currency_var': StringVar(master=root),
        'amount_var': StringVar(master=root),
        'result_var': StringVar(master=root),
    }


@patch('app.exchange.convert_currency')
def test_convert_button_clicked(mock_convert_currency, tk_variables):
    # Create GUI with the provided Tkinter variables
    api_key_var, source_currency_var, target_currency_var, amount_var, result_var = create_gui()

    # Set values in the entry fields
    api_key_var.set('7b12344eb6334444a9d975149ff5ac4b')
    source_currency_var.set('USD')
    target_currency_var.set('EUR')
    amount_var.set(100)

    # Mock the convert_currency function
    mock_convert_currency.return_var = 91.27

    # Trigger the button click
    create_gui().convert_button_clicked()

    # Assert the result_var is updated as expected
    expected_result = '100 USD is = 91.27'
    assert result_var.get() == expected_result

    # Assert that convert_currency was called with the expected args
    mock_convert_currency.assert_called_once_with('7b12344eb6334444a9d975149ff5ac4b')

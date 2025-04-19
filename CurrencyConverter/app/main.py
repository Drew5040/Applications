from argparse import ArgumentParser
from sys import argv
from conversion import convert_currency
from gui import create_gui
from logs import log_conversion


def main():
    # Check len of command-line argument list
    if len(argv) == 1:

        # No command-line arguments
        print("Running in GUI mode...")

        # Open GUI
        create_gui()

    else:
        # Parse command-line arguments
        print("Running in command-line mode...")

        # Create argument parser object
        parser = ArgumentParser(description="Anwoo's Currency Converter Tool")

        # Add command line arguments
        parser.add_argument('--api_key', required=True, help='Your API key for the currency exchange service')
        parser.add_argument('--source_currency', required=True, help='Source currency code')
        parser.add_argument('--target_currency', required=True, help='Target currency code')
        parser.add_argument('--amount', type=float, required=True, help='Amount to convert')

        # Parse command-line arguments
        args = parser.parse_args()

        # Start conversion
        converted_amount = convert_currency(args.api_key, args.source_currency, args.target_currency, args.amount)

        # Display conversion result
        if converted_amount is not None:
            print(f'{args.amount} {args.source_currency:.5f} is = {converted_amount:.5f} {args.target_currency}')
            log_conversion(args.source_currency, args.target_currency, args.amount, converted_amount)
        else:
            print('Failed to fetch exchange rate')


# Run the script
if __name__ == '__main__':
    main()

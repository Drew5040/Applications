from datetime import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
from os import path, makedirs

# Define the app directory and log file path
home_dir = path.expanduser('~')
app_dir = path.join(home_dir, ".anwoo")
log_file_path = path.join(app_dir, 'anwoo_log.log')

# Check if directory exists, if not create it
if not path.exists(log_file_path):
    makedirs(app_dir)

    # Check if log file exits, if not, create an empty log file
    with open(log_file_path, 'w'):
        pass

# Configure the logging settings
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    handlers=[RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=5)],
    level=logging.INFO,
    format=log_format,
)


def log_conversion(source_currency, target_currency, amount, converted_amount):
    # Log conversion details
    conversion_details = (f'{source_currency} to {target_currency}, '
                          f'Amount:{amount} '
                          f'Converted: {converted_amount}')

    logging.info(conversion_details)


def log_error(exception_type, exception_message):
    # Log error details
    error_details = f'Error: {exception_type}, Message: {exception_message}'
    logging.error(error_details)

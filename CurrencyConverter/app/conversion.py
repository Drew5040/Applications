import requests
from typing import Optional


def get_exchange_rate(api_key: str, source_currency: str, target_currency: str) -> Optional[float]:
    """""
        Retrieve the exchange rate between two currencies using the FreeCurrencyAPI.

        Parameters:
        - api_key (str): The API key for accessing the FreeCurrencyAPI.
        - source_currency (str): The currency code of the source currency.
        - target_currency (str): The currency code of the target currency.

        Returns:
        float: The exchange rate from source_currency to target_currency.

        Raises:
        - ConnectionError: If there is an issue connecting to the API.
        - ValueError: If the API response is not successful or the currencies are not valid.

        Example:
        api_key = 'your_api_key'
        source_currency = 'USD'
        target_currency = 'EUR'
        rate = get_exchange_rate(api_key, source_currency, target_currency)
        print(rate)
        0.85
        """""
    # Create URL variable
    url = 'https://api.freecurrencyapi.com/v1/latest'
    # Create headers for API request
    headers = {'apikey': api_key}
    # Create params dict for API request
    params = {'base_currency': source_currency, 'symbols': target_currency}
    # Make request and get response
    response = requests.get(url, headers=headers, params=params)
    # Check if response is successful (status code 200)
    if response.status_code == 200:
        # Parse response as a json object
        data = response.json()
        # Return exchange rate for the target currency
        return data['data'][target_currency]
    else:
        # If response is not 200, print error message
        print(f'Error: {response.status_code}, {response.text}')


def convert_currency(api_key: str, source_currency: str, target_currency: str, amount: float) -> Optional[float]:
    """
       Convert a specified amount from one currency to another using the FreeCurrencyAPI.

       Parameters:
       - api_key (str): The API key for accessing the FreeCurrencyAPI.
       - source_currency (str): The currency code of the source currency.
       - target_currency (str): The currency code of the target currency.
       - amount (float): The amount to be converted.

       Returns:
       float or None: The converted amount if the conversion is successful, None otherwise.

       Raises:
       - ConnectionError: If there is an issue connecting to the API.
       - ValueError: If the API response is not successful or the currencies are not valid.

       Example:
       api_key = 'your_api_key'
       source_currency = 'USD'
       target_currency = 'EUR'
       amount = 100.0
       converted_amount = convert_currency(api_key, source_currency, target_currency, amount)
       print(converted_amount)
       85.0
       """
    # Get the exchange rate
    exchange_rate = get_exchange_rate(api_key, source_currency, target_currency)
    # Check if there is an exchange rate to perform calculations on
    if exchange_rate is not None:
        # Convert the amount
        converted_amount = amount * exchange_rate
        # Return the converted amount
        return converted_amount
    else:
        # Return None if there is not an exchange rate
        return None

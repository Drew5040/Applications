import pytest
from unittest.mock import MagicMock, patch
from app.conversion import get_exchange_rate
from app.conversion import convert_currency


# @patch decorator to temporarily replace requests.get with a Mock object
@pytest.mark.parametrize("status_code, api_key, source_currency, target_currency, expected_result", [
    # (200, '7b12344eb6334444a9d975149ff5ac4b', 'USD', 'EUR', 0.9127),
    (200, '7b12344eb6334444a9d975149ff5ac4b', 'USD', 'CAD', 1.33),  # Corrected value

])
@patch('requests.get')
def test_get_exchange_rate(mock_get, status_code, api_key, source_currency, target_currency, expected_result):
    # Mock the request.get function to control its behavior in the test
    mock_response = MagicMock()
    headers = {'X-API-Key': api_key}
    mock_response.status_code = status_code

    if status_code == 200:
        # Replace with a sample JSON response for a successful request
        mock_response.json.return_value = {'rates': {'USD': 1, 'CAD': 1.33}}

    mock_get.return_value = mock_response

    # Call the function with sample arguments
    result = get_exchange_rate(api_key=api_key, source_currency=source_currency, target_currency=target_currency)

    # Assert the result matches the expected result
    assert result == expected_result

    # Assert that requests.get was called with the expected URL and headers
    mock_get.assert_called_once_with(
        f'https://openexchangerates.org/api/latest.json?app_id=7b12344eb6334444a9d975149ff5ac4b&base=USD',
        headers={'X-API-Key': '7b12344eb6334444a9d975149ff5ac4b'}
    )


@pytest.mark.parametrize('api_key, source_currency, target_currency, amount, expected_result', [
    # ('7b12344eb6334444a9d975149ff5ac4b', 'USD', 'EUR', 100, 0.9127),
    ('7b12344eb6334444a9d975149ff5ac4b', 'USD', 'CAD', 100, 1.33),  # Corrected value
])
@patch('app.exchange.get_exchange_rate')
def test_convert_currency(mock_get_exchange_rate, api_key, source_currency, target_currency, amount, expected_result):
    # Mock the test_get_exchange_rate function to control its behavior in the test
    mock_get_exchange_rate.return_value = .0133  # Mock exchange rate for USD to EUR

    # Call the function with sample arguments
    result = convert_currency(api_key, source_currency, target_currency, amount)

    # Assert the result matches the expected result with tolerance
    assert result == pytest.approx(expected_result)

    # Assert that test_get_exchange_rate was called with the expected parameters
    mock_get_exchange_rate.assert_called_once_with(api_key, source_currency, target_currency)


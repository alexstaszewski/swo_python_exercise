# Used a library to get the current exchange rates
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from decimal import Decimal

from . import abc
import json
import os

class Currency(abc.Currency):
    def __init__(self):
        self._currencies = dict()
        self._currencies_json = "C:\\Users\\Alex\\Documents\\GitHub\\swo_python_exercise\\data\\currencies.json"
        self._currency_rates = CurrencyRates()
        self._currency_codes = CurrencyCodes()

    # A function that creates a currencies.json file if it doesn't exist
    # or updates an existing one
    # Defaults to euro, but can be specified
    # I do not call this because its slow to do everytime, but can be called if you want to update the list
    def update_currencies(self, currency : str = "EUR"):
        # Create the currencies json file if it does not exist
        with open(self._currencies_json, 'w+') as json_file:
            #currencies_json = json.loads(json_file.read())

            # Get a dictionary of all the currency exchange rates in comparison to the base currency
            currency_dict = self._currency_rates.get_rates(currency)
            # Update it to include the base currency at a rate of 1 (since it is being compared against itself)
            currency_dict[currency] = 1.0

            # Write to JSON
            json_file.write(json.dumps(currency_dict))

    # Function to convert one currency to another
    def convert(self, origin: str, destination: str, amount:float) -> float:
        with open(self._currencies_json, 'r') as json_file:
            currencies_json = json.loads(json_file.read())

        # Make sure the currency code is in the dictionary
        try:
            origin_rate = currencies_json[origin.upper()]
            destination_rate = currencies_json[destination.upper()]
        except Exception as e:
            print(e)

        # Convert the value from the origin currnecy into destination currency
        # A bit inaccurate though but mainly for demonstration purposes
        converted_value = (amount/origin_rate) * destination_rate

        return converted_value

    # Function to get the currency symbol for a currency
    def _get_currency_symbol(self, code: str) -> str:
        return self._currency_codes.get_symbol(code.upper())




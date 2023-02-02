import typing
import json


from . import abc
from shoppingcart.currency import Currency



class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = dict()
        self._prices_json = "../data/prices.json"
        self._default_currency = "EUR"
        self._currency = Currency()

    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

            # Added a line to pop the newly added item and re-append it
            # so it is at the bottom of the list
            self._items[product_code] = self._items.pop(product_code)

    # Added a field to signify which currency to print the receipt in, it defaults to euro
    # The default currency (self._default_currency) should be euro (eur)
    def print_receipt(self, currency : str ="EUR") -> typing.List[str]:
        lines = []
        # To make the currency code consistent
        currency = currency.upper()

        total_price = 0
        total_count = 0

        # Get the currency symbol
        currency_symbol = self._currency._get_currency_symbol(currency)

        for item in self._items.items():
            if currency != self._default_currency:
                price = self._currency.convert(self._default_currency, currency, self._get_product_price(item[0])) * item[1]
            else:
                price = self._get_product_price(item[0]) * item[1]

            total_price += price
            total_count += item[1]

            price_string = "%s%.2f" % (currency_symbol, price)

            lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)

        # Append a line to the very end for the total price + amount of items
        # (I added the amount of items for uniformity)
        lines.append("Total" + " - " + str(total_count) + ' - ' + "%s%.2f" % (currency_symbol, total_price))

        return lines

    def _get_product_price(self, product_code: str) -> float:
        # Read a JSON file with the prices
        # If the product does not exist, set the price to 0
        # Prices are EURO
        with open(self._prices_json, 'r') as json_file:
            product_prices = json.loads(json_file.read())
        try:
            price = product_prices[product_code]
        except:
            price = 0.0

        return price

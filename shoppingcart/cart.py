import typing
import json

from . import abc


class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = dict()
        self._prices_json = "../data/prices.json"

    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

            # Added a line to pop the newly added item and re-append it
            # so it is at the bottom of the list
            self._items[product_code] = self._items.pop(product_code)

    def print_receipt(self) -> typing.List[str]:
        lines = []

        total_price = 0
        total_count = 0

        for item in self._items.items():
            price = self._get_product_price(item[0]) * item[1]
            total_price += price
            total_count += item[1]

            price_string = "€%.2f" % price

            lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)

        # Append a line to the very end for the total price + amount of items
        # (I added the amount of items for uniformity)
        lines.append("Total" + " - " + str(total_count) + ' - ' + "€%.2f" % total_price)

        return lines

    def _get_product_price(self, product_code: str) -> float:

        # Read a JSON file with the prices
        # If the product does not exist, set the price to 0
        with open(self._prices_json, 'r') as json_file:
            product_prices = json.loads(json_file.read())
        try:
            price = product_prices[product_code]
        except:
            price = 0.0


        return price

from shoppingcart.cart import ShoppingCart
import json
from forex_python.converter import CurrencyCodes

def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 1 - €1.00"
    assert receipt[-1] == "Total - 1 - €1.00"


def test_add_item_with_multiple_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 2)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 2 - €2.00"
    assert receipt[-1] == "Total - 2 - €2.00"


def test_add_different_items():
    cart = ShoppingCart()
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 1 - €1.10"
    assert receipt[1] == "kiwi - 1 - €3.00"
    assert receipt[-1] == "Total - 2 - €4.10"

# Add many items and items twice to see if its position is in the correct order
def test_add_many_twice():
    cart = ShoppingCart()
    cart.add_item("apple", 1)
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 1)
    cart.add_item("banana", 1)
    cart.add_item("apple", 2)

    receipt = cart.print_receipt()

    assert receipt[0] == "kiwi - 1 - €3.00"
    assert receipt[1] == "banana - 2 - €2.20"
    assert receipt[2] == "apple - 3 - €3.00"
    assert receipt[-1] == "Total - 6 - €8.20"


def test_total():
    cart = ShoppingCart()
    cart.add_item("apple", 1)
    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 1 - €1.00"
    assert receipt[-1] == "Total - 1 - €1.00"


def test_currency():
    cart = ShoppingCart()
    cart.add_item("apple", 1)

    receipt = cart.print_receipt("usd")
    assert receipt[0] == "apple - 1 - $1.08"
    assert receipt[-1] == "Total - 1 - $1.08"


def test_all_currencies():
    # Read all the currencies from the JSON (with their exchange rates against the euro)
    with open("../data/currencies.json", 'r') as json_file:
        currencies_json = json.loads(json_file.read())

    currency_codes = CurrencyCodes()

    # Loops through all currencies and checks their default values
    for currency in currencies_json:
        cart = ShoppingCart()
        cart.add_item("apple", 1)
        receipt = cart.print_receipt(currency)

        assert receipt[0] == "apple - 1 - %s%.2f" % (currency_codes.get_symbol(currency), currencies_json[currency])
        assert receipt[-1] == "Total - 1 - %s%.2f" % (currency_codes.get_symbol(currency), currencies_json[currency])


def test_add_invalid():
    cart = ShoppingCart()
    cart.add_item("wapple", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "wapple - 1 - €0.00"
    assert receipt[-1] == "Total - 1 - €0.00"


# To test them within the IDE
# test_add_item()
# test_add_item_with_multiple_quantity()
# test_add_different_items()
# test_add_many_twice()
# test_total()
# test_currency()
# test_all_currencies()
# test_add_invalid()
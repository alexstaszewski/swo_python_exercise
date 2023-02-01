
import abc
import typing


class ShoppingCart(abc.ABC):

    @abc.abstractmethod
    def add_item(self, product_code: str, quantity: int):
        pass

    @abc.abstractmethod
    def print_receipt(self) -> typing.List[str]:
        pass

class Currency(abc.ABC):
    @abc.abstractmethod
    def update_currencies(self, currency: str):
        pass

    @abc.abstractmethod
    def convert(self, origin: str, destination: str, amount: float):
        pass


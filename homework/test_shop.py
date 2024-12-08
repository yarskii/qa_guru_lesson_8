"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 99.99, "This is a book", 1000)


@pytest.fixture
def product_2():
    return Product("pen", 45.49, "This is a pen", 20)


@pytest.fixture
def cart(product):
    return Cart()


buy_product_count = 2
buy_product_2_count = 3


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1)
        assert product.check_quantity(product.quantity)
        assert not product.check_quantity(product.quantity + 1)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity_before = product.quantity
        product.buy(buy_product_count)
        assert product.quantity == quantity_before - buy_product_count

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_to_cart(self, cart, product):
        cart.add_product(product, buy_product_count)

        assert cart.products[product] == buy_product_count

    def test_add_product_insufficient_quantity(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)

    def test_remove_product_from_cart(self, cart, product):
        cart.add_product(product, buy_product_count)
        cart.remove_product(product, 1)

        assert cart.products[product] == 1

    def test_remove_one_product_from_cart(self, cart, product, product_2):
        cart.add_product(product, buy_product_count)
        cart.add_product(product_2, buy_product_count)
        cart.remove_product(product, 1)

        assert cart.products[product] == buy_product_count - 1
        assert cart.products[product_2] == buy_product_count

    def test_remove_over_product_from_cart(self, cart, product):
        cart.add_product(product, buy_product_count)
        cart.remove_product(product, remove_count=cart.products[product] + 1)

        assert cart.products == {}

    def test_remove_product_completely(self, cart, product):
        cart.add_product(product, buy_product_count)
        cart.remove_product(product)

        assert product not in cart.products

    def test_remove_two_products_completely(self, cart, product, product_2):
        cart.add_product(product, buy_product_count)
        cart.add_product(product_2, buy_product_count)
        cart.remove_product(product)

        assert product not in cart.products
        assert product_2 in cart.products

        cart.remove_product(product_2)

        assert product not in cart.products
        assert product_2 not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, buy_product_count)
        cart.clear()

        assert not cart.products

    def test_clear_empty_cart(self, cart, product):
        cart.clear()

        assert not cart.products

    def test_get_total_price(self, cart, product, product_2):
        cart.add_product(product, buy_product_count)
        cart.add_product(product_2, buy_product_2_count)
        total_price = cart.get_total_price()

        assert total_price == product.price * buy_product_count + product_2.price * buy_product_2_count

    def test_buy_cart_success(self, cart, product, product_2):
        product_in_storage = product.quantity
        product_2_in_storage = product_2.quantity
        cart.add_product(product, buy_product_count)
        cart.add_product(product_2, buy_product_count)
        cart.buy()

        assert product.quantity == product_in_storage - buy_product_count
        assert product_2.quantity == product_2_in_storage - buy_product_count
        assert not cart.products

    def test_buy_cart_failure_due_to_insufficient_quantity(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)
            cart.buy()

    def test_buy_cart_partial_failure(self, cart, product, product_2):
        cart.add_product(product, buy_product_count)

        with pytest.raises(ValueError):
            cart.add_product(product_2, product_2.quantity + 1)
            cart.buy()

    def test_buy_multiple_products(self, cart, product, product_2):
        initial_quantity_product = product.quantity
        initial_quantity_product_2 = product_2.quantity
        cart.add_product(product, buy_product_count)
        cart.add_product(product_2, buy_product_count)
        cart.buy()

        assert product.quantity == initial_quantity_product - buy_product_count
        assert product_2.quantity == initial_quantity_product_2 - buy_product_count
        assert not cart.products

    def test_buy_cart_with_mixed_success_and_failure(self, cart, product, product_2):
        cart.add_product(product, buy_product_count)

        with pytest.raises(ValueError):
            cart.add_product(product_2, product_2.quantity + 1)

        assert len(cart.products) == 1

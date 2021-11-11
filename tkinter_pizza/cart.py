# Класс, который хранит данные текущего заказа
class Cart:

    def __init__(self):
        self.cart = {}

    def get_number(self, pizza_name):
        if pizza_name in self.cart:
            return self.cart[pizza_name]
        else:
            return 0

    def get_pizzas(self):
        result = []
        for name in list(self.cart.keys()):
            result.append([name, self.cart[name]])

        return result

    def add_pizza(self, pizza_name):
        if pizza_name in self.cart:
            self.cart[pizza_name] += 1
        else:
            self.cart[pizza_name] = 1

# Класс, позволяющий осуществлять навигацию в приложении
class MainLayoutManager:

    def __init__(self, main_container, cart_container, cart_page):
        self.pages = {
            "menu": main_container,
            "cart": cart_container
        }

        self.cart_page = cart_page

        self.chosen_page = "main"
        main_container.tkraise()

    def navigate_to(self, name):
        if name == "Меню":
            page = self.pages["menu"]
            page.tkraise()

        elif name == "Корзина":
            page = self.pages["cart"]
            page.tkraise()

            # Добавляет актуальные данные на страницу
            self.cart_page.render()

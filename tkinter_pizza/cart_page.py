import tkinter
import tkinter.messagebox as messagebox


# Страница с заказом
class CartPage(tkinter.Frame):
    def __init__(self, master, cart, pizzas_data, font_color="black",
                 bg_color="white", button_bg="blue", button_font="white"):
        tkinter.Frame.__init__(self, master, bg=bg_color)

        self.cart = cart
        self.font_color = font_color
        self.bg_color = bg_color
        self.button_bg = button_bg
        self.button_font = button_font
        self.pizzas_data = pizzas_data
        self.layouts = []

    def draw(self):
        self.grid(row=0, column=0, sticky="nw", padx=(25, 10), pady=(5, 5))

        empty_layout = tkinter.Frame(self, bg=self.bg_color, width=519, height=550)
        empty_layout.grid(row=0, column=0, sticky="ns")
        not_empty_layout = tkinter.Frame(self, bg=self.bg_color, width=519, height=550)
        not_empty_layout.grid(row=0, column=0, sticky="ns")
        empty_layout.tkraise()

        border = tkinter.Frame(self, bg=self.bg_color, width=1, height=550)
        border.grid(row=0, column=1, sticky="ns")

        self.layouts = [empty_layout, not_empty_layout]

        text = tkinter.Label(empty_layout, text="Корзина пуста! Вернитесь в меню, чтобы добавить товары",
                             bg=self.bg_color, wraplength=519,
                             foreground=self.font_color, anchor="nw", font=("Arial", 14))
        text.grid(row=0, column=0, padx=(10, 0), sticky="nw")

        self.render()
        empty_layout.tkraise()

    def render(self):
        orders = self.cart.get_pizzas()
        if len(orders) == 0:
            self.layouts[0].tkraise()
        else:
            self.layouts[1].tkraise()

            for widgets in self.layouts[1].winfo_children():
                widgets.destroy()

            text = tkinter.Label(self.layouts[1], text="Ваш заказ",
                                 bg=self.bg_color, foreground=self.font_color, anchor="nw", font=("Arial", 16))
            text.grid(row=0, column=0, padx=(10, 0), sticky="nw")

            border1 = tkinter.Frame(self.layouts[1], width=519, height=4, bg=self.button_bg)
            border1.grid(row=1, column=0, padx=(5, 5), sticky="we")

            table = tkinter.Frame(self.layouts[1], bg=self.bg_color, width=519)
            table.grid(row=2, column=0, sticky="nw", pady=(20, 30))

            count = 0
            for name in ["Название", "Количество", "Стоимость"]:
                text = tkinter.Label(table, text=name,
                                     bg=self.bg_color, foreground=self.font_color, anchor="nw", font=("Arial", 14))
                text.grid(row=0, column=count, padx=(10, 0), pady=(5, 15), sticky="nw")
                count += 1

            for i in range(len(orders)):
                price = int()
                for pizza in self.pizzas_data:
                    if pizza["name"] == orders[i][0]:
                        price = pizza["price"]
                orders[i].append(int(price) * int(orders[i][1]))

            count_y = 1
            for order in orders:
                count_x = 0
                for pos in order:

                    text = tkinter.Label(table, text=pos,
                                         bg=self.bg_color,
                                         foreground=self.font_color, anchor="nw", font=("Arial", 12))
                    text.grid(row=count_y, column=count_x, padx=(10, 5), sticky="nw")
                    count_x += 1

                count_y += 1

            border2 = tkinter.Frame(self.layouts[1], width=519, height=4, bg=self.button_bg)
            border2.grid(row=3, column=0, padx=(5, 5), sticky="we")

            text = tkinter.Label(self.layouts[1], text="Чтобы сделать заказ, введите ваш адрес в форму ниже",
                                 wraplength=520,
                                 bg=self.bg_color, foreground=self.font_color, anchor="nw", font=("Arial", 14))
            text.grid(row=4, column=0, padx=(10, 0), pady=(15, 5), sticky="nw")

            address_field = tkinter.Entry(self.layouts[1], bg=self.bg_color,
                                          foreground=self.font_color, font=("Arial", 12))
            address_field.grid(row=5, column=0, padx=(10, 10), pady=(15, 25), sticky="new")

            order_btn = tkinter.Label(self.layouts[1], text="Заказать", cursor="hand2",
                                      height=2, width=30,
                                      bg=self.button_bg, foreground=self.button_font, font=("Arial", 12))
            order_btn.grid(row=6, column=0, padx=(10, 0), pady=(5, 20), sticky="se")

            order_btn.bind('<Button-1>', self.show_message(f"Ваш заказ принят! Ожидайте доставки в течение 40 минут."))

    def show_message(self, info):
        def _show_message(args):
            messagebox.showinfo(message=info)

        return _show_message

import tkinter
from PIL import Image, ImageTk
import requests
from io import BytesIO


# Виджеты с информацией о пицце
class PizzaWidget(tkinter.Frame):
    rows_count = 0

    def __init__(self, master, name, price, size, description, image, cart,
                 bg_color="black", font_color="yellow",
                 button_bg="green", button_font="red"):
        tkinter.Frame.__init__(self, master, bg=bg_color, width=550)

        self.name = name
        self.price = price
        self.size = size
        self.description = description
        self.image = image
        self.columns_count = 0
        self.cart = cart
        self.bg_color = bg_color
        self.font_color = font_color
        self.button_bg = button_bg
        self.button_font = button_font

    def draw(self):
        self.grid(row=PizzaWidget.rows_count, column=0, sticky="new", padx=(25, 40), pady=(5, 5))
        PizzaWidget.rows_count += 1

        pic_path = self.image

        response = requests.get(pic_path, stream=True)
        pizza_pic = Image.open(BytesIO(response.content))
        pic = ImageTk.PhotoImage(pizza_pic)

        pizza_pic_label = tkinter.Label(self, image=pic, bg=self.bg_color, width=150)
        pizza_pic_label.image = pic
        pizza_pic_label.grid(row=0, column=0)

        pizza_content = tkinter.Frame(self, bg=self.bg_color, width=400)
        pizza_content.grid(row=0, column=1, sticky="nw")

        pizza_header = tkinter.Label(pizza_content, text=self.name, bg=self.bg_color, wraplength=400,
                                     foreground=self.font_color, anchor="nw", font=("Arial", 14))
        pizza_header.grid(row=0, column=0, padx=(10, 0), sticky="nw")

        pizza_price = tkinter.Label(pizza_content, text=f"{self.size} см - {self.price}руб.",
                                    bg=self.bg_color, wraplength=400,
                                    foreground=self.font_color, anchor="nw", font=("Arial", 12))
        pizza_price.grid(row=1, column=0, padx=(10, 0), pady=(5, 5), sticky="nw")

        pizza_description = tkinter.Label(pizza_content, text=self.description, bg=self.bg_color,
                                          foreground=self.font_color, anchor="nw", font=("Arial", 12),
                                          wraplength=400)
        pizza_description.grid(row=2, column=0, padx=(10, 0), pady=(5, 5), sticky="nw")

        pizza_order_btn = tkinter.Label(pizza_content, text="Добавить в корзину", cursor="hand2",
                                        height=2, width=30,
                                        bg=self.button_bg, foreground=self.button_font, font=("Arial", 12))
        pizza_order_btn.grid(row=3, column=0, padx=(10, 0), pady=(5, 0), sticky="nw")

        pizzas_count_label = tkinter.Label(pizza_content, text=f"В корзине {self.cart.get_number(self.name)}",
                                           bg=self.bg_color, foreground=self.font_color, font=("Arial", 10))
        pizzas_count_label.grid(row=4, column=0, padx=(10, 0), pady=(0, 0), sticky="nw")

        def add_pizza_to_cart(arg):
            self.cart.add_pizza(self.name)
            pizzas_count_label.config(text=f"В корзине {self.cart.get_number(self.name)}")

        pizza_order_btn.bind('<Button-1>', add_pizza_to_cart)

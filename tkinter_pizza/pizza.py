import tkinter
from PIL import Image, ImageTk
import requests
from io import BytesIO

from pizza_widget import PizzaWidget
from cart import Cart
from side_bar import SideBar
from main_layout_manager import MainLayoutManager
from cart_page import CartPage


# Данные о пицце
pizzas = [
    {
        "name": "Четыре сыра",
        "image": "https://raw.githubusercontent.com/artemmufazalov/file_storage/master/cheesy.png",
        "description": "Почувствуй вкус лучших сыров!",
        "price": 550,
        "size": 30
    },
    {
        "name": "Гавайская",
        "image": "https://raw.githubusercontent.com/artemmufazalov/file_storage/master/hawaiian.png",
        "description": "Идеальное сочетание курицы и ананаса!",
        "price": 600,
        "size": 30
    },
    {
        "name": "Грибная",
        "image": "https://raw.githubusercontent.com/artemmufazalov/file_storage/master/mushrooms.png",
        "description": "Грибы и курица, очень вкусно и очень сытно!",
        "price": 620,
        "size": 30
    },
]

main_bg_color = "white"
main_font_color = "black"

cart = Cart()

window = tkinter.Tk()
window.title("Pizza App")
window.configure(background=main_bg_color)
window.resizable(False, False)

# Устанавливаем иконку приложения
path = "https://raw.githubusercontent.com/artemmufazalov/file_storage/master/pizza.png"
response = requests.get(path, stream=True)
ico = Image.open(BytesIO(response.content))
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

# Настраиваем скелет приложения
mainFrame = tkinter.Frame(window, width=800, height=600, bg=main_bg_color)
mainFrame.grid(row=0, column=0, padx=(10, 20), pady=(20, 40))

cart_content = tkinter.Frame(mainFrame, bg=main_bg_color, width=520, height=550)
cart_content.grid(row=0, column=1, sticky='nw')

main_content = tkinter.Frame(mainFrame, bg=main_bg_color, width=520, height=550)
main_content.grid(row=0, column=1, sticky='nw')

cart_page = CartPage(cart_content, cart, pizzas,
                     font_color=main_font_color,
                     bg_color=main_bg_color,
                     button_bg="blue",
                     button_font="white")

cart_page.draw()


# Устанавливаем для страниц меню и корзины навигацию
main_layout = MainLayoutManager(main_container=main_content, cart_container=cart_content, cart_page=cart_page)


side_bar = SideBar(mainFrame, main_layout)
side_bar.draw()


for pizza in pizzas:
    pizza_widget = PizzaWidget(main_content,
                               pizza["name"], pizza["price"],
                               pizza["size"], pizza["description"],
                               pizza["image"], cart,
                               font_color=main_font_color,
                               bg_color=main_bg_color,
                               button_bg="blue",
                               button_font="white")

    pizza_widget.draw()

window.mainloop()

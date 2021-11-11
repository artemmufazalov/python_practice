import tkinter


# Класс, отвечающий за боковое меню и навигацию в нем
class SideBar(tkinter.Frame):
    def __init__(self, master, main_layout, font_color="black", bg_color="white"):
        tkinter.Frame.__init__(self, master, bg=bg_color)

        self.bg_color = bg_color
        self.font_color = font_color

        self.main_layout = main_layout
        self.navigation = ["Меню", "Корзина", ]

        self.buttons = {}

    def draw(self):
        self.grid(row=0, column=0, sticky='nw')
        count = 0

        for nav in self.navigation:
            if count == 0:
                bg_color = "#B0DDF5"
            else:
                bg_color = self.bg_color

            btn = tkinter.Label(self, text=nav, bg=bg_color, width=8,
                                foreground=self.font_color, anchor="nw", font=("Arial", 14), cursor="hand2")
            btn.grid(row=count, column=0, sticky='nw', padx=(10, 10), pady=(5, 5))
            count += 1
            btn.bind('<Button-1>', self.set_navigation(nav))
            self.buttons[nav] = btn

    def set_navigation(self, name):
        def _navigate_to(arg):
            self.main_layout.navigate_to(name)
            for button_name in list(self.buttons.keys()):
                if button_name == name:
                    self.buttons[button_name].config(bg="#B0DDF5")
                else:
                    self.buttons[button_name].config(bg="white")

        return _navigate_to

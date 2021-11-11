import tkinter


# Кнопка для управления задачами
class Button(tkinter.Label):
    def __init__(self, master, text, bind_fc, bg, fg='white'):
        super(Button, self).__init__(
            master, anchor='center', cursor="hand2",
            text=text,
            bg=bg, foreground=fg, font=('Arial', 12)
        )

        self.text = text
        self.enabled = False
        self.cursor = 'arrow'
        self.bg = bg
        self.fg = fg
        self.disabled_bg = 'gray'
        self.bind_fc = bind_fc

    def display(self):
        self.render()
        self.pack(side=tkinter.RIGHT, padx=(5, 5), pady=(5, 5), ipadx=2, ipady=2)

    def render(self):
        # Перерисовывает кнопку в соответствии с актуальными данными состояния (enabled / disabled)
        self.config(
            cursor='hand2' if self.enabled else 'arrow',
            bg=self.bg if self.enabled else self.disabled_bg)

        # Для неактивной кнопки передается функция, которая не делает ничего
        bind_fc = self.bind_fc if self.enabled else lambda x: x
        self.bind('<Button-1>', bind_fc)

    def disable(self):
        # Выключается кнопку
        self.enabled = False

    def enable(self):
        # Включает кнопку
        self.enabled = True


# Верхняя часть приложения, на которой расположены кнопки управления задачами
class Header(tkinter.Frame):
    def __init__(self, master, widgets_manager):
        super(Header, self, ).__init__(master)
        widgets_manager.init_header(self)

        self.widgets_manager = widgets_manager
        self.buttons = []

    def display(self):
        self.pack(side='top', fill='x', anchor='n', pady=(5, 0))

        # В списке первое значение - текст на кнопке, второе - ее цвет,
        # третье - то действие, которое должно осуществиться в widget_manager.process_action()
        for btn_data in [('Удалить', 'red', 'delete'),
                         ('В прогрессе', 'blue', 'process'),
                         ('Завершить', 'green', 'finish')]:
            btn = Button(self,
                         btn_data[0],
                         self.widgets_manager.process_action(btn_data[2]),
                         btn_data[1])
            self.buttons.append(btn)
            btn.display()

    def toggle_rerender(self):
        # Перерисовывает кнопки в соответствии с актуальным состоянием
        # В соответствии с той группой, к которой принадлежит выбранный виджет,
        # включает или выключает определенные кнопки
        # Так, например, завершенную задачу нельзя заново завершить или переместить в группу "В прогрессе"
        # Если ничего не выбрано, то выключает все кнопки

        selected_widget = self.widgets_manager.get_selected()
        if selected_widget:
            pool = selected_widget.get_pool()
            name = pool.header

            btn_to_disable = []

            if name == 'Завершенные':
                btn_to_disable.append('Завершить')
                btn_to_disable.append('В прогрессе')
            elif name == 'В прогрессе':
                btn_to_disable = 'В прогрессе'

            for button in self.buttons:
                if button.text in btn_to_disable:
                    button.disable()
                else:
                    button.enable()

                button.render()
        else:
            for button in self.buttons:
                button.disable()
                button.render()

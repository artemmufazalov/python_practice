import tkinter


# Класс виджетов задач
class TaskWidget(tkinter.Label):
    def __init__(self, master, widgets_manager, pool, task, task_id,
                 height=2, width=30,
                 bg='#C5EAFE', fg='black',
                 selected_bg='#66F3B8',
                 hover_bg='#61C6FF', selected_hover_bg='#09DA69'):

        super(TaskWidget, self).__init__(master, text=task, height=height, width=width, cursor="hand2",
                                         bg=bg, foreground=fg, font=("Arial", 10))

        self.task_id = task_id
        self.task = task
        self.widgets_manager = widgets_manager
        self.pool = pool
        self.is_selected = False

        self.current_bg = bg
        self.default_bg = bg
        self.default_fg = fg
        self.selected_bg = selected_bg
        self.hover_bg = hover_bg
        self.default_hover_bg = hover_bg
        self.selected_hover_bg = selected_hover_bg

    def display(self):
        self.pack(padx=(5, 5), pady=(5, 5))

        # Устанавливает обработчики при наведении на задачу и ее выборе
        self.bind('<Enter>', lambda event: self.on_enter())
        self.bind('<Leave>', lambda event: self.on_exit())
        self.bind('<Button-1>', lambda event: self.on_select())

    def get_pool(self):
        # Возвращает дорожку, к которой принадлежит задача
        return self.pool

    def on_enter(self):
        # Изменение цвета при наведении на задачу мышью
        self.configure(bg=self.hover_bg)

    def on_exit(self):
        # Возвращение изначального цвета, если мышь более не направлена на виджет
        self.configure(bg=self.current_bg)

    def on_select(self):
        # Выбор задач. У выбранной задачи меняется цвет, также активируются кнопки для ее изменения
        # При повторном клике на уже выбранную задачу она перестает быть выбранной
        if self.is_selected:
            self.widgets_manager.select(None)
        else:
            self.is_selected = True
            self.current_bg = self.selected_bg
            self.hover_bg = self.selected_hover_bg
            self.configure(bg=self.current_bg)
            self.widgets_manager.select(self)

    def on_deselect(self):
        # Отмена выбора текущей задачи
        self.is_selected = False
        self.hover_bg = self.default_hover_bg
        self.current_bg = self.default_bg
        self.configure(bg=self.current_bg)

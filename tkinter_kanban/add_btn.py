import tkinter


# Класс кнопки, добавляющей задачи
class AddBtn(tkinter.Label):
    def __init__(self, master, widgets_manager):
        super(AddBtn, self).__init__(master, text='Добавить задачу',
                                     bg="#E195EC", fg="black",
                                     font=('Helvetica', 14, 'bold'),
                                     cursor='hand2')
        self.bind('<Button-1>', self.add_task)
        self.widgets_manager = widgets_manager

    def display(self):
        self.pack(side='right', anchor='center', ipady=4, ipadx=4, padx=(5, 25), pady=(5, 5))

        # Настройка изменения цвета при наведении на кнопку мышью
        self.bind('<Enter>', lambda event: self.on_enter())
        self.bind('<Leave>', lambda event: self.on_exit())

    def on_enter(self):
        self.configure(bg="#CD95EC")

    def on_exit(self):
        self.configure(bg="#E195EC")

    def add_task(self, *args):
        # При нажатии на кнопку открывается окно ввода задачи.
        # В окно передается функция, она будет вызвана после подтверждения создания задачи
        # Данная функция (_process_input) принимает в себя текст новой задачи и передает его в widgets_manager
        self.widgets_manager.deselect()
        InputDialog(self._process_input).start()

    def _process_input(self, text):
        self.widgets_manager.add_task(text)


# Окно ввода новой задачи
class InputDialog(tkinter.Tk):
    def __init__(self, on_enter_cb):
        super(InputDialog, self).__init__()
        self.minsize(300, 150)
        self.resizable(False, False)
        self.title("Добавить новую задачу")

        self.on_enter_cb = on_enter_cb
        self.input_border = None
        self.error_handler = None
        self.entry = None

        self.current_value = ""

    def display(self):
        header = tkinter.Label(self, text="Введите название задачи", anchor="center")
        header.pack(pady=(10, 10), padx=(10, 10))

        # В качестве границы поля ввода используется фрейм, что позволяет изменять цвет границы динамически
        entry_box = tkinter.Frame(self, bg='gray')
        entry_box.pack(anchor='center', ipadx=0, ipady=0)
        self.input_border = entry_box

        entry = tkinter.Entry(entry_box, width=30, selectborderwidth=0, bd=0)
        entry.pack(anchor='center', padx=(2, 2), pady=(3, 3))
        entry.bind('<Return>', self.process_submit)
        self.entry = entry

        # Текст ошибки, отображается в том случае, если текст задачи не прошел валидацию
        error_handler = tkinter.Label(self, text="", anchor="center", fg="red")
        error_handler.pack(pady=(10, 10), padx=(10, 10))
        self.error_handler = error_handler

        bottom_frame = tkinter.Frame(self)
        bottom_frame.pack(side='bottom', anchor='center', fill='x', pady=(10, 10), padx=(10, 10))

        close_btn = tkinter.Label(bottom_frame, text="Отмена", bg="#E195EC", cursor='hand2')
        close_btn.pack(side='right', anchor='center', ipadx=2, ipady=2)
        close_btn.bind('<Button-1>', self.end)

        submit_btn = tkinter.Label(bottom_frame, text="Создать задачу", bg="#E195EC", cursor='hand2')
        submit_btn.pack(side='right', padx=(10, 10), anchor='center', ipadx=2, ipady=2)
        submit_btn.bind('<Button-1>', self.process_submit)

    def process_submit(self, *args):
        text = self.entry.get()

        # Производится валидация ввода.
        # Если ввод слишком длинный или пустой, то граница поля ввода подсвечивается красным и выводится текст ошибки
        # Если все окей, то вызывается переданная функция (callback), в нее передается текст из формы,
        # а процесс завершается и окно закрывается
        if len(text) > 30:
            self.input_border.config(bg="red")
            self.error_handler.config(text="Название не должно быть больше 30 символов!")
        elif len(text) == 0:
            self.input_border.config(bg="red")
            self.error_handler.config(text="Название не может быть пустым!")
        else:
            self.input_border.config(bg="gray")
            self.error_handler.config(text="")
            self.on_enter_cb(text)
            self.end()

    def start(self, *args):
        self.display()
        self.mainloop()

    def end(self, *args):
        self.destroy()

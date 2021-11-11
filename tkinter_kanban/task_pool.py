import tkinter
from typing import TypedDict, List, Callable

from tkinter_kanban.task_widget import TaskWidget


# Дорожка с задачами
class TaskPool(tkinter.Frame):
    pools_counter = 0

    def __init__(self, master, widgets_manager, tasks: List, header, side="left"):
        super(TaskPool, self).__init__(master)
        widgets_manager.init_pool(header, self)

        # Для последующего расчета id задач в дорожке
        TaskPool.pools_counter += 100

        self.tasks = tasks
        self.id_counter = TaskPool.pools_counter
        self.widgets_manager = widgets_manager
        self.header = header
        self.side = side

        self.tasks_frame = None

    def get_tasks(self):
        return self.tasks

    def add_task(self, task):
        self.tasks.append(task)
        self.render_tasks()

    def delete_task(self, task):
        # Все названия задач уникальны, поэтому список фильтруется по названию задачи
        self.tasks = list(filter(lambda x: x != task, self.tasks))
        self.render_tasks()

    def display(self):
        self.pack(side=self.side, fill='y', anchor='n')

        # При клике за пределами виджетов с задачами, если какой-то виджет был выбран, то выбор отменяется
        self.bind('<Button-1>', self.widgets_manager.deselect)

        header = tkinter.Label(self, text=self.header)
        header.pack()

        border = tkinter.Frame(self, height=1, bg="black")
        border.pack(fill="x")

        task_box = tkinter.Frame(self, width=256, height=1)
        self.tasks_frame = task_box
        task_box.pack(fill='x', ipadx=5, anchor='center')

        self.render_tasks()

    def create_task(self, task):
        # Создает виджет с задачей
        self.id_counter += 1
        task = TaskWidget(self.tasks_frame, self.widgets_manager, self, task, self.id_counter)
        return task

    def render_tasks(self):
        # Перерисовывает все виджеты с задачами, в соответствии с актуальными данными
        if self.tasks_frame:
            for widgets in self.tasks_frame.winfo_children():
                widgets.destroy()

        for item in self.tasks:
            task_widget = self.create_task(item)
            task_widget.display()

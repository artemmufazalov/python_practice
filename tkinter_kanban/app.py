import tkinter

from tkinter_kanban.add_btn import AddBtn
from tkinter_kanban.header import Header
from tkinter_kanban.widgets_manager import WidgetsManager
from tkinter_kanban.task_pool import TaskPool
from tkinter_kanban.data_manager import DataManager

# Приложение Simple Kanban - менеджер задач, по своему виду и функционалу соответствующий доске задач Kanban
# В нем есть три группы задач:
# "Сделать" - еще не начатые задачи
# "В прогрессе" - те задачи, которые уже начаты, но не завершены
# "Завершенные" - список последний выполненных задач
# Для каждой группы задач есть ограничение по количеству,
# так, нельзя добавить больше определенного числа задач в первую и вторую группу,
# а в случае с третьей группой, отображаются только последние выполненные задачи,
# задачи, которые выполнены давно удаляются

# Главное окно приложения
root = tkinter.Tk()
root.minsize(750, 600)
root.resizable(False, True)
root.title("Simple Kanban")

# Менеджер данных
dataManager = DataManager()

# Менеджер виджетов
w_manager = WidgetsManager(dataManager)

# Верхняя часть приложения
header = Header(root, w_manager)
header.display()

border1 = tkinter.Frame(root, bg='black', height=1)
border1.pack(fill='x', pady=(5, 5))

# Фрейм для размещения дорожек задач
pools_container = tkinter.Frame(root)
pools_container.pack()

# Дорожки задач
todo_pool = TaskPool(pools_container, w_manager, [], "Сделать")
todo_pool.display()

in_progress_pool = TaskPool(pools_container, w_manager, [], "В прогрессе")
in_progress_pool.display()

finished_pool = TaskPool(pools_container, w_manager, [], "Завершенные")
finished_pool.display()

# Нижняя часть приложения с кнопкой добавления новой задачи
footer = tkinter.Frame(root)
footer.pack(side='bottom', anchor='center', fill='x', pady=(0, 10))

border2 = tkinter.Frame(root, bg='black', height=1)
border2.pack(side='bottom', fill='x', pady=(5, 5))

add_btn = AddBtn(footer, w_manager)
add_btn.display()

# Загрузка прежде записанных задач из файла
w_manager.load_tasks()

root.mainloop()

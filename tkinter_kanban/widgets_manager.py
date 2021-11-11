import tkinter.messagebox as messagebox


# Класс управления виджетами и данными в приложении.
# По-хорошему его следовало назвать AppManager из-за большого количества его функций,
# но увы, слишком много где экземпляры класса уже названы w_manager или widgets_manager :(
class WidgetsManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.pools = {}
        self.header = None
        self.pool_max = 8

        self.selected_widget = None

    def init_pool(self, name, pool):
        self.pools[name] = pool

    def init_header(self, header):
        self.header = header

    def load_tasks(self):
        # Подгружает задачи из файла
        data = self.data_manager.load_tasks()

        for item in data:
            self.pools[item[0]].add_task(item[1])

    def get_all_tasks(self):
        # Возвращает все задачи из всех дорожек без разделения на группы
        tasks_list = []
        for key in list(self.pools.keys()):
            pool = self.pools[key]
            pool_tasks = pool.get_tasks()
            tasks_list = [*tasks_list, *pool_tasks]

        return tasks_list

    def process_tasks_list_changes(self):
        # При каждом изменении списка задач инициирует запись нового списка в файл
        tasks_list = []
        for key in list(self.pools.keys()):
            for task in self.pools[key].get_tasks():
                tasks_list.append((key, task))

        self.data_manager.write_tasks(tasks_list)

    def add_task(self, text):
        # Добавляет задачу. Следит, чтобы количество задач в дорожках не превышало верхней границы,
        # а если все-таки превышает, то предупреждает пользователя (дорожки "Сделать" и "В прогрессе)
        # или удаляет лишнее (дорожка "Завершенные")
        # (увы, я не сумел постфактум сделать, чтобы дорожки можно было скролить нормально)

        all_tasks = self.get_all_tasks()
        if text in all_tasks:
            messagebox.showinfo(message='Задача с таким названием уже существует! Название должно быть уникальным!')
        elif len(self.pools["Сделать"].get_tasks()) > self.pool_max:
            messagebox.showinfo(message='Слишком много задач! Сконцентрируйтесь на том, что важно!')
        else:
            self.pools['Сделать'].add_task(text)
            self.process_tasks_list_changes()

    def process_action(self, action: str):
        # Возвращает функцию для выполнения переданного действия.
        # Так сделано для того, чтобы,
        # во-первых, зная действия, функцию можно было вызывать из любого места приложения,
        # а во-вторых, чтобы можно было передавать ее в качестве callback для кнопок и других функций

        def _process(*args):
            if self.selected_widget:
                if action == 'delete':
                    pool = self.selected_widget.get_pool()
                    task = self.selected_widget.task
                    self.selected_widget.on_deselect()
                    self.selected_widget = None
                    pool.delete_task(task)
                elif action == 'process':
                    if len(self.pools["В прогрессе"].get_tasks()) > self.pool_max:
                        messagebox.showinfo(message='Многозадачность - это не всегда хорошо! '
                                                    'Сначала закончите задачи из имеющегося списка!')
                    else:
                        self._move_to_pool("В прогрессе")
                elif action == 'finish':
                    # Удаляет самую старую задачу, если задач слишком много
                    if len(self.pools["Завершенные"].get_tasks()) > self.pool_max - 1:
                        self.pools["Завершенные"].tasks.pop(0)
                    self._move_to_pool("Завершенные")

            # Перерисовывает все виджеты задач и кнопки на верхней панели после завершения действия
            self.header.toggle_rerender()
            self.process_tasks_list_changes()

        return _process

    def _move_to_pool(self, pool_name):
        # Перемещает задачу из одной дорожки в другую
        task = self.selected_widget.task
        output_pool = self.selected_widget.get_pool()
        input_pool = self.pools[pool_name]

        self.selected_widget.on_deselect()
        self.selected_widget = None
        output_pool.delete_task(task)
        input_pool.add_task(task)

    def deselect(self, *args):
        # Отмена выбора текущей задачи
        if self.selected_widget:
            self.selected_widget.on_deselect()
            self.selected_widget = None
            self.header.toggle_rerender()

    def select(self, new_widget):
        # Выбор задачи. С данной задачей далее производятся действия с помощью кнопок на верхней панели
        if self.selected_widget:
            self.selected_widget.on_deselect()
        self.selected_widget = new_widget

        self.header.toggle_rerender()

    def get_selected(self):
        return self.selected_widget

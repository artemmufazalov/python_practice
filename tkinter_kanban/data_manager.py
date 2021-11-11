import os
import csv


# Класс, с помощью которого осуществляется запись данных в файл и их чтение
# Данные сохраняются в файл data.csv в папке с файлом кода
# Все задачи записаны вместе с названием группы (pool), к которой они принадлежат
class DataManager:
    def __init__(self):
        cwd = os.getcwd()
        self.path = os.path.join(cwd, "data.csv")

    def load_tasks(self):
        if not os.path.isfile(self.path):
            return []

        with open(self.path, 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            result = set()
            for row in file_reader:
                if row:
                    result.add((row[0], row[1]))

            return result

    def write_tasks(self, tasks_list):
        with open(self.path, "w", encoding="utf-8") as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for task in tasks_list:
                file_writer.writerow([task[0], task[1]])

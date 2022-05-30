import pandas as pd
import numpy as np
import random


class GameEngine:

    def __init__(self, size=4):
        self.size = size
        self.field = self.generate_field()
        self.is_over = False

        self.generate_new_value()
        self.generate_new_value()

    def get_field(self):
        return self.field

    def generate_field(self):
        field = pd.DataFrame([np.full(self.size, 0) for i in range(self.size)],
                             columns=range(self.size),
                             index=range(self.size))

        return field

    def generate_new_value(self):
        empty_cells = list()

        for i in range(self.field.shape[1]):
            for j in range(self.field.shape[0]):
                if self.field[i][j] == 0:
                    empty_cells.append((i, j))

        if len(empty_cells) == 0:
            self.is_over = True
        else:
            random_value = random.randint(0, len(empty_cells) - 1)
            cell_to_fill = empty_cells[random_value]

            self.field[cell_to_fill[0]][cell_to_fill[1]] = 2

    def process_action(self, action):
        if action == 'up':
            self.field.apply(axis=0, func=self._process('left'))
        elif action == 'left':
            self.field.apply(axis=1, func=self._process('left'))
        elif action == 'down':
            self.field.apply(axis=0, func=self._process('right'))
        elif action == 'right':
            self.field.apply(axis=1, func=self._process('right'))

        self.generate_new_value()

        return self.field

    def get_is_game_over(self):
        # return self.is_over
        return True

    @staticmethod
    def _process(order):
        def calculate_action(row):
            size = len(row) - 1
            is_changed = True

            left_border = size if order == 'right' else 0
            right_border = 0 if order == 'right' else size
            step = -1 if order == 'right' else 1

            while is_changed:
                is_changed = False
                for i in range(left_border, right_border, step):
                    if i == right_border:
                        break
                    else:
                        if row[i] == 0:
                            if row[i + step] != 0:
                                row[i] = row[i + step]
                                row[i + step] = 0
                                is_changed = True
                        elif row[i + step] == row[i]:
                            row[i] = row[i] * 2
                            row[i + step] = 0
                            is_changed = True

            return row

        return calculate_action

    def calculate_result(self):
        return self.field.sum().sum()

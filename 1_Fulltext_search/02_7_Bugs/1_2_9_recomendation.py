from typing import Optional


class Matrix:
    """
    Код нашего коллеги аналитика
    Очень медленный и тяжелый для восприятия. Ваша задача сделать его быстрее и проще для понимания.
    """

    def __init__(self):
        self.matrix = []
        self.linear_matrix = []
        self.size = 1

    def matrix_scale(self, scale_up: bool):
        """
        Функция отвечает за создание увеличенной или уменьшенной матрицы.
        Режим работы зависит от параметра scale_up. На выходе получаем расширенную матрицу.
        :param scale_up: если True, то увеличиваем матрицу, иначе уменьшаем
        """
        if scale_up:
            self.size = self.size + 1
        else:
            self.size = self.size - 1


    def add_item(self, element: Optional = None):
        """
        Добавляем новый элемент в матрицу.
        Если элемент не умещается в (size - 1) ** 2, то расширить матрицу.
        """
        if element is None:
            raise ValueError

        if len(self.linear_matrix) >= ((self.size - 1) ** 2):
            self.matrix_scale(scale_up=True)

        self.linear_matrix.append(element)

    def pop(self):
        """
        Удалить последний значащий элемент из массива.
        Если значащих элементов меньше (size - 1) * (size - 2) уменьшить матрицу.
        """
        if self.size == 1:
            raise IndexError()

        value = self.linear_matrix.pop()

        if len(self.linear_matrix) <= ((self.size - 1) * (self.size - 2)):
            self.matrix_scale(scale_up=False)
        return value

    def __str__(self):
        """
        Метод должен выводить матрицу в виде:
        1 2 3\nNone None None\nNone None None
        То есть между элементами строки должны быть пробелы, а строки отделены \n
        """
        for r in range(self.size):
            row = []
            for elem in range(self.size):
                index = self.size * r + elem

                if index < len(self.linear_matrix):
                    row.append(str(self.linear_matrix[index]))
                else:
                    row.append(str(None))

            self.matrix.append(' '.join(row))
        return '\n'.join(self.matrix)


if __name__ == '__main__':
    m = Matrix()
    amount = 14

    elem = (_ for _ in range(amount))
    for _ in elem:
        m.add_item(_+1)
    print(m)
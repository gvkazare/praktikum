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







import pytest

# перечисляем тестовые сценарии
@pytest.mark.parametrize(
    'items,pop_count,expected',
    [
        pytest.param(
            [1, 1, 1, 1], 3, "1 None\nNone None",
            id='pop_several_resizes'
        ),
        pytest.param(
            [1, 1, 1, 1], 1, "1 1 1\nNone None None\nNone None None",
            id='pop_without_resize'
        ),
        pytest.param(
            [1, 2, 3], 1, "1 2\nNone None",
            id='pop_with_resize'
        ),
        pytest.param(
            [1, 1, 1, 1], 0, "1 1 1\n1 None None\nNone None None",
            id='add_item_without_resize'
        ),
        pytest.param(
            [1, 2, 3], 0, "1 2 3\nNone None None\nNone None None",
            id='add_item_extend_non_empty_matrix'
        ),
        pytest.param(
            [1], 0, "1 None\nNone None",
            id='add_item_empty_matrix'
        ),

    ],
)

def test_matrix(items, pop_count, expected):
    matrix = Matrix()
    for item in items:
        matrix.add_item(item)
    for _ in range(pop_count):
        matrix.pop()

    assert str(matrix) == expected

# тесты на проверку исключения, они не вписывается в шаблон,
# где можно передать однотипные параметры как в test_matrix
def test_pop_size_1():
    matrix = Matrix()

    with pytest.raises(IndexError):
        matrix.pop()

def test_add_item_none_value():
    matrix = Matrix()

    with pytest.raises(ValueError):
        matrix.add_item(None)






if __name__ == '__main__':
    m = Matrix()
    amount = 14

    elem = (_ for _ in range(amount))
    for _ in elem:
        m.add_item(_+1)
    print(m)


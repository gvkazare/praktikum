import typing

class CyclicIterator:
    def __init__(self, _range: typing.Iterable):
        self._range = _range
        self._list_of_range_elem = []

    def __iter__(self):
        for i in self._range:
            self._list_of_range_elem.append(i)

        while True:
            for i in self._list_of_range_elem:
                yield self._list_of_range_elem[i]

    def __next__(self):
        pass

cyclic_iterator = CyclicIterator(range(3))
for i in cyclic_iterator:
    print(i)
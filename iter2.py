class CyclicIterator:
    def __init__(self, container):
        self.container = container
        self.current = -1
        self.module = len(container)

    def __iter__(self):
        return self

    def __next__(self):
        self.current = (self.current + 1) % self.module
        return self.container[self.current]

cyclic_iterator = CyclicIterator(range(3))
for i in cyclic_iterator:
    print(i)
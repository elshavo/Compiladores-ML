class Stack:
    def __init__(self):
        """Inicializa el stack vacío"""
        self._data = []

    def push(self, item):
        """Agrega un elemento al tope del stack"""
        self._data.append(item)

    def pop(self):
        """Quita y devuelve el elemento del tope del stack.
        Lanza un error si el stack está vacío."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        """Devuelve el elemento del tope sin quitarlo.
        Lanza un error si el stack está vacío."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        """Devuelve True si el stack está vacío, False si no"""
        return len(self._data) == 0

    def size(self):
        """Devuelve el número de elementos en el stack"""
        return len(self._data)


def run_tests():
    # Caso 1
    s = Stack()
    assert s.is_empty() is True
    assert s.size() == 0

    # Caso 2
    s.push(10)
    assert s.peek() == 10
    assert s.size() == 1

    # Caso 3
    s.push(20)
    assert s.pop() == 20
    assert s.size() == 1

    # Caso 4
    assert s.pop() == 10
    assert s.is_empty() is True

    # Caso 5
    try:
        s.pop()
        assert False, "Debió lanzar IndexError al hacer pop en vacío"
    except IndexError:
        pass

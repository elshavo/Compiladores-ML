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

# Caso 1: stack recién creado está vacío
s = Stack()

assert s.is_empty() == True
assert s.size() == 0

# Caso 2: push y peek funcionan
s.push(10)
assert s.peek() == 10
assert s.size() == 1

# Caso 3 push seguido de pop
s.push(20)
assert s.pop() == 20
assert s.size() == 1

# Caso 4: pop saca lo ultimo (LIFO)

assert s.pop() == 10
assert s.is_empty() == True

# Caso 5: pop en vacío debería lanzar error
try:
    s.pop()
    assert False, "Debió lanzar error al hacer pop en stack vacío"
except IndexError:
    pass # OK, comportamiento esperado
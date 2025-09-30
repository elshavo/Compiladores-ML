class Queue:
    def __init__(self):
        """"Inicializa una cola vacía."""
        self._data = []

    def enqueue(self, item):
        """Agrega un elemento al final de la cola."""
        self._data.append(item)

    def dequeue(self):
        """Remueve y retorna el elemento al frente de la cola.
        Lanza una excepción si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)
    
    def peek(self):
        """Devuelve el elemento del frente sin quitarlo.
        Lanza un error si está vacía"""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self):
        """True si está vacía, False en otro caso"""
        return len(self._data) == 0

    def size(self):
        """Número de elementos en la cola"""
        return len(self._data)

q = Queue()
assert q.is_empty() is True
assert q.size() == 0

q.enqueue("A")
assert q.is_empty() is False
assert q.size() == 1

q.enqueue("B")
assert q.size() == 2


q = Queue()
q.enqueue("A")
q.enqueue("B")
q.enqueue("C")

assert q.peek() == "A"       # El frente es "A"
assert q.dequeue() == "A"    # Sale "A"
assert q.peek() == "B"       # Ahora el frente es "B"
assert q.dequeue() == "B"    # Sale "B"
assert q.dequeue() == "C"    # Sale "C"
assert q.is_empty() is True  # Cola vacía

try:
    q.peek()
    assert False, "Debió lanzar error al hacer peek en vacío"
except IndexError:
    pass





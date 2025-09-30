from structures.stack import Stack
from structures.queue import Queue
from structures.hashtable import HashTable

def demo_stack():
    print("\n--- Stack Demo ---")
    s = Stack()
    s.push(1); s.push(2); s.push(3)
    print("Stack después de pushes:", s._data)
    print("Peek:", s.peek())
    print("Pop:", s.pop())
    print("Stack final:", s._data)

def demo_queue():
    print("\n--- Queue Demo ---")
    q = Queue()
    q.enqueue("A"); q.enqueue("B"); q.enqueue("C")
    print("Queue después de enqueues:", list(q._data))
    print("Peek:", q.peek())
    print("Dequeue:", q.dequeue())
    print("Queue final:", list(q._data))

def demo_hashtable():
    print("\n--- HashTable Demo ---")
    h = HashTable()
    h.put("nombre", "Mario")
    h.put("edad", 23)
    print("Items iniciales:", list(h.items()))
    h.put("edad", 24)  # update
    print("Edad actualizada:", h.get("edad"))
    h.delete("nombre")
    print("Tras borrar 'nombre':", list(h.items()))

if __name__ == "__main__":
    demo_stack()
    demo_queue()
    demo_hashtable()

# 📘 Tarea 01 – Estructuras de Datos (Stack, Queue, HashTable)

## 👤 Autor
- **Nombre:** Mario Alberto González Méndez  
- **Curso:** Compiladores – ITC  
- **Fecha:** Septiembre 2025  

---

## 🎯 Objetivo
Implementar y demostrar el funcionamiento de tres estructuras de datos clásicas:
- **Stack (pila, LIFO)**
- **Queue (cola, FIFO)**
- **HashTable (diccionario con hashing)**  

Cada estructura incluye sus operaciones básicas, pruebas con casos de uso, y un programa principal (`main.py`) que muestra ejemplos de funcionamiento.

---

## 🛠️ Implementación

### 1. Stack (LIFO – Last In, First Out)
- **Métodos:**
  - `push(item)` → inserta elemento en el tope.  
  - `pop()` → elimina y devuelve el elemento del tope.  
  - `peek()` → devuelve el elemento del tope sin eliminarlo.  
  - `is_empty()` → True si está vacío.  
  - `size()` → número de elementos.  
- **Complejidad:** Todas las operaciones en O(1).

---

### 2. Queue (FIFO – First In, First Out)
- **Métodos:**
  - `enqueue(item)` → inserta elemento al final.  
  - `dequeue()` → elimina y devuelve el primer elemento.  
  - `peek()` → devuelve el primer elemento sin eliminarlo.  
  - `is_empty()` → True si está vacía.  
  - `size()` → número de elementos.  
- **Complejidad:**  
  - Con lista: `enqueue` O(1), `dequeue` O(n).  
  - Con `deque`: todas las operaciones en O(1).

---

### 3. HashTable (Diccionario con Separate Chaining)
- **Métodos:**
  - `put(key, value)` → inserta o actualiza.  
  - `get(key)` → devuelve el valor asociado a la clave.  
  - `delete(key)` → elimina la clave y devuelve su valor.  
  - `keys()` → iterador de claves.  
  - `items()` → iterador de pares (clave, valor).  
  - `is_empty()`, `size()`.  
- **Manejo de colisiones:** Separate chaining (listas en cada bucket).  
- **Resize:** duplicación de capacidad cuando `n / capacidad > 0.75`.  
- **Complejidad:**  
  - Promedio: O(1) en `put`, `get`, `delete`.  
  - Peor caso: O(n) si todas las claves colisionan en un mismo bucket.  

---

## ✅ Test-Cases realizados

### Stack
1. Stack vacío recién creado (`is_empty() == True`, `size() == 0`).  
2. `push` seguido de `peek` devuelve el elemento correcto.  
3. Varios `push` seguidos de `pop` cumplen la propiedad LIFO.  
4. `pop` en stack vacío lanza `IndexError`.  

### Queue
1. Queue vacía recién creada (`is_empty() == True`).  
2. `enqueue` seguido de `peek` devuelve el primer elemento.  
3. Varios `enqueue` y `dequeue` cumplen la propiedad FIFO.  
4. `dequeue` en cola vacía lanza `IndexError`.  

### HashTable
1. `put` y `get` funcionan correctamente.  
2. Actualización de clave existente no aumenta el tamaño.  
3. `get` y `delete` de claves inexistentes lanzan `KeyError`.  
4. Iteración con `keys()` e `items()` devuelve todas las entradas.  
5. `resize` automático mantiene accesibles todos los elementos.  
6. Azúcar sintáctico (`h["k"]=v`, `h["k"]`, `del h["k"]`, `"k" in h`) funciona correctamente.  

---

## 📂 Estructura del proyecto
```
Tarea01/
├── structures/
│   ├── stack.py        # Implementación de Stack
│   ├── queue.py        # Implementación de Queue
│   └── hashtable.py    # Implementación de HashTable
└── main.py             # Programa demostrativo de las tres estructuras
```

---

## ▶️ Ejecución
Para correr el demo:
```bash
python main.py
```

### Salida esperada:
```
--- Stack Demo ---
Stack después de pushes: [1, 2, 3]
Peek: 3
Pop: 3
Stack final: [1, 2]

--- Queue Demo ---
Queue después de enqueues: ['A', 'B', 'C']
Peek: A
Dequeue: A
Queue final: ['B', 'C']

--- HashTable Demo ---
Items iniciales: [('nombre', 'Mario'), ('edad', 23)]
Edad actualizada: 24
Tras borrar 'nombre': [('edad', 24)]
```

---

## 📊 Complejidad de operaciones

| Estructura  | Operación principal         | Complejidad promedio | Complejidad peor caso |
|-------------|-----------------------------|----------------------|------------------------|
| **Stack**   | `push`, `pop`, `peek`       | O(1)                 | O(1)                   |
| **Queue**   | `enqueue`, `dequeue`, `peek`| O(1)*                | O(n) con listas        |
| **HashTable** | `put`, `get`, `delete`   | O(1)                 | O(n) si muchas colisiones |

\*Nota: Con `collections.deque`, las operaciones de Queue son O(1) reales.

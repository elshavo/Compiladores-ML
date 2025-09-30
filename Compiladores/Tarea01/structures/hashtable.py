class HashTable:
    def __init__(self, capacity=4):
        """Tabla hash con separate chainin (buckets como listas de (key, value))."""
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)] #lista de buckets
        self._n = 0 # número de pares clave-valor

    def _idx(self, key):
        """Calcula el índice del bucket para una clave"""
        return hash(key) % self._capacity
    
    def put(self, key, value):
        idx = self._idx(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._n += 1
        if self._should_resize():
            self._resize()

    
    def get(self, key):
        """Obtiene el valor de una clave, Lanza KeyError si no existe"""
        idx = self._idx(key)
        bucket = self._buckets[idx]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)
    
    def delete(self, key):
        """Elimina la clave y devuelve su valor. Lanza KeyError si no existe."""
        idx = self._idx(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._n -= 1
                return v
        raise KeyError(key)


    def size(self):
        return self._n
    
    def is_empty(self):
        return self._n == 0
    
    # opcional: azúcar sintáctico
    def __setitem__(self, key, value): self.put(key, value)
    def __getitem__(self, key): return self.get(key)
    def __delitem__(self, key): self.delete(key)
    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def keys(self):
        """Itera sobre todas las claves."""
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def items(self):
        """Itera sobre (clave, valor)."""
        for bucket in self._buckets:
            for k, v in bucket:
                yield (k, v)

    def _should_resize(self, load_factor=0.75):
        return (self._n / self._capacity) > load_factor

    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        old_n = self._n
        self._n = 0  # se recontará en put()

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)  # reinsertar con nueva capacidad

        # sanity check opcional:
        assert self._n == old_n



if __name__ == "__main__":
    h = HashTable()
    assert h.is_empty()
    h.put("A", 10)
    h.put("B", 20)

    assert h.get("A") == 10
    assert h.get("B") == 20
    assert h.size() == 2

    h.put("A", 99)   # actualizar
    assert h.get("A") == 99
    assert h.size() == 2  # no creció, solo actualizó

    try:
        h.get("Z")
        assert False, "Debió lanzar KeyError para clave inexistente"
    except KeyError:
        pass



        # Borrado existente
    h.put("lang", "python")
    assert h.get("lang") == "python"
    val = h.delete("lang")
    assert val == "python"
    try:
        h.get("lang")
        assert False, "Debió lanzar KeyError tras borrar 'lang'"
    except KeyError:
        pass

    # Borrado de clave inexistente
    try:
        h.delete("nope")
        assert False, "Debió lanzar KeyError al borrar clave inexistente"
    except KeyError:
        pass

    # Azúcar sintáctico (si lo agregaste)
    h["x"] = 1
    assert "x" in h
    del h["x"]
    assert ("x" in h) is False


    h = HashTable()
    h.put("a", 1); h.put("b", 2); h.put("c", 3)
    ks = set(h.keys())
    its = set(h.items())
    assert ks == {"a","b","c"}
    assert its == {("a",1),("b",2),("c",3)}

    h = HashTable(capacity=4)
    for i in range(20):
        h.put(f"k{i}", i)
    # Si no hubo errores, ya rehashó varias veces
    for i in range(20):
        assert h.get(f"k{i}") == i
    assert h.size() == 20


    print("✅ HashTable básica put/get OK")

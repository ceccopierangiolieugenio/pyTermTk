import threading
import traceback

class TestLock():
    def __init__(self):
        self.value = 1
        self._mutex = threading.Lock()
        self._r_mutex = threading.RLock()

    def increment(self):
        with self._r_mutex:
            self.value += 1

    def incrementTwice(self):
        with self._r_mutex:
            self.increment()
            self.increment()

t = TestLock()

print(t.value)
t.increment()
print(t.value)
t.increment()
print(t.value)
t.incrementTwice()
print(t.value)

lock = threading.RLock() ; print(lock)

lock.acquire() ; print(lock)
lock.acquire() ; print(lock)
lock.release() ; print(lock)
lock.release() ; print(lock)

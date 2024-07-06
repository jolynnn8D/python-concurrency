import threading
import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print("Elapsed time during the whole program in ms:",
                                                (end-start)*100)
    return wrapper

class MyClass:
    def __init__(self):
        self.my_list = []
        self.second_list = []

    def add_value(self, value):
        self.my_list.append(value)

my_object = MyClass()

def add_values(add_func, start, end):
    for i in range(start, end):
        add_func(i)

@measure_time
def thread_add():
    thread_1 = threading.Thread(target=add_values, args=(my_object.add_value, 0, 100000,))
    thread_2 = threading.Thread(target=add_values, args=(my_object.add_value, 100000, 200000,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

thread_add()
# It can be seen here that thread 1 runs entirely before thread 2
# This is because of GIL locking my_list
# print(my_object.my_list)
print(len(my_object.my_list))


# Thought: What if there's another object?
my_object = MyClass()
second_object = MyClass()

@measure_time
def thread_add_different_object():
    thread_1 = threading.Thread(target=add_values, args=(my_object.add_value, 0, 100000,))
    thread_2 = threading.Thread(target=add_values, args=(second_object.add_value, 100000, 200000,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

# Observation: Runtime is similar -- GIL blocks execution of Python bytecode

thread_add_different_object()
print(len(my_object.my_list))
print(len(second_object.my_list))

# Thought: Adding IO operation to the function should change the execution order
 
my_object = MyClass()

def add_values_with_print(thread, add_func, start, end):
    for i in range(start, end):
        print(f"Thread #{thread} adding {i}")
        add_func(i)

@measure_time
def thread_add_and_print():
    thread_1 = threading.Thread(target=add_values_with_print, args=(1, my_object.add_value, 0, 100,))
    thread_2 = threading.Thread(target=add_values_with_print, args=(2, my_object.add_value, 100, 200,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

# Obersvation: Some interleaving can be observed now, I/O operations will release the GIL
thread_add_and_print()
print(len(my_object.my_list))
print(my_object.my_list)
import threading

from util import measure_time


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
        print(f"#{thread} adding {i}")
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
# print(my_object.my_list)

# A simple CPU intensive task without any shared resources

def cpu_bound_task():
    count = 0
    for _ in range(10**7):
        count += 1

@measure_time
def thread_count(num_threads):
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=cpu_bound_task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


thread_count(1)
thread_count(5)
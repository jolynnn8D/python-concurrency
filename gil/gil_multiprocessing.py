import multiprocessing as mp

from util import measure_time

# A simple multiprocessing test for CPU intensive task

def cpu_bound_task():
    count = 0
    for _ in range(10**7):
        count += 1

@measure_time
def process_count(num_process):
    processes = []
    for i in range(num_process):
        p = mp.Process(target=cpu_bound_task)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()       

def ex1():
    # Time taken for process_count(1) and process_count(5) is similar
    process_count(1)
    process_count(5)

class MyClass:
    def __init__(self):
        manager = mp.Manager()
        self.my_list = manager.list()

    def add_value(self, value):
        self.my_list.append(value)


def add_values(add_func, start, end):
    for i in range(start, end):
        add_func(i)

@measure_time
def process_add():
    my_object = MyClass()
    factor = 10000
    processes = []
    for i in range(20):
        p = mp.Process(target=add_values, args=(my_object.add_value, i*factor, (i+1)*factor))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()    

def ex2():
    # With shared resource, multiprocessing becomes extremely slow -- mutex on shared resource + overhead for context switch
    process_add()
    # print(len(my_object.my_list))

if __name__ == "__main__":
    ex1()
    ex2()

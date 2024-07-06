import multiprocessing as mp

from util import measure_time


class MyClass:
    def __init__(self):
        self.manager = mp.Manager()
        self.my_list = self.manager.list()

    def add_value(self, value):
        self.my_list.append(value)

def add_values(add_func, start, end):
    for i in range(start, end):
        add_func(i)
   
my_object = MyClass()

@measure_time
def process_add():
    factor = 10000
    processes = []
    for i in range(20):
        p = mp.Process(target=add_values, args=(my_object.add_value, i*factor, (i+1)*factor))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()    

process_add()
print(len(my_object.my_list))
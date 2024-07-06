import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} elapsed time during the whole program in ms:",
                                                (end-start)*100)
    return wrapper
from generators.base import function_generator, producer
from generators.consumer import q


def produce():
    functions = function_generator()
    producer(functions, ("", 12345))

if __name__ == "__main__":
    produce()
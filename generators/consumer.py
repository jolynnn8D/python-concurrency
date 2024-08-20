import queue
import threading

from generators.base import consumer, receive_from_queue


def consume():
    for f in consumer(("", 12345)):
        print(f)


if __name__ == "__main__":
    consume()
import os
import pickle
import queue
import re
import socket
import threading
import time
from pathlib import Path

# Basic generator functions

def countdown(n):
    while n > 0 :
        print("Counting down from", n)
        yield n # produces a value and suspends the function
        print("Resume countdown!") # resume here in the next iteration
        n -= 1

def ex1():
    x = countdown(5)
    print("\n## First call ##")
    x.__next__()
    print("\n## Second call ##")
    x.__next__()

    # When the function ends, raise StopIteration
    print("\n## Call in a loop ##")
    try:
        while True:
            x.__next__()
    except StopIteration as e:
        print ("Iteration ended.\n")

 # A simple data processing pipeline to
 # get Python function & arguments from the current directory

def open_files(fp):
    for file in fp:
        yield open(file, 'r', encoding='utf-8')

def cat_lines(files):
    for file in files:
        yield from file

def is_function(line):
    return "def" in line

def parse_function(lines):
    func_regex = re.compile(r"\s*def (\S+)\((.*)\):")
    for line in lines:
        match = func_regex.match(line)
        if match:
            yield match.groups()

def convert_to_dict(tup):
    col_names = ('function_name', 'args')
    return (dict(zip(col_names, t)) for t in tup)

def function_generator():
    file_paths = Path('./').rglob('*.py') # This is a generator object
    py_files = open_files(file_paths)
    py_lines = cat_lines(py_files)
    function_lines = (line for line in py_lines if is_function(line))

    groups = parse_function(function_lines)
    functions = convert_to_dict(groups) # Here we get a generator function to get all Python functions in the directory
    for f in functions:
        yield f

def ex2():
    for f in function_generator():
        print(f)

# Dealing with infinite streams

def follow(f):
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def ex3():
    file = open("./files/log.txt", "r")
    lines = follow(file)
    for line in lines:
        print(line, end='')


# Streaming from sockets

def receive_connections(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is the address family for IPv4 and SOCK_STREAM is the socket type for TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows socket address to be reused immediately after closing, else the socket will be in TIME_WAIT state for 2*MSL (maximum segment lifetime)
    s.bind(addr)
    s.listen(5) # Maximum number of queued connections
    while True:
        client, addr = s.accept()
        print("Connection from", addr)
        yield client

def ex4():
    for client in receive_connections(('', 12345)): # Note that this is not concurrent
        client.send(b"Hello World\n")
        # time.sleep(30) # Adding this would cause the next client to wait for 30 seconds
        client.close()

# Producer & Consumer

def gen_pickle(source):
    for item in source:
        yield pickle.dumps(item)

def gen_unpickle(infile):
    while True:
        try:
            item = pickle.load(infile)
            yield item
        except EOFError:
            return
        

def producer(source, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    for pitem in gen_pickle(source):
        s.sendall(pitem)
    s.close()

def consumer(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    client, addr = s.accept()
    infile = client.makefile('rb')
    for item in gen_unpickle(infile):
        yield item
    client.close()

# Threads communicating with a Queue 

def send_to_queue(source, q):
    for item in source:
        q.put(item)
    q.put(StopIteration)

def receive_from_queue(q):
    while True:
        item = q.get()
        if item is StopIteration:
            break
        yield item

def queue_consumer(q):
    items = receive_from_queue(q)
    for item in items:
        print(item)

def queue_producer(source, q):
    for item in source:
        q.put(item)
    q.put(StopIteration)

def ex6():
    q = queue.Queue()
    t = threading.Thread(target=queue_consumer, args=(q,))
    t.start() 

    lines = follow(open("./files/log.txt", "r"))
    queue_producer(lines, q)


# Data processing pipeline with multiple sources (threads)

def gen_cat(sources):
    for src in sources:
        yield from src

def multiplex(sources):
    in_q = queue.Queue()
    consumers = [] 
    for src in sources:
        t = threading.Thread(target=send_to_queue, args=(src, in_q))
        t.start()
        consumers.append(receive_from_queue(in_q))

    return gen_cat(consumers)

def ex7():
    # The log files are being read concurrently
    lines1 = follow(open("./files/log.txt", "r"))
    lines2 = follow(open("./files/another_log.txt", "r"))
    log = multiplex([lines1, lines2])
    for line in log:
        print(line, end='')

if __name__ == "__main__":
    # ex1()
    # ex2()
    # ex3()
    # ex4()
    # ex6()
    ex7()
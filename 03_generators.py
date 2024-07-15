import re
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

def ex2():
    file_paths = Path('./').rglob('*.py') # This is a generator object
    py_files = open_files(file_paths)
    py_lines = cat_lines(py_files)
    function_lines = (line for line in py_lines if is_function(line))

    groups = parse_function(function_lines)
    functions = convert_to_dict(groups) # Here we get a generator function to get all Python functions in the directory

    for f in functions:
        print(f)

if __name__ == "__main__":
    ex1()
    ex2()
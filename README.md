# A simple exploration into Python concurrency

## GIL

A study on the Global Intepreter Lock (GIL) to see how threading in Python behaves.   

By using `threading` to run CPU and I/O operations, we can observe how CPU operations cannot run concurrently due to the GIL.

We can also see how `multiprocessing` differ from multithreaded programmes in Python. Some key points to observe are the overhead involved in context switching and the manipulation of shared resources.

## Generators

A simple exercise on how generators can be used for data processing pipelines and a leadup into understanding coroutines. This loosely follows the PyCon presentation: [Generator Tricks For Systems Programmers](https://www.dabeaz.com/generators/Generators.pdf).
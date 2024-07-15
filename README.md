# A simple exploration into Python concurrency

## 01. Threading

A study on the Global Intepreter Lock (GIL) to see how threading in Python behaves.   

By using `threading` to run CPU and I/O operations, we can observe how CPU operations cannot run concurrently due to the GIL.

## 02. Multiprocessing
An extension of `01. Threading` to see how multiprocesses differ from multithreaded programmes in Python. Some key points to observe are the overhead involved in context switching and the manipulation of shared resources.

## 03. Generators
A simple exercise on how generators can be used for data processing pipelines and a leadup into understanding coroutines.
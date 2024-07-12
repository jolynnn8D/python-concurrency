# Basic generator functions
def countdown(n):
    while n > 0 :
        print("Counting down from", n)
        yield n # produces a value and suspends the function
        print("Resume countdown!") # resume here in the next iteration
        n -= 1 


x = countdown(10)
x.__next__()
x.__next__()

# When the function ends, raise StopIteration
try:
    while True:
        x.__next__()
except StopIteration as e:
    print ("Iteration ended.")
    
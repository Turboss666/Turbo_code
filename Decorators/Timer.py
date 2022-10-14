import time


def timer(func):
    def inner1(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        time_of_execution = end - start
        print("Total time taken in : ",time_of_execution)
    return(inner1)


@timer
def add(*args):
    time.sleep(3)
    print(sum(args))

add(1,2,3,4,56,7)
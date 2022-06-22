import collections


def log_and_count(counts, key=None):    
    def wrapper(func):
        def in_wrapper(*args, **kwargs):
            if key is None:
                counts.update({func.__name__: 1})
            else:
                counts.update({key: 1})
            func(*args, **kwargs)
            print("called " + func.__name__ + " with " + str(args) + " and " + str(kwargs))
        return in_wrapper
    return wrapper


my_counter = collections.Counter()


@log_and_count(key='basic functions', counts=my_counter)
def f1(a, b=2):
    return a ** b


@log_and_count(key='basic functions', counts=my_counter)
def f2(a, b=3):
    return a ** 2 + b


@log_and_count(counts=my_counter)
def f3(a, b=5):
    return a ** 3 - b


f1(2)
f2(2, b=4)
f1(a=2, b=4)
f2(4)
f2(5)
f3(5)
f3(5, 4)

# outputs:
# called f1 with (2,) and {}
# called f2 with (2,) and {'b': 4}
# called f1 with () and {'a': 2, 'b': 4}
# called f2 with (4,) and {}
# called f2 with (5,) and {}
# called f3 with (5,) and {}
# called f3 with (5, 4) and {}

print(my_counter)
# Counter({'basic functions': 5, 'f3': 2})

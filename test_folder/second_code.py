def first_function(a, b):
    return a + b


def second_function(a, b):
    tot = 0
    for i in range(b):
        tot += first_function(a, i)
    return tot


print(second_function(3, 6))

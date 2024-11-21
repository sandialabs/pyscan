def infinite_iterator():
    i = 0
    while True:
        yield i
        i += 1

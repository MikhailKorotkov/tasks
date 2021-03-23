def task(array):
    if isinstance(array, str):
        return array.index(str(0))
    else:
        return array.index(0)


print(task([1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]))
print(task('1111111110000000'))

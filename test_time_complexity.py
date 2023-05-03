
# test whether accessing via index is slower on bigger arrays
import timeit
my_list_big = range(100_000)
my_list_sml = range(1_000)
def get_big():
    return my_list_big[50_000]
def get_sml():
    return my_list_sml[500]

print(timeit.timeit('get_big()', globals=globals(), number=100_000))
print(timeit.timeit('get_sml()', globals=globals(), number=100_000))
# takes the same amount of time => indexing should


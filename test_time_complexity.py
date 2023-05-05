import json
import random
import timeit

import matplotlib.pyplot as plt

from IndexedList import IndexedList, BaseList


# def test_timing_list_indexing():
#     # test whether accessing via index is slower on bigger arrays
#     my_list_big = range(100_000)
#     my_list_sml = range(1_000)
#     def get_big():
#         return my_list_big[50_000]
#     def get_sml():
#         return my_list_sml[500]

#     print(timeit.timeit('get_big()', globals=locals(), number=100_000))
#     print(timeit.timeit('get_sml()', globals=locals(), number=100_000))
#     # takes the same amount of time

#%%

results, repeats = {}, 100
for p in [1, 1.5, 2, 2.5, 3, 3.5, 4]:
    print(p)
    n = int(10 ** p)

    # values = range(n)  # ascending
    # values = range(n)[::-1]  # descending
    values = sorted(range(n), key=lambda x: random.random())  # random

    print('creating baselist')
    baselist = BaseList(range(n)[::-1])
    timing_baselist_write = timeit.timeit(f'BaseList(range(n)[::-1])', globals=globals(), number=repeats)

    print('creating indexlist')
    indexlist = IndexedList(range(n)[::-1])
    timing_indexlist_write = timeit.timeit(f'IndexedList(range(n)[::-1])', globals=globals(), number=repeats)

    print('querying baselist')
    result_baselist = baselist.query(eq=500)
    timing_baselist_read = timeit.timeit('baselist.query(eq=500)', globals=globals(), number=repeats)

    print('querying indexlist')
    result_indexlist = indexlist.query(eq=500)
    timing_indexlist_read = timeit.timeit('indexlist.query(eq=500)', globals=globals(), number=repeats)

    results[p] = {
        'baselist': {'write': timing_baselist_write, 'read': timing_baselist_read},
        'indexlist': {'write': timing_indexlist_write, 'read': timing_indexlist_read},
    }

with open('./results.json', 'w') as f:
    f.write(json.dumps(results, indent=4))

#%%

with open('./results.json', 'r') as f:
    results = json.loads(f.read())

x = list(results.keys())

# WRITE
base = [results[p]['baselist']['write'] for p in x]
index = [results[p]['indexlist']['write'] for p in x]

f, axs = plt.subplots(2, 1)
print(axs)

ax = axs[0]
ax.plot(x, base, label='base')
ax.plot(x, index, label='index')
ax.set_title('Write performance')
# ax.set_xlabel('Power of 10')
ax.set_ylabel('Relative time')
ax.legend()
ax.grid(True, linestyle='--')


# READ
base = [results[p]['baselist']['read'] for p in x]
index = [results[p]['indexlist']['read'] for p in x]

ax = axs[1]
ax.plot(x, base, label='base')
ax.plot(x, index, label='index')
ax.set_title('Read performance')
ax.set_xlabel('Power of 10')
ax.set_ylabel('Relative time')
ax.legend()
ax.grid(True, linestyle='--')

plt.show()


# %%

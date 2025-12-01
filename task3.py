a = [2,2,4,2,3,4,3,7]

freq = {}
for x in a:
    freq[x] = freq.get(x, 0) + 1

sorted_keys = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
'''
res = []

for key in sorted_keys:
    res.append(key)
'''
print(sorted_keys)


'''
Reference:
https://www.geeksforgeeks.org/python/python-sort-list-elements-by-frequency/
'''
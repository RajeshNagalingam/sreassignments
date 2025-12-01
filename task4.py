def getsub(arr,s):
    result = []
    for x in range(len(arr)):
        result.append(arr[x])
        while sum(result) > s:
            result.pop(0)
        if sum(result) == s:
            return result
arr = [1,2,3,7,5]
s=12
print(getsub(arr,s))


'''
Reference:
https://stackoverflow.com/questions/69263743/how-to-find-the-subarray-with-given-sum
'''
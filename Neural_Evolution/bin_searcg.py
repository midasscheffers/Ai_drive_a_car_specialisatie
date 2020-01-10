import math as mth


def findmiddle(l, answer):

    if not answer in l:
        return None

    length = len(l)
    half = mth.floor(length/2)
    print(l[half], l[0])
    index = None
    
    if l[half] == answer:
        return half

    if l[half] < answer:
        index = findmiddle(l[half:], answer)
        index - half

    if l[half] > answer:
        index = findmiddle(l[:half], answer)
        index + half

    return index


lis = list(range(100))
answer = 44
print(lis)

print(findmiddle(lis, answer))
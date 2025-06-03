def findZigZagSequence(a):
    n = len(a)
    a.sort()
    # basically we find the median and we invert the series after it

    mid = int((n - 1)/2)
    a[mid], a[n-1] = a[n-1], a[mid]

    st = mid + 1
    ed = n - 2
    while(st <= ed):
        a[st], a[ed] = a[ed], a[st]
        st = st + 1
        ed = ed - 1

    for i in range (n):
        if i == n-1:
            print(a[i])
        else:
            print(a[i], end = ' ')
    return

n=5
findZigZagSequence(list(range(2*n+1)))
# 0 1 2 3 4 10 9 8 7 6 5
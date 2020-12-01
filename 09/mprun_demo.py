def sum_of_lists(N):
    total = 0
    for i in range(5):
        L = [j ^ (j >> i) for j in range(N)]
        total += sum(L)
        del L # remove reference to L
    return total

def copies_of_lists(N):
    d = {}
    for i in range(N):
        d[i] = [1,2,3]
    return d

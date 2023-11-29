#Dynamic knapsack

def knapsack(v, w, C):
    N = len(v)
    m = {}

    for c in range(C+1):
        m[(0, c)] = 0

    for i in range(1, N+1):
        m[(i, 0)] = 0
        for c in range(1, C+1):
            if w[i-1] <= c:
                m[(i, c)] = max(m[(i-1, c)], v[i-1] + m[(i-1, c-w[i-1])])
            else:
                m[(i, c)] = m[(i-1, c)]

    return m[(N, C)]

# Example
v = [500, 250, 1500, 1200, 1200, 800]
w = [4, 3, 10, 12, 9, 6]
C = 30

result = knapsack(v, w, C)
print(result)

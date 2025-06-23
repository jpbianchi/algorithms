#%%
def flippingMatrix(matrix):
    # Write your code here
    from copy import deepcopy
    n = len(matrix) // 2

    def hflip(matrix, r):
        for i in range(n):
            matrix[r][i], matrix[r][2*n - 1 - i] = matrix[r][2*n - 1 - i], matrix[r][i]

    def vflip(matrix,c):
        for i in range(n):
            matrix[i][c], matrix[2*n - 1 - i][c] = matrix[2*n - 1 - i][c], matrix[i][c]

    def nsum(matrix,half=False):
        # half = True -> takes 2n x n matrix
        rows = n
        if half:
            rows = 2 * n
        return sum(sum(matrix[i][:n]) for i in range(rows))

    # first we optimize the left side 2n x n by flipping rows
    # which brings the big values to the left
    curtot = nsum(matrix, half=True)
    for r in range(2*n):
        hflip(matrix, r)
        rtot = nsum(matrix, half=True)
        if rtot > curtot:
            curtot = rtot
            print(f"Flipped row {r}")
            print('\n'.join(str(row) for row in matrix) + '\n')
        else:
            print(f"Flipping row {r} back")
            hflip(matrix,r)
    # then we optimize the top left side n x n
    # so no need to go beyond column n
    for c in range(n):
        vflip(matrix, c)
        ctot = nsum(matrix)
        if ctot > curtot:
            curtot = ctot
            print(f"flipped column {c}")
            print('\n'.join(str(row) for row in matrix) + '\n')
        else:
            print(f"Flipping column {c} back")
            vflip(matrix,c)

    return curtot


matrix = [[112, 42, 83, 119], [56, 125, 56, 49], [15, 78, 101, 43], [62, 98, 114, 108]]

print(flippingMatrix(matrix))
# hackerrank says that the maximum is by flipping row2 and column 0
# but by flipping rows 0 2 3 and no column, we get 749

# Flipped row 0
# [119, 83, 42, 112]
# [56, 125, 56, 49]
# [15, 78, 101, 43]
# [62, 98, 114, 108]
# Flipping row 1 back
# Flipped row 2
# [119, 83, 42, 112]
# [56, 125, 56, 49]
# [43, 101, 78, 15]
# [62, 98, 114, 108]
# Flipped row 3
# [119, 83, 42, 112]
# [56, 125, 56, 49]
# [43, 101, 78, 15]
# [108, 114, 98, 62]
# Flipping column 0 back
# Flipping column 1 back
# 749

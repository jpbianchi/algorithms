#!/bin/python3

# https://www.hackerrank.com/challenges/matrix-rotation-algo/problem

def matrixrotation(matrix, rotations=0):
    print('')
    if n < 15 and m < 15:  # we dont print big matrices, they are used for final check only
        for row in matrix: print(' '.join([str(x) for x in row]))

    num_rings = min(n, m) // 2  # n and m are always even, but without //, we get a float

    # let's create rings containing the indices of original elements -> easy rebuild
    # ring k starts from (k,k), and will rotate anti-clockwise
    def ringk2(k):
        """ Here we save only the LOCATIONS of the elements of a ring."""
        ring_k = []
        for i in range(k, m-k):         ring_k += [(k, i)]
        for i in range(k+1, n-1-k):     ring_k += [(i, m-1-k)]
        for i in range(m-k-1, k-1, -1): ring_k += [(n-1-k, i)]
        for i in range(n-2-k, k, -1):   ring_k += [(i, k)]
        return ring_k

    def shift2():
        for k in range(num_rings):
            ring_k = ringk(k)
            if n < 15 and m < 7: print(ring_k)
            lenk = len(ring_k)
            # let's save the r values that are going to be erased before we can move them
            temp = [matrix[pos[0]][pos[1]] for pos in ring_k[:r%lenk]]
            # print('temp=', temp)
            # temp = list(map(lambda x: matrix[x[0]][x[1]], ring_k[:r%lenk]))
            # now we can move elements in the matrix
            for i in range(lenk-r%lenk):  # be careful, r can be > lenk
                row, col = ring_k[i]
                row_value, col_value = ring_k[i+r%lenk]
                matrix[row][col] = matrix[row_value][col_value]
            # let's fill the last values stored in temp and we're done
            temp_pos = 0
            for pos in ring_k[lenk-r%lenk:]:
                row, col = pos
                matrix[row][col] = temp[temp_pos]
                temp_pos += 1

    def ringk(k):  # cleaner code
        """ Here we save only the LOCATIONS of the elements of a ring."""
        ring_k = [(k, i)     for i in range(k,     m-k    )]    \
               + [(i, m-1-k) for i in range(k+1,   n-1-k  )]    \
               + [(n-1-k, i) for i in range(m-k-1, k-1, -1)]    \
               + [(i, k)     for i in range(n-2-k, k,   -1)]
        return ring_k

    def shift():
        """ Here we build a temp ring with matrix values shifted.
            And then we store them in the matrix using ring_k.
            We could have saved only the r values that are erased
            before being used, but the code is cleaner this way
            because can go through ring_k in one shot."""
        for k in range(num_rings):
            ring_k = ringk(k)
            lenk = len(ring_k)
            temp_ring = [matrix[ring_k[(i+r)%lenk][0]][ring_k[(i+r)%lenk][1]] for i in range(lenk)]
            for i in range(lenk): matrix[ring_k[i][0]][ring_k[i][1]] = temp_ring[i]
            # the following code is equivalent, but more readable
            # if n < 15 and m < 7: print(ring_k)
            # temp_ring = []
            # for i in range(lenk):
            #    row, col = ring_k[(i+r)%lenk]
            #    temp_ring.append(matrix[row][col])
            # for i in range(lenk):
            #   row, col = ring_k[i]
            #    matrix[row][col] = temp_ring[i]

    shift()
    print('')
    if n < 15:
        for row in matrix: print(' '.join([str(x) for x in row]))
    ok = True
    for i in range(n):
        if matrix[i] != matrix_test[i]:
            ok = False
            print(str(matrix[i][:15])+'\n' + str(matrix_test[i][:15]))
            break

    print('matrix {} x {} x {} rotations:'.format(n,m,r), 'OK' if ok else 'Not OK')


if __name__ == '__main__':

    INPUT_FILE = "Matrix Layer Rotation tests.txt"
    fin = open(INPUT_FILE, 'r')

    rep = 5
    for _ in range(rep):
        n, m, r = list(map(int, fin.readline().strip().split()))
        matrix = []

        for _ in range(n):
            m_line = fin.readline().rstrip().split()
            matrix.append(list(map(int, m_line)))

        _ = fin.readline()

        matrix_test = []

        for _ in range(n):
            m_line = fin.readline().rstrip().split()
            matrix_test.append(list(map(int, m_line)))

        _ = fin.readline()

        matrixrotation(matrix, r)

    fin.close()

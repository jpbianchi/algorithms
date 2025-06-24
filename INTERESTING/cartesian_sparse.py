"""
Problem: find 2 matrices P & Q of pairs whose cartesian products row by row gives a given set of pairs xiyi
This is an optimized version of cartesian.py. I use sparse matrices to
- save memory (valuable with high values since cartesian.py builds a maxval x maxval matrix)
- speed up search (important to build a second 'vertical' sparse matrix tough)

The search is ~100x faster now.

"""
import time
import numpy as np
from itertools import product
# from dask.array import einsum, asarray, zeros, where
from scipy.sparse import csr_matrix

K=1000
maxval = 1_000_000  # high values don't matter with sparse matrices
start = time.time()
# let's create xi,yi pairs from randomly generated P,Q
pqpairs = [np.random.choice(maxval,4, replace=True) for _ in range(K)]  # replace True much faster
P,Q = np.array(pqpairs)[:, :2], np.array(pqpairs)[:, 2:]
print(f"Matrices P, Q created in {time.time()-start:.2f} s")
def cartLine(p0,p1,q0,q1):
    return np.array([(p0,q0),(p0,q1),(p1,q0),(p1,q1)])

xypairs = cartLine(P[:,0],P[:,1],Q[:,0],Q[:,1]).transpose(0,2,1) # move pairs to last dim
xymixed = sorted(xypairs.reshape(-1,2).tolist())  # remove the dimensions, keep the pairs

if len({tuple(xy) for xy in xymixed}) != K * 4:
    print(f"This program doesn't work with duplicates (xi,yi)")
    exit()

Xi,Yi = np.array(xymixed).transpose().tolist()  # must separate indices for M[Xi,Yi]==1 to work

Mx = csr_matrix((np.ones(K*4, dtype=int), (Xi,Yi)))
My = csr_matrix((np.ones(K*4, dtype=int), (Xi,Yi))).tocsc()
# ^ without the second sparse matrix, the vertical search M[:,yi] takes a LOT of time

print("Sparse matrix created")
start = time.time()

def findSquare(Xi,Yi):
    pairs = []
    xymixedset = {tuple(xy) for xy in xymixed}

    start = time.time()
    for xi, yi in xymixedset:

        ys = Mx.getrow(xi).indices
        xs = My.getcol(yi).indices
        for i,j in product(xs,ys):

            i,j = int(i), int(j)
            if i==xi or j==yi: # 4th corner must not be on xi or yi, or 'flat' square
                continue

            if Mx[i,j] == 1:  # found 4th corner!
                corners = (xi,yi),(i,yi),(xi,j),(i,j)
                p1 = [xi,i] if [xi,i] in P else [i,xi]
                p2 = [yi,j] if [yi,j] in Q else [j,yi]
                assert {*corners} - xymixedset == set()
                assert p1 in P, f"Found wrong pair in P {xi,i}"
                assert p2 in Q, f"Found wrong pair in Q {yi,j}"
                # print(f"Found square {corners}")
                xymixedset -= {corners}
                # remove 4 corners from Mx, no need to update My
                Mx[[xi,i,xi,i],[yi,yi,j,j]]=0

                pairs.append([p1,p2])
                if not len(pairs) % 100:
                    print(f"Found {len(pairs)} pairs in {time.time()-start:.2f}s")
                continue
        pass

    if K < 10:
        print(f"Found the following pairs")
        print(pairs)
    assert len(pairs) == K, f"Mismatch - {len(pairs)} found instead of {K}"
    print(f"All {K} pairs P & Q found")

if K < 10:
    print(P)
    print(Q)

findSquare(Xi,Yi)
print(f"CPU time: {time.time()-start:.2f}s")

# K =  500, maxval =  1_000_000 - 0.1s
# K = 1000, maxval =    100_000 - 0.3s
# K = 1000, maxval = 10_000_000 - 0.3s
# K = 5000, maxval = 10_000_000 - 2s (with replace = True)
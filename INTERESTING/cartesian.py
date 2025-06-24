"""
Problem: find 2 matrices P & Q of pairs whose cartesian products row by row gives a given set of pairs xiyi

Hint: a cartesian product of two pairs creates 4 pairs which represent a square.  
So we look for squares in the matrix of all possible pairs.
We will optimize by using sparse matrices later.
"""
import time
import numpy as np
from itertools import product

K=1000
maxval = 100_000
# let's create xi,yi pairs from randomly generated P,Q
pqpairs = [np.random.choice(maxval,4, replace=True) for _ in range(K)]
P,Q = np.array(pqpairs)[:, :2], np.array(pqpairs)[:, 2:]
def cartLine(p0,p1,q0,q1):
    return np.array([(p0,q0),(p0,q1),(p1,q0),(p1,q1)]).transpose()

xypairs = cartLine(P[:,0],P[:,1],Q[:,0],Q[:,1]).transpose(0,2,1)
xymixed = sorted(xypairs.reshape(-1,2).tolist())
if len({tuple(xy) for xy in xymixed}) != len(xymixed):
    print(f"This program doesn't work with identical (xi,yi)")
    exit()

Xi,Yi = np.array(xymixed).transpose().tolist() # must separate indices for M[Xi,Yi]=1 to work

M = np.zeros((maxval, maxval), dtype=int)
M[Xi,Yi] = 1

def removexiyi(xi, yi, xymixed):
    idx = xymixed.index([xi,yi])
    xymixed.pop(idx)

def findSquare(Xi,Yi):
    pairs = []
    xymixedset = {tuple(xy) for xy in xymixed}

    start = time.time()
    for xi, yi in xymixedset:

        ys = np.where(M[xi,:] == 1)[0]
        xs = np.where(M[:,yi] == 1)[0]
        for i,j in product(xs,ys):

            i,j = int(i), int(j)
            if i==xi or j==yi:
                continue

            if M[i,j] == 1:
                corners = (xi,yi),(i,yi),(xi,j),(i,j)
                p1 = [xi,i] if [xi,i] in P else [i,xi]
                p2 = [yi,j] if [yi,j] in Q else [j,yi]
                assert {*corners} - xymixedset == set()
                assert p1 in P, f"Found wrong pair in P {xi,i}"
                assert p2 in Q, f"Found wrong pair in Q {yi,j}"
                # print(f"Found square {corners}")
                xymixedset -= {corners}
                # remove 4 corners from M
                M[[xi,i,xi,i],[yi,yi,j,j]]=0

                pairs.append([p1,p2])
                if not len(pairs) % 100:
                    print(f"Found {len(pairs)} pairs in {time.time()-start:.2f}s")
                continue

    if K < 10:
        print(pairs)
    assert len(pairs) == K, f"Mismatch - {len(pairs)} found instead of {K}"
    print(f"All {K} pairs P & Q found")

if K < 10:
    print(P)
    print(Q)
else:
    print(f"Looking for {K} pairs...")
start = time.time()
findSquare(Xi,Yi)
print(f"CPU time: {time.time()-start:.2f}s")

# K = 1000, maxval = 10000 - 0.8s
# K = 5000, maxval = 50000 - 24s
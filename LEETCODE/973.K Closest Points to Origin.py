# https://leetcode.com/problems/k-closest-points-to-origin
# Given an array of points where points[i] = [xi, yi] represents a point on the 
# X-Y plane and an integer k, return the k closest points to the origin (0, 0). 
# 
#  The distance between two points on the X-Y plane is the Euclidean distance (
# i.e., √(x1 - x2)² + (y1 - y2)²). 
# 
#  You may return the answer in any order. The answer is guaranteed to be 
# unique (except for the order that it is in). 
#  Example 1: 
# Input: points = [[1,3],[-2,2]], k = 1
# Output: [[-2,2]]
# Explanation:
# The distance between (1, 3) and the origin is sqrt(10).
# The distance between (-2, 2) and the origin is sqrt(8).
# Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
# We only want the closest k = 1 points from the origin, so the answer is just [
# [-2,2]].
#  
#  Example 2: 
# 
# Input: points = [[3,3],[5,-1],[-2,4]], k = 2
# Output: [[3,3],[-2,4]]
# Explanation: The answer [[-2,4],[3,3]] would also be accepted.
#  
#  Constraints: 
# 
#  1 <= k <= points.length <= 10⁴ 
#  -10⁴ < xi, yi < 10⁴ 
#  
#  Related Topics Array Math Divide and Conquer Geometry Sorting Heap (Priority 
# Queue) Quickselect 👍 6909 👎 251

from typing import List
# leetcode submit region begin(Prohibit modification and deletion)
from scipy.spatial.distance import cdist
import numpy as np
import heapq
class Solution:
    def kClosest1(self, points: List[List[int]], k: int) -> List[List[int]]:
        ''' This is kNN for [0,0]'''
        if k == len(points):
            return points
        # cdist is a very handy function to calculate all distances between two groups
        dist = cdist(points,[[0,0]]).flatten()
        pos = np.argpartition(dist, kth=k)[:k]
        topk = np.array(points)[pos]

        return topk.astype(int).tolist()

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """ Let's try with heapq which sorts automatically """

        # the following works, very simple
        # return heapq.nsmallest(k, points, key=lambda x: x[0] * x[0] + x[1] * x[1])

        # but let's try to play with heaps a bit
        heap = []
        for x,y in points:
            # we limit the heap size so that an insertion takes log(k)
            if len(heap) < k:
                # IMPORTANT the heap remains a list at all times
                heapq.heappush(heap, (-(x**2+y**2),x,y))
            else:
                # we use negative distances because we pop the smallest
                # value = the highest distance
                heapq.heappushpop(heap, (-(x**2+y**2),x,y))
        return [[x,y] for dist,x,y in heap]


# leetcode submit region end(Prohibit modification and deletion)
print(Solution().kClosest([[3,3],[5,-1],[-2,4]], 2))
# print(Solution().kClosest([[0,1],[1,0]], 2))
assert Solution().kClosest([[3,3],[5,-1],[-2,4]], 2) in [[[3,3],[-2,4]], [[-2,4],[3,3]]]
print('TESTS PASSED')

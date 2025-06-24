# !/bin/python3

# problem https://www.hackerrank.com/challenges/non-divisible-subset/problem?utm_campaign=challenge-recommendation

# there is a trick - if you try to compute all the combinations, it becomes exponential and takes forever
# the problem is solved by taking mod k of all values, so now we must avoid a sum = k
# so if there are numbers multiples of 0 or k/2, we can only take 1 of those
# then we look at the pairs which are i and k-i because only those pairs can give k
# we must choose between one of the two otherwise there will be a pair whose sum is k, so we pick
# the one with the highest count ... all the other modules will never make a total = k
# since the pairs can't interfere with each other, we can just sum up all the numbers we got

from collections import Counter

def nonDivisibleSubset2(k, S):
    '''This solution takes forever with large sets'''

    def test_all_duos(s):
        '''Returns True if no combinations of sums is divisible by k
           s is a list of numbers [1,2,5]'''
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                if (s[i] + s[j]) == k:  # all elements < k, so the sum is either k or not divisible by k
                    #print('Found {} + {} in {}'.format(s[i],s[j],s))
                    return False
        return True

    def test_all_sets(S):
        '''Returns True where it found one set where all sums are not divisible by k
           This supposes that S = [[a,b,c],[a,c,d]]'''
        if len(S[0]) < 2: return True
        print(len(S))
        for s in S:
            if test_all_duos(s): return True  # exit as soon as one subset is ok
        return False

    def gen_subsets(S):
        '''Generates all subsets of S, with one less elements than S'''
        l = []
        for subset in S:
            for i in range(len(subset)):
                k = subset.copy()
                del k[i]
                l.append(k)
        return l

    def find_subset(S):
        '''Finds out if one pair is S is divisible by k
           Here S, can have multiple subsets, so we must check them all'''

        size = len(S[0])  # size of subsets, to be returned eventually

        for i in range(len(S[0])):

            if test_all_sets(S) is True:
                return size
            else:
                S = gen_subsets(S)
                size -= 1
        return size
    print(len(S))
    S = [[S[i]%k for i in range(len(S))]] # first time, S=[1,2,3] -> [[1,2,3]]
    return(find_subset(S))

def nonDivisibleSubset(k, S):

    print(len(S))
    S = [S[i]%k for i in range(len(S))]
    count = Counter(S)
    print(count)
    ans = 1 if count[0] else 0 # we take 1 for all the values that are % k, if there are any
    if k % 2 == 0: ans += 1 if count[k/2] else 0 # we also take one for values % k/2, if there are any
    span = (k-1) // 2

    for i in range(1, span+1):
        ans += max(count[i], count[k-i])
    return ans

INPUT_PATH = 'Non Divisible Subset test11.txt'

fin = open(INPUT_PATH, 'r')

nk = fin.readline().split()
arr = fin.readline().rstrip().split()

fin.close()

n = int(nk[0])

k = int(nk[1])

S = list(map(int, arr))

result = nonDivisibleSubset(k, S)

print(result)

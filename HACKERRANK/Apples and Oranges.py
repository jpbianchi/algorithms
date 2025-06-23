def countApplesAndOranges(s, t, a, b, apples, oranges):
    # Write your code here
    def howmany(a,fruits):
        print([d for d in fruits if s<=(a+d)<=t])
        return sum([1 for d in fruits if s <= (a+d) <= t])
        
    return howmany(a, apples) + howmany(b, oranges)

print(countApplesAndOranges(7, 10, 4, 12, [2, 3, -4], [3 ,-2, -4]))
# This problem asks to calculate x^n
# https://codinginterviewsmadesimple.substack.com/p/solutionproblem-70-powxn-amazon
# Let's forget the edge cases and focus on the computation of the main case (x and n > 0, if n < 0, just use 1/x)

# if n = 2 k, then x^n = x^2k = (x^2)^k
# if n = 2 k + 1, then do x x^2k = x (x^2)^k
# in other words, x^n = x^(n%2) pow(x^2, n//2) = x^(n%2) pow(x', n')

# we have the same problem but with x'=x^2 (1) and n'=n//2 (5), we stop when n' = 1 (4)
# one could write x^n = x^(n%2) (x^2)^(n//2%2) (x^4)^(n//4%2)... 
# this shows we do not care about pow(x', n'), we only track the oddity of 
# n' to decide if we use x' at that iteration or not

# so at each iteration, we also need to test if the exponent is odd (3), in which 
# case we multiply the temporary result by the current power of x (2)
# then we prepare the next iteration by squaring (1) the current value of x to get x',
# in case we need it, and the new exponent is n' = n//2 (5)


def powxn(x, n):
    ans = 1
    
    while n >= 1:       # for (4) above
        if n % 2:       # for (3) above
            ans *= x    # for (2) above
        x *= x          # for (1) above, this is x'
        n //= 2         # for (5) above, this is n'
    
    return ans


assert abs(powxn(1.5, 33) - 1.5**33) < 1e-5
assert abs(powxn(0.95, 75) - 0.95**75) < 1e-5
print("TESTS PASSED")

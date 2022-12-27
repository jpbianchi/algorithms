These problems come from Leetcode.
Also look into leetcode/editor/en which were put there by a Pycharm Leetcode plugin.

To extract the most out of a problem, beyond solving it, I first come up with a solution.
Then I try to optimize it for speed or memory, according to the Leetcode scores of the previous solution.
That way, you can follow my thinking process.
When relevant, I describe in the docstrings the type of problem it is (dynamic programming, heaps etc)

Then I look at the best solutions, to see if I missed something, a different way to solve the problem, to learn from them.  
This is why there are several solutions per problem.  

Also, sometimes, when I know how to solve a problem by, say, using nested loops which is not very interesting, I try to use new libraries, or libraries functions I had never used before to at least learn something.

A great example of this is the problem "[542]01 Matrix.py" which can be solved by scanning every cell of the matrix with two nested for loops.
Instead, I used numpy.vectorize on the main matrix and 4 rolled version (up/down, left/right) to find the areas to be updated in parallel.
It's slower but more interesting to solve it that way.  
    def fizzBuzz(n):
        # Write your code here
        for i in range(1,n+1):
            match i:
                case _ if i % 15 == 0:
                    print("FizzBuzz")
                case _ if i % 3 == 0 and i % 5 > 0:
                    print("Fizz")
                case _ if i % 5 == 0 and i % 3 > 0:
                    print("Buzz")
                case _:
                    print(i)

fizzBuzz(15)
# 1
# 2
# Fizz
# 4
# Buzz
# Fizz
# 7
# 8
# Fizz
# Buzz
# 11
# Fizz
# 13
# 14
# FizzBuzz
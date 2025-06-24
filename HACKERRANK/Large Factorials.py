

import re
# let's train with lists, and try to implement factorial using strings, so we can
# compute very very long factorials (totally useless in python3 since it can handle any length

def extraLongFactorials(n):
    def add_two_str(str1, str2):

        len1 = len(str1)
        len2 = len(str2)

        sum_str = ""
        carry = 0
        for i in range(max(len1, len2)):
            digit1 = int(str1[i]) if i < len1 else 0
            digit2 = int(str2[i]) if i < len2 else 0

            digit = (digit1 + digit2 + carry) % 10
            carry = (digit1 + digit2 + carry) // 10

            sum_str += str(digit)
        return sum_str + (str(carry) if carry is not 0 else '')

    def mul_str(str1, n):

        n = str(n)[::-1]
        result = ''
        for num in range(len(n)):

            temp_str = '0'* num
            carry = 0

            for i in range(len(str1)):

                prod = int(str1[i]) * int(n[num]) + carry
                digit = prod % 10
                carry = prod // 10
                temp_str +=str(digit)

            result = add_two_str(result, temp_str + (str(carry) if carry is not 0 else ''))

        return result

    fac = "1"

    for i in range(n):
        fac = mul_str(fac, i+ 1)

    return int(fac[::-1])
ll = extraLongFactorials(50)
print(type(ll), ll)

spl = re.split(r'(\d\d\d\d)' , str(ll))
print(spl)

for num4 in (x for x in spl if x != ''):
    print(num4, end = ' ')
print('')

print(lambda i : next(x for x in spl if x != '') for i in range(len(spl)) )
print([x for x in spl if x != ''])
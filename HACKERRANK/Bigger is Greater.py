# https://www.hackerrank.com/challenges/bigger-is-greater/problem

#!/bin/python3

# Complete the biggerIsGreater function below.
def biggerIsGreater(w):

    def find_switch(ww, start, end):  # we search only between start and end not included
        """Finds the positions to switch"""
        if len(ww) == 1: return None, None
        for i in range(end-1, start-1, -1):
            for j in range(i-1, start-1, -1):
                if ww[i] > ww[j]:
                    #print("let's switch {} - {}".format(ww[j],ww[i]))
                    return j, i
        return None, None # no switching possible

    w = list(w)  # we need a list of characters because string is immutable, so can't swap characters

    switch_couple = list(find_switch(w, 0, len(w)))  # holds the best switch couple, for now
    if switch_couple[0] is None:
        return 'no answer'
    # when we find a switching couple, we must be sure there isn't a better one
    best_switch = switch_couple.copy()  # best case scenario

    while 1:
        j, i = find_switch(w,best_switch[0],switch_couple[1])
        if j is None:
            break
        elif  (j == best_switch[0] and w[best_switch[1]] > w[i]) or (j > best_switch[0]): # we have found a smaller change
            best_switch = j, i
            switch_couple = [j, i]
        else :
            switch_couple[1] = i

    # now we have the best switch couple, we must switch and then
    # we must mininize value of everything that's after position best_switch[0]
    if best_switch[0] is not None:
        w[best_switch[0]], w[best_switch[1]] = w[best_switch[1]], w[best_switch[0]]
        w = w[:best_switch[0]+1] + sorted(w[best_switch[0]+1:])
    else:
        w = ['no answer']

    return ''.join(w)

if __name__ == '__main__':

    print('{0} should be {1}'.format(biggerIsGreater('abdc'), 'acbd'))
    print('{0} should be {1}'.format(biggerIsGreater('abcd'), 'abdc'))
    print('{0} should be {1}'.format(biggerIsGreater('dkhc'), 'hcdk'))
    print('{0} should be {1}'.format(biggerIsGreater('dcba'), 'no answer'))
    print('{0} should be {1}'.format(biggerIsGreater('dmsym'), 'dmyms'))

    INPUT_FILE = 'Bigger is Greater'
    fin = open(INPUT_FILE + ' test.txt', 'r')
    fcheck = open(INPUT_FILE + ' test results.txt', 'r')

    num = int(fin.readline().strip())
    print(num)
    successes = 0
    total_tries = 4000
    for i in range(total_tries):

        w = fin.readline().strip()
        w_check = fcheck.readline().strip()
        wbigger = biggerIsGreater(w)
        if wbigger != w_check:
            print(i, wbigger, w_check, wbigger == w_check)
            #break
        else:
            successes += 1
    print(successes, ' successes over ', total_tries)

    fin.close()
    fcheck.close()



#!/bin/python3

# https://www.hackerrank.com/challenges/almost-sorted/problem


def almostsorted(arr):

    def verify_sequence(first_pos, second_pos, len_arr, inverted = False):
        """ True if sequence around first_pos and second_pos are ok when inverted is False
            True if still ascending if we reverse the seq when inverted is True"""

        f1 = arr[first_pos-1] if first_pos > 0 else arr[second_pos]  # else just to make first test good
        f2 = arr[second_pos + 1] if second_pos < len_arr - 1 else arr[first_pos]

        if inverted:
            return (f1 <= arr[second_pos]) and (arr[first_pos] <= f2)
        else:
            return ((f1 <= arr[second_pos] <= arr[first_pos+1]) and
                (arr[second_pos - 1] <= arr[first_pos] <= f2))

    def inverted_seq(first_pos, len_arr):
        """Find decreasing sequence starting at first_pos, and return last_pos"""

        for i in range(first_pos, len_arr - 1):
            if arr[i] >= arr[i+1]:
                continue
            return i  # we found a sequence of at least 2 elements or more, ending on i
        return len_arr - 1  # we reached the end and exit for loop

    def test_swap():
        first_pos = None
        second_pos = None
        len_arr = len(arr)

        i = -1
        while i < len_arr - 2:
            i += 1
            if arr[i] <= arr[i+1]:
                continue
            if first_pos is None:
                first_pos = i  # we found the first elem to swap, let's save it
                second_pos = inverted_seq(first_pos, len_arr)  # let's find out if it's an inverted seq
                if second_pos - first_pos > 1:  # we have an inverted seq, let's check the limits
                    if verify_sequence(first_pos, second_pos, len_arr, inverted=True):
                        i = second_pos - 1  # - 1 because of i += 1 after while
                        msg = ['yes\nreverse', first_pos+1, second_pos+1]  # they want starting pos at 1
                    else:
                        msg = ['no', '', '']
                    continue

                if second_pos == first_pos + 1:  # we have a swap but real second_pos could be further
                    if second_pos == len_arr - 1:  # if we have reached the end, exit, we got our pair
                        if verify_sequence(first_pos, second_pos, len_arr):
                            msg = ['yes\nswap', first_pos + 1, second_pos + 1]
                        else:
                            msg = ['no', '', '']
                        break
                    else:
                        second_pos = None  # use it as a flag we're still looking for swap elem
                        continue

            if second_pos is None:  # we never enter here if we have an inverted seq, so we're safe
                # we found our second element, now verify seq and continue
                second_pos = i + 1  # we want arr[i+1] here
                if verify_sequence(first_pos, second_pos, len_arr):
                    msg = ['yes\nswap', first_pos+1, second_pos+1]
                    continue
                else:
                    msg = ['no', '', '']
                    break

            # if we end up here, it means the sequence after second_pos is not ascending
            msg = ['no', '', '']
        else:
            # here we finished the while loop which means either it's good, or we didn't find second
            # be careful, we also end up here for the inv sequences
            if first_pos is None:
                msg = ['no', '', '']  # arr is already an ascending sequence, so no
            elif second_pos is None:  # we never found a second element, so it was first_pos+1
                second_pos = first_pos + 1
                # we must retest the sequence
                if verify_sequence(first_pos, second_pos, len_arr):
                    msg = ['yes\nswap', first_pos+1, second_pos+1]
                else:
                    msg = ['no', '', '']

        return msg

    print(*arr)
    print(*test_swap(), '\n')
    pass


if __name__ == '__main__':

    INPUT_FILE = "Almost Sorted tests.txt"
    fin = open(INPUT_FILE, 'r')


    def sort_input():
        _ = fin.readline().split()

        arr = list(map(int, fin.readline().rstrip().split()))
        _ = fin.readline()  # to get rid of the line with the answer

        almostsorted(arr)

    sort_input()
    sort_input()
    sort_input()
    sort_input()
    sort_input()
    sort_input()
    sort_input()
    sort_input()
    fin.close()

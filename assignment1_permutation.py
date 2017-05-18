# Uses python3
import sys

def check_str_permutation(a, b):
    """ Сhecks that two strings, a and b, are permutations of each other """
    if len(a) != len(b):
        return False
    else:
        a = a.lower()
        b = b.lower()
        letters = {}
        for l in a:
            if l in letters:
                letters[l] += 1
            else:
                letters[l] = 1
        for l in b:
            if l in letters:
                if letters[l] == 1:
                    letters.pop(l)
                elif letters[l] > 1:
                    letters -= 1
            else:
                return False
        return letters == {}


if __name__ == '__main__':
    input = sys.stdin.read()
    strings = input.split()
    if len(strings) != 2:
        raise RuntimeError('2 strings expected, got {0}'.format(len(strings)))
    else:
        print(check_str_permutation(strings[0], strings[1]))

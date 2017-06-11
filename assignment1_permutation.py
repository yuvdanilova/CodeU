#!/usr/bin/env python3
import sys
import unittest

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
                    letters[l] -= 1
            else:
                return False
        return letters == {}


class TestStrPermutation(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(check_str_permutation('abc', 'cba'))

    def test_complicated(self):
        # a more complicated case, includes numbers / cyrillic / symbols / capital letters
        self.assertTrue(check_str_permutation('пр#иВЕт hel$lo12345', '$helloп#1р2и 3в4е5т'))

    def test_different_length(self):
        self.assertFalse(check_str_permutation('abckld', 'cb'))

    def test_equal_length(self):
        self.assertFalse(check_str_permutation('abcdef', 'abcdeg'))

    def test_empty_string(self):
        # non-empty string is not a permutation of an empty string
        self.assertFalse(check_str_permutation('abcdef', ''))
        # empty string is a permutation of itself
        self.assertTrue(check_str_permutation('', ''))

if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python3
import unittest

class WordDict():

    def __init__(self, w_set, pref_set):
        self.words = w_set
        self.prefixes = pref_set

    def isWord(self, string):
        return string in self.words

    def isPrefix(self, string):
        return string in self.prefixes


def form_prefixes(words):
    """ 
    Input:
        words: set of strings
    Output:
        prefixes: set of strings, all prefixes of all of the strings in words
    """
    prefixes = set()
    for word in words:
        for i in range(len(words)):
            prefixes.add(word[:i+1])
    return prefixes


def DFS(i, j, prefix, visited, n_rows, n_cols, ch_grid, w_dict):
    """ Recursive auxiliary function for word_search """
    words = set()
    potential_w = prefix + ch_grid[i][j]
    if not w_dict.isPrefix(potential_w):
        return set()
    else:
        if w_dict.isWord(potential_w):
            words.add(potential_w)
        visited_new = set(visited)
        visited_new.add((i, j))
        for m in range(max(0, i-1), min(n_rows, i+2)):
            for n in range(max(0, j-1), min(n_cols, j+2)):
                if (m, n) not in visited_new:
                    words.update(DFS(m, n, potential_w, 
                        visited_new, n_rows, n_cols, ch_grid, w_dict))
    return words


def word_search(n_rows, n_cols, ch_grid, w_dict):
    """ 
    Input:
        n_rows: int, equal to the 0' dimension size of ch_grid matrix
        n_cols: int, equal to the 1' dimension size of ch_grid matrix
        ch_grid: list of lists of strings, repesenting an n_rows * n_cols matrix
        w_dict: instance of WordDict class
    Output:
        total_words: set of all words found in ch_grid that are present in w_dict
    """
    total_words = set()
    for i in range(n_rows):
        for j in range(n_cols):
            total_words.update(DFS(i, j, '', set(), n_rows, n_cols, ch_grid, w_dict))
    return total_words


class TestWordSearch(unittest.TestCase):

    def test_simple(self):
        words = set({'CAR', 'CARD', 'CART', 'CAT'})
        prefixes = form_prefixes(words)
        wdict = WordDict(words, prefixes)
        ch_grid = [['A', 'A', 'R'], ['T', 'C', 'D']]
        self.assertEqual(word_search(2, 3, ch_grid, wdict), {'CAR', 'CARD', 'CAT'})
    
    def test_empty_dict(self):
        words = set()
        prefixes = form_prefixes(words)
        wdict = WordDict(words, prefixes)
        ch_grid = [['A', 'A', 'R'], ['T', 'C', 'D']]
        self.assertEqual(word_search(2, 3, ch_grid, wdict), set())

    def test_empty_grid(self):
        words = set({'CAR', 'CARD', 'CART', 'CAT'})
        prefixes = form_prefixes(words)
        wdict = WordDict(words, prefixes)
        ch_grid = []
        self.assertEqual(word_search(0, 0, ch_grid, wdict), set())

    def test_visit_same_cell(self):
        words = set({'ABCD', 'ABCDA', 'AC', 'ACA'})
        prefixes = form_prefixes(words)
        wdict = WordDict(words, prefixes)
        ch_grid = [['A', 'B'], ['D', 'C']]
        self.assertEqual(word_search(2, 2, ch_grid, wdict), {'ABCD', 'AC'})

    def test_different_first_letter(self):
        words = set({'ABC', 'CA', 'AEI', 'AJ', 'DF'})
        prefixes = form_prefixes(words)
        wdict = WordDict(words, prefixes)
        ch_grid = [['A', 'B', 'C'], ['D', 'E', 'F'], ['H', 'I', 'J']]
        self.assertEqual(word_search(3, 3, ch_grid, wdict), {'ABC', 'AEI'})


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
import unittest
import numpy as np

class Graph():

    def __init__(self):
        self.edges = {}
        self.v_sources = set()
        self.v_stocks = set()

    def add_edge(self, v_from, v_to):
        """ Adds an edge to the graph and corresponding vertices to the sets of sources/stocks """
        self.v_sources.add(v_from)
        self.v_stocks.add(v_to)
        if v_from in self.edges:
            self.edges[v_from].append(v_to)
        else:
            self.edges[v_from] = [v_to,]

    def add_vertex(self, v):
        """ Add a vertex to the set of source vertices (suppose that a distinct vertex is a source) """
        self.v_sources.add(v)

    def top_sort(self):
        """ Topological sorting using DFS. Assumes that the graph is a DAG. """
        v_starts = self.v_sources - self.v_stocks
        v_visited = set()
        sorted_list = []
        while len(v_starts):
            start_point = v_starts.pop()
            self.top_sort_recursive(start_point, v_starts, v_visited, sorted_list)
        sorted_list.reverse()
        return sorted_list

    def top_sort_recursive(self, point, v_starts, v_visited, sorted_list):
        """ Auxiliary recursive function for Topological Sorting """
        v_starts.discard(point)
        v_visited.add(point)
        if point in self.edges:
            for next_point in self.edges[point]:
                if next_point not in v_visited:
                    self.top_sort_recursive(next_point, v_starts, v_visited, sorted_list)
        sorted_list.append(point)


def first_uncommon_letter(str1, str2):
    """ 
    Returns an index of the first letter that is different in two strings, -1 if not found
    """
    i = 0
    min_len = min(len(str1), len(str2))
    while str1[i] == str2[i]:
        i += 1
        if i == min_len:
            return -1
    return i


def parse_alphabet(words):
    """
    Returns an alphabet that is consistent with the provided list of words in sorted order.
    Assumes there is at least one possible alphabet for the sequence of words (i.e. no cycles)

    Input:
        words: List of Strings, words in lexicographic order
    """
    letters = Graph()
    for i in range(len(words) - 1):
        for l in words[i]:
            letters.add_vertex(l) # make sure all the letters are in the graph
        let_idx = first_uncommon_letter(words[i], words[i+1])
        if let_idx != -1:
            letters.add_edge(words[i][let_idx], words[i+1][let_idx])
    for l in words[-1]:
        letters.add_vertex(l)
    return letters.top_sort()


class TestAlphabet(unittest.TestCase):

    def check_order(self, alphabet, let1, let2):
        """ 
        Auxiliary function that checks that one letter comes before another
        one in a given alphabet. Assumes alphabet is a List.
        """
        return alphabet.index(let1) < alphabet.index(let2)

    def check_unique(self, alphabet):
        """ Checks that there are no repeating letters in the alphabet """
        letters_set = set()
        for let in alphabet:
            if let in letters_set:
                return False
            else:
                letters_set.add(let)
        return True

    def test_simple(self):
        words = ['ART', 'RAT', 'CAT', 'CAR']
        alphabet = parse_alphabet(words)

        self.assertEqual(len(alphabet), 4)
        self.assertTrue(self.check_unique(alphabet))
        letters_order = [['A', 'R'], ['R', 'C'], ['T', 'R']]
        for rel in letters_order:
            self.assertTrue(self.check_order(alphabet, rel[0], rel[1]))

    def test_undefined_order(self):
        words = ['CAE', 'CAT']
        alphabet = parse_alphabet(words)

        self.assertEqual(len(alphabet), 4)
        self.assertTrue(self.check_unique(alphabet))
        self.assertTrue(self.check_order(alphabet,'E', 'T'))
        self.assertTrue(set(['C', 'A']).issubset(set(alphabet)))

    def test_different_length(self):
        words = ['A', 'BC']
        alphabet = parse_alphabet(words)

        self.assertEqual(len(alphabet), 3)
        self.assertTrue(self.check_unique(alphabet))
        self.assertTrue(self.check_order(alphabet,'A', 'B'))
        self.assertTrue('C' in set(alphabet))

    def test_disjoint_orders(self):
        # A -> B -> C -> F -> G
        # D -> E
        # G -> H
        words = ['A', 'B', 'C', 'CD', 'CE', 'FG', 'FH']
        letters_order = [['A','B'],['B','C'],['C','F'],['F','G'],['D','E'],['G','H']]
        alphabet = parse_alphabet(words)

        self.assertEqual(len(alphabet), 8)
        self.assertTrue(self.check_unique(alphabet))
        for rel in letters_order:
            self.assertTrue(self.check_order(alphabet, rel[0], rel[1]))

    def test_same_word(self):
        words = ['ABC', 'ABC']
        alphabet = parse_alphabet(words)

        self.assertEqual(len(alphabet), 3)
        self.assertTrue(self.check_unique(alphabet))
        self.assertEqual(set(['A', 'B', 'C']), set(alphabet))


if __name__ == '__main__':
    unittest.main()

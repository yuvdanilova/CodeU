#!/usr/bin/env python3
import unittest
import numpy as np

class UnionFindElement():

    def __init__(self, parent):
        self.parent = parent
        self.rank = 0


class UnionFind(): 
    """
    This is an implementation of a union-find (disjoint-set) data structure
    where elements of UnionFindElement class are stored in a dictionary
    """

    def __init__(self):
        self.uf_dict = {}

    def make_set(self, idx):
        self.uf_dict[idx] = UnionFindElement(idx)

    def union(self, i, j):
        """
        If elements are from different sets, performs union and returns 1.
        Returns 0 if both elements are members of the same set.
        """
        root_i = self.uf_dict[self.find(i)]
        root_j = self.uf_dict[self.find(j)]
        if root_i == root_j:
            return 0
        if root_i.rank > root_j.rank:
            root_j.parent = root_i.parent
        elif root_i.rank < root_j.rank:
            root_i.parent = root_j.parent
        else:
            root_i.parent = root_j.parent
            root_j.rank += 1
        return 1

    def find(self, x):
        """ Returns a key of an element in a union-find dict """
        while self.uf_dict[x].parent != x:
            x = self.uf_dict[x].parent
        return x


class IslandMap():

    def __init__(self, nrows, ncols, isl_array):
        self.nrows = nrows
        self.ncols = ncols
        self.islands = isl_array

    def isIsland(self, i, j):
        if (i < 0) or (i >= self.nrows):
            return False
        if (j < 0) or (j >= self.ncols):
            return False
        return self.islands[i][j]

    def countIslands(self):
        """
        Counts islands using a union-find data structure in an iterative way.
        Returns an integer -- number of islands on a map
        """
        isls_uf = UnionFind()
        counter = 0
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.isIsland(i, j):
                    isls_uf.make_set(i * self.ncols + j)
                    counter += 1
                    if self.isIsland(i-1, j):
                        if isls_uf.union((i-1) * self.ncols + j, i * self.ncols + j):
                            counter -= 1
                    if self.isIsland(i, j-1):
                        if isls_uf.union(i * self.ncols + j-1, i * self.ncols + j):
                            counter -= 1
        return counter

    def countIslandsDFS(self, i, j, visited):
        """ Auxiliary recursive function for countIslandsRecursive """
        visited.add(i * self.ncols + j)
        for d in ([0, 1], [1, 0], [0, -1], [-1, 0]):
            new_i = i+d[0]
            new_j = j+d[1]
            if ((new_i * self.ncols + new_j) not in visited) and self.isIsland(new_i, new_j):
                self.countIslandsDFS(new_i, new_j, visited)
        return

    def countIslandsRecursive(self):
        """ 
        Counts islands using Depth-First search in a recursive way.
        """
        visited = set()
        counter = 0
        for i in range(self.nrows):
            for j in range(self.ncols):
                if ((i * self.ncols + j) not in visited) and self.isIsland(i, j):
                    counter += 1
                    self.countIslandsDFS(i, j, visited)
        return counter


class TestCountIslands(unittest.TestCase):

    def test_empty_case(self):
        isl_map = [[0,0,0],[0,0,0],[0,0,0]]
        im = IslandMap(3, 3, isl_map)
        self.assertEqual(im.countIslands(), 0)
        self.assertEqual(im.countIslandsRecursive(), 0)
    
    def test_full_case(self):
        isl_map = [[1,1,1],[1,1,1],[1,1,1]]
        im = IslandMap(3, 3, isl_map)
        self.assertEqual(im.countIslands(), 1)
        self.assertEqual(im.countIslandsRecursive(), 1)

    def test_distinct_islands(self):
        isl_map = [[1,0,0],[0,1,0],[0,0,1]]
        im = IslandMap(3, 3, isl_map)
        self.assertEqual(im.countIslands(), 3)
        self.assertEqual(im.countIslandsRecursive(), 3)

    def test_doughnut(self):
        isl_map = [[1,1,1],[1,0,1],[1,1,1]]
        im = IslandMap(3, 3, isl_map)
        self.assertEqual(im.countIslands(), 1)
        self.assertEqual(im.countIslandsRecursive(), 1)     

    def test_complicated_form(self):
        isl_map = [[0,0,1,0,1,1,1,1,1,1,0,0], [1,1,1,1,1,1,0,0,1,0,0,0]]
        im = IslandMap(2, 12, isl_map)
        self.assertEqual(im.countIslands(), 1)
        self.assertEqual(im.countIslandsRecursive(), 1)   

    def test_disjoint_complicated(self):
        isl_map = [
            [0,0,1,0,1,1,1,1,1,1,0,0], # rows 0 & 1 have one island
            [1,1,1,1,1,1,0,0,1,0,0,0], 
            [0,0,0,0,0,0,0,0,0,0,0,0], # empty line
            [0,0,0,1,1,1,0,0,0,1,0,1], # row 3 has 3 islands
            [0,0,0,0,0,0,0,0,0,0,0,0], # empty row
            [1,1,1,1,1,1,1,1,1,1,1,1]] # row 5 has 1 island
        im = IslandMap(6, 12, isl_map)
        self.assertEqual(im.countIslands(), 5)
        self.assertEqual(im.countIslandsRecursive(), 5)

    def test_doughnut_in_doughnut(self):
        isl_map = [
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,1,0,1],
            [1,0,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1], 
            [1,1,1,1,1,1,1,1,1,1,1,1]]
        im = IslandMap(7, 12, isl_map)
        self.assertEqual(im.countIslands(), 2)
        self.assertEqual(im.countIslandsRecursive(), 2)

    def test_random_matrices(self):
        for i in range(50):
            np.random.seed(i)
            sizes = [(5, 5), (10, 10), (20, 20)]
            probs = [0.2, 0.5, 0.8]
            for mat_size in sizes:
                for prob in probs:
                    isl_map = np.random.binomial(1, prob, size=mat_size)
                    im = IslandMap(mat_size[0], mat_size[1], isl_map)
                    self.assertEqual(im.countIslands(), im.countIslandsRecursive())

if __name__ == '__main__':
    unittest.main()

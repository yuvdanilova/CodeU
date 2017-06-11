#!/usr/bin/env python3
import unittest

class Node:

    def __init__(self, val):
        self.val = val
        self.left_child = None
        self.right_child = None


class BinaryTree:

    def __init__(self):
        self.head = None

    def build_from_list(self, val_list):
        """
        builds a tree from a list in a recursive format
        each node should be in format [val, [], []]
        where the 2nd and the 3rd elements are also node lists
        empty lists [] are leaves
        e.g. [a, [b, [d, [], []], []], [c, [], []]] is for
        a
        |\
        b c
        |
        d
        """
        def add_nodes(val_list):
            if val_list == []:
                return None
            new_node = Node(val_list[0])
            new_node.left_child = add_nodes(val_list[1])
            new_node.right_child = add_nodes(val_list[2])           
            return new_node
        self.head = add_nodes(val_list)

    def print_ancestors(self, val):
        """
        Prints out the ancestors in the format: "ancestor -> ... -> ancestor -> val"
        Returns values of ancestors (excluding val itself) in order from farthest to closest
        """
        def recursive_print_ancestors(val, node):
            # dfs modification
            found = False
            ancestors = []
            if node.val == val:
                found = True
            if (node.left_child != None) and not found:
                [found, ancestors] = recursive_print_ancestors(val, node.left_child)
                if found:
                    ancestors.append(node.val)
            if (node.right_child != None) and not found:
                [found, ancestors] = recursive_print_ancestors(val, node.right_child)
                if found:
                    ancestors.append(node.val)
            return [found, ancestors]

        if self.head == None:
            raise RuntimeError('The tree is empty')

        [found, ancestors] = recursive_print_ancestors(val, self.head)
        ancestors.reverse()
        if not found:
            raise RuntimeError('The vertex not found in the tree')
        else:
            print(' -> '.join([str(x) for x in ancestors] + [str(val),]))
        return ancestors

    def lowest_common_ancestor(self, val1, val2):
        """ 
        Prints the Lowest Common Ancestor of val1 and val2 nodes if both do exist.
        Supposes that there are no duplicates in the tree.

        Returns the Lowest Ancestor value, if found, otherwise throws an error
        """

        def recursive_val_search(val1, val2, _a, _c, node):
            # dfs modification
            a = _a
            c = _c
            if (node.val == val1) or (node.val == val2):
                if a == 1:
                    # found the second vertex
                    return [1, 1, None]
                else:
                    # found the 1st vertex; current vertex could be LA
                    # if we find another one in subtrees. Mark as [0, 1]
                    c = 1
            LA = None

            # below we are looking for vertices in the subtrees
            # case 1: already found a candidate for LA, looking for another vertex. Mark as [1, 0]
            # case 2: haven't found any candidate for LA. Mark as [0, 0]

            # don't update [a, c] in case we haven't found the second vertex and
            # we want to propagate the candidate (marked [0, 1]) above

            if (node.left_child != None):
                if a + c == 1:
                    [a_new, c_new, LA] = recursive_val_search(val1, val2, 1, 0, node.left_child)
                elif a + c == 0:
                    [a_new, c_new, LA] = recursive_val_search(val1, val2, 0, 0, node.left_child)
                if (a == 0) and (c == 1):
                    if (a_new == 1) and (c_new == 1):
                        # print(node.val)
                        LA = node.val
                        a, c = a_new, c_new
                else:
                    a, c = a_new, c_new

            if (node.right_child != None):
                if a + c == 1:
                    [a_new, c_new, LA] = recursive_val_search(val1, val2, 1, 0, node.right_child)
                elif a + c == 0:
                    [a_new, c_new, LA] = recursive_val_search(val1, val2, 0, 0, node.right_child)
                if (a == 0) and (c == 1):
                    if (a_new == 1) and (c_new == 1):
                        LA = node.val
                        a, c = a_new, c_new
                else:
                    a, c = a_new, c_new

            return [a, c, LA]

        if self.head == None:
            raise RuntimeError('The tree is empty')

        if (val1 == val2):
            raise RuntimeError('{0} == {1}: there are no duplicates in the tree'.format(str(val1), str(val2)))

        [a, c, LA] = recursive_val_search(val1, val2, 0, 0, self.head)
        if (LA == None):
            raise RuntimeError('Some of the vertices not found in the tree')
        else:
            return LA


class TestBinaryTree(unittest.TestCase):

    def test_print_ancestors(self):
        """
        1
        | \
        2  5
          / \
          8  10
         /   /
        6   4 
        """
        tree_list = [1, [2, [], []], [5, [8, [6, [], []], []], [10, [4, [], []], []]]]
        btree = BinaryTree()
        btree.build_from_list(tree_list)

        # head, no ancestors
        self.assertEqual(btree.print_ancestors(1), [])

        # values from different subtrees
        self.assertEqual(btree.print_ancestors(2), [1,])
        self.assertEqual(btree.print_ancestors(4), [1, 5, 10])
        self.assertEqual(btree.print_ancestors(8), [1, 5])

        # doesn't exist
        with self.assertRaises(RuntimeError):
            btree.print_ancestors(21)

        # check that it throws an error when the tree is empty
        btree = BinaryTree()
        with self.assertRaises(RuntimeError):
            btree.print_ancestors(1)


    def test_lowest_common_ancestor(self):
        """
        1
        | \
        2  5
          / \
          8  10
         /   /
        6   4 
        """
        tree_list = [1, [2, [], []], [5, [8, [6, [], []], []], [10, [4, [], []], []]]]
        btree = BinaryTree()
        btree.build_from_list(tree_list)

        # check that it throws an error when you input duplicates
        with self.assertRaises(RuntimeError):
            btree.lowest_common_ancestor(5, 5)

        # one is the lowest ancestor of another one
        self.assertEqual(btree.lowest_common_ancestor(1, 2), 1)
        self.assertEqual(btree.lowest_common_ancestor(5, 4), 5)

        # values in different subtrees
        self.assertEqual(btree.lowest_common_ancestor(2, 6), 1)
        self.assertEqual(btree.lowest_common_ancestor(8, 4), 5)

        # one of the values doesn't exist
        with self.assertRaises(RuntimeError):
            btree.lowest_common_ancestor(5, 21)
        with self.assertRaises(RuntimeError):
            btree.lowest_common_ancestor(35, 4)

        # both don't exist
        with self.assertRaises(RuntimeError):
            btree.lowest_common_ancestor(42, 7)

        # check that it throws an error when the tree is empty
        btree = BinaryTree()
        with self.assertRaises(RuntimeError):
            btree.lowest_common_ancestor(5, 5)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
import sys
import unittest

class Node:

    def __init__(self, val, next_node):
        self.val = val
        self.next = next_node


class SinglyLinkedList:

    def __init__(self):
        self.head = None

    def append(self, x):
        self.head = Node(x, self.head)

    def show(self):
        """ Prints all values in the list separated by space """
        curr_node = self.head
        while curr_node != None:
            print(curr_node.val, end=" ")
            curr_node = curr_node.next
        print('\n')

    def kth_from_end(self, k):
        """ Returns k'th element from the end, where 0'th element means identity mapping """
        counter = 0
        kth_el = self.head
        curr_node = self.head
        while curr_node != None:
            counter += 1
            if counter > (k + 1):
                kth_el = kth_el.next
            curr_node = curr_node.next
        if counter < (k + 1):
            raise RuntimeError('Length of the list is smaller than k + 1: {0} < {1}'.format(counter, k + 1))
        else:
            return kth_el.val


class TestSLL(unittest.TestCase):

    def test_simple(self):
        ssl_elements = [0, 1, 2, 3, 4, 5, 6]
        ssl = SinglyLinkedList()
        for el in ssl_elements:
            ssl.append(el)
        for i in range(len(ssl_elements)):
            self.assertEqual(ssl.kth_from_end(i), i)

    def test_mixed(self):
        ssl_elements = [0, 'fhf', 23.5, 'compda']
        ssl = SinglyLinkedList()
        for el in ssl_elements:
            ssl.append(el)
        for i in range(len(ssl_elements)):
            self.assertEqual(ssl.kth_from_end(i), ssl_elements[i])

    def test_kth_existance(self):
        # check that calling for k larger than the lenght of the list throws an exception
        ssl_elements = [0, 1, 2, 3, 4, 5, 6]
        ssl = SinglyLinkedList()
        for el in ssl_elements:
            ssl.append(el)
        with self.assertRaises(RuntimeError):
            ssl.kth_from_end(7)

    def test_empty(self):
        ssl = SinglyLinkedList()
        with self.assertRaises(RuntimeError):
            self.assertRaises(ssl.kth_from_end(0))


if __name__ == '__main__':
    unittest.main()

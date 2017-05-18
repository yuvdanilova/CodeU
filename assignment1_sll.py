# Uses python3
import sys

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


if __name__ == '__main__':
    input = sys.stdin.read()
    *ssl_elements, k = input.split()

    ssl = SinglyLinkedList()
    for el in ssl_elements:
        ssl.append(el)

    if not k.isdigit():
        raise RuntimeError('k is not a digit: {0}'.format(k))

    print(ssl.kth_from_end(int(k)))

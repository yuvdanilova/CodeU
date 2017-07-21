#!/usr/bin/env python3
from statistics import median
import unittest
import numpy as np

class RearrangingArray():

	def __init__(self, arrangement, verbose=False):

		self.arrangement = arrangement
		self.swap_idx = None
		self.order_dict = None
		self.verbose = verbose

	def _swap(self, i, j, k):
		""" Swaps elements on indices i and j using an element on index k """
		if self.verbose:
			print(i, k)
			print(i, j)
			print(j, k)
		self.arrangement[i],self.arrangement[k] = self.arrangement[k],self.arrangement[i]
		self.arrangement[i],self.arrangement[j] = self.arrangement[j],self.arrangement[i]
		self.arrangement[j],self.arrangement[k] = self.arrangement[k],self.arrangement[j]

	def _move_swap_el(self, j):
		""" Moves the swap element to position j from the current position """
		i = self.swap_idx
		while i < j:
			if self.verbose:
				print(i, i+1)
			self.arrangement[i],self.arrangement[i+1]=self.arrangement[i+1],self.arrangement[i]
			i += 1
		while i > j:
			if self.verbose:
				print(i, i-1)
			self.arrangement[i],self.arrangement[i-1]=self.arrangement[i-1],self.arrangement[i]
			i -= 1
		self.swap_idx = j

	def _build_dict(self, new_order):
		""" 
		Builds a dictionary which defines the desired sorting order

		Input:
			new_order: List, a permutation of the class arrangement list
		Output:
			order_dict: Dict, keys are elements of the list, values are
						positions in the sorted list
		"""
		order_dict = {}
		for i, el in enumerate(new_order):
			order_dict[el] = i
		return order_dict

	def _partition(self, l, r):
		""" Partition function for QuickSort sorting algorithm """
		pivot = median([
			self.order_dict[self.arrangement[l]], 
			self.order_dict[self.arrangement[(l+r)//2]], 
			self.order_dict[self.arrangement[r]]]
		)
		while True:
			while ((self.order_dict[self.arrangement[l]] < pivot) or (l == self.swap_idx)) and (l < r):
				l += 1
			while ((self.order_dict[self.arrangement[r]] > pivot) or (r == self.swap_idx)) and (l < r):
				r -= 1
			if l == r:
				break
			self._swap(l, r, self.swap_idx)
		return l

	def _quicksort(self, l, r):
		""" In-place QuickSort sorting algorithm """
		if l < r:
			splitpoint = self._partition(l, r)
			self._quicksort(l, splitpoint-1)
			self._quicksort(splitpoint+1, r)

	def sort(self, new_arrangement):
		""" 
		Sorts the inner arrangement list in-place according
		to the order defined by new_arrangement list

		Input:
			new_arrangement: List, a permutation of the class arrangement list
		"""
		self.order_dict = self._build_dict(new_arrangement)
		self.swap_idx = self.arrangement.index(0)
		self._move_swap_el(len(new_arrangement)-1)
		l = self._quicksort(0, len(new_arrangement)-2)
		self._move_swap_el(self.order_dict[0])


class TestRearranging(unittest.TestCase):

	def test_simple(self):

		init_order = [1, 2, 0, 3]
		new_order = [3, 1, 2, 0]
		rarr = RearrangingArray(init_order, verbose=False)
		rarr.sort(new_order)
		self.assertEqual(rarr.arrangement, new_order)

	def test_random(self):

		for j in range(1, 10001, 10):
			np.random.seed(j)
			init_order = list(np.random.permutation(np.arange(j)))
			np.random.seed(j * 2)
			new_order = list(np.random.permutation(np.arange(j)))
			rarr = RearrangingArray(init_order)
			rarr.sort(new_order)
			self.assertEqual(rarr.arrangement, new_order)


if __name__ == '__main__':
	unittest.main()

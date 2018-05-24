import pytest
import tec.ic.ia.pc2.g08


class TestInput(object):
	""" Test object for validation of the utils module"""

	def test_table_input():
		"""
		Tests an arbitrary input of 14x15 and checks that the dimensions are correct
		"""
		table = utils.load_input("14x15.txt")
		assert len(table) == 15
		assert len(table[0]) == 14

	def test_two_carrot_input():
		"""
		Tests an arbitrary input of 14x15 and checks that it has indeed 2 carrots
		"""
		table = utils.load_input("14x15.txt")
		assert sum(row.count("Z") for row in table) == 2

	def test_bunny_in_table_input():
		"""
		Tests an arbitrary input of 14x15 and checks that it has a bunny
		"""
		table = utils.load_input("14x15.txt")
		assert sum(row.count("C") for row in table) == 1

	def test_correct_table_input():
		"""
		Checks that the input table is according to the default valid characters
		"""

		valid_characters = utils.get_characters()
		
		#Valid table
		table = utils.load_input("14x15.txt")
		assert (element in list(valid_characters.values()) for element in row) for row in table

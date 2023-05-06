import sys
sys.path.append('..')

import unittest

from src.indexed_list import BaseList, IndexedList


class TestIndexedList(unittest.TestCase):

    def setUp(self):
        self.ilist = IndexedList([10, 20, 15, 12])

    def tearDown(self):
        self.ilist._validate()

    def test_validate(self):
        self.assertTrue(self.ilist._validate())

    def test_constructor(self):
        v = IndexedList([2,3,1])
        self.assertListEqual(v._index_values, [1, 2, 3])
        self.assertListEqual(v._index_indices, [2, 0, 1])

    def test_add_with_no_value(self):
        with self.assertRaises(ValueError):
            self.ilist.add()

    def test_add_when_length_is_zero(self):
        ilist = IndexedList()
        ilist.add(5)
        self.assertEqual(len(ilist), 1)
        self.assertEqual(ilist._index_values[0], 5)
        self.assertEqual(ilist._index_indices[0], 0)

    def test_add_when_value_is_minimum(self):
        self.ilist.add(-5)
        self.assertEqual(self.ilist._index_values[0], -5)
        self.assertEqual(self.ilist._index_indices[0], len(self.ilist.values)-1)

    def test_add_when_value_is_maximum(self):
        self.ilist.add(50)
        self.assertEqual(self.ilist._index_values[-1], 50)
        self.assertEqual(self.ilist._index_indices[-1], len(self.ilist.values)-1)

    def test_add_when_value_is_in_middle(self):
        self.ilist.add(13)  # .values is now [10, 20, 15, 12, 13]
        self.assertEqual(self.ilist._index_values[2], 13)
        self.assertEqual(self.ilist._index_indices[2], len(self.ilist.values)-1)

    def test_delete_when_no_value_and_no_index(self):
        with self.assertRaises(ValueError):
            self.ilist.delete()

    def test_delete_when_length_is_one(self):
        ilist = IndexedList([5])
        ilist.delete(index=0)
        self.assertEqual(len(ilist.values), 0)
        self.assertEqual(len(ilist._index_values), 0)
        self.assertEqual(len(ilist._index_indices), 0)

    def test_delete_with_index(self):
        self.ilist.delete(index=1)  # .values is [10, 20, 15, 12]
        self.assertListEqual(self.ilist.values, [10, 15, 12])
        self.assertListEqual(self.ilist._index_values, [10, 12, 15])
        self.assertListEqual(self.ilist._index_indices, [0, 2, 1])

    def test_delete_with_value(self):
        self.ilist.delete(value=15)  # .values is [10, 20, 15, 12]
        self.assertListEqual(self.ilist.values, [10, 20, 12])
        self.assertListEqual(self.ilist._index_values, [10, 12, 20])
        self.assertListEqual(self.ilist._index_indices, [0, 2, 1])

    def test_delete_with_value_not_present_in_list(self):
        with self.assertRaises(ValueError):
            self.ilist.delete(value=29)

    def test_delete_first_entry_via_index(self):
        self.ilist.delete(index=0)
        self.assertListEqual(self.ilist.values, [20, 15, 12])
        self.assertListEqual(self.ilist._index_values, [12, 15, 20])
        self.assertListEqual(self.ilist._index_indices, [2, 1, 0])

        # 10 is also the lowest value ie first in index_values - test again with non-min value
        self.ilist.delete(index=0)
        self.assertListEqual(self.ilist.values, [15, 12])
        self.assertListEqual(self.ilist._index_values, [12, 15])
        self.assertListEqual(self.ilist._index_indices, [1, 0])

    def test_delete_first_entry_via_value(self):
        self.ilist.delete(value=10)
        self.assertListEqual(self.ilist.values, [20, 15, 12])
        self.assertListEqual(self.ilist._index_values, [12, 15, 20])
        self.assertListEqual(self.ilist._index_indices, [2, 1, 0])

        # 10 is also the lowest value ie first in index_values - test again with non-min value
        self.ilist.delete(value=20)
        self.assertListEqual(self.ilist.values, [15, 12])
        self.assertListEqual(self.ilist._index_values, [12, 15])
        self.assertListEqual(self.ilist._index_indices, [1, 0])

    def test_delete_last_entry_via_index(self):
        self.ilist.delete(index=3)  # .values is [10, 20, 15, 12]
        self.assertListEqual(self.ilist.values, [10, 20, 15])
        self.assertListEqual(self.ilist._index_values, [10, 15, 20])
        self.assertListEqual(self.ilist._index_indices, [0, 2, 1])

    def test_delete_last_entry_via_negative_index(self):
        self.ilist.delete(index=-1)
        self.assertListEqual(self.ilist.values, [10, 20, 15])
        self.assertListEqual(self.ilist._index_values, [10, 15, 20])
        self.assertListEqual(self.ilist._index_indices, [0, 2, 1])

    def test_delete_last_entry_via_value(self):
        self.ilist.delete(value=12)
        self.assertListEqual(self.ilist.values, [10, 20, 15])
        self.assertListEqual(self.ilist._index_values, [10, 15, 20])
        self.assertListEqual(self.ilist._index_indices, [0, 2, 1])


    # add some 'generic' test cases - run a couple of scenarios for each method and ensure
    # the output is generally as expected.
    def test_add_generic(self):
        v = IndexedList()

        v.add(5)
        self.assertEqual(len(v.values), 1)
        self.assertEqual(len(v._index_values), 1)
        self.assertListEqual(v._index_values, [5])
        self.assertListEqual(v._index_indices, [0])

        v.add(10)
        self.assertListEqual(v._index_values, [5, 10])
        self.assertListEqual(v._index_indices, [0, 1])

        v.add(7)
        self.assertListEqual(v._index_values, [5, 7, 10])
        self.assertListEqual(v._index_indices, [0, 2, 1])

        v.add(1)
        self.assertListEqual(v._index_values, [1, 5, 7, 10])
        self.assertListEqual(v._index_indices, [3, 0, 2, 1])

        v.add(20)
        self.assertListEqual(v._index_values, [1, 5, 7, 10, 20])
        self.assertListEqual(v._index_indices, [3, 0, 2, 1, 4])

        self.assertEqual(len(v._index_values), len(v.values))

    def test_delete_generic(self):
        v = IndexedList([4,6,9,10,12,14,15])

        v.delete(value=15)
        self.assertEqual(v._index_values, [4, 6, 9, 10, 12, 14])
        self.assertEqual(v._index_indices, [0, 1, 2, 3, 4, 5])

        v.delete(value=4)
        self.assertEqual(v._index_values, [6, 9, 10, 12, 14])
        self.assertEqual(v._index_indices, [0, 1, 2, 3, 4])

        v.delete(value=10)
        self.assertEqual(v._index_values, [6, 9, 12, 14])
        self.assertEqual(v._index_indices, [0, 1, 2, 3])

        v.delete(index=1)
        self.assertEqual(v._index_values, [6, 12, 14])
        self.assertEqual(v._index_indices, [0, 1, 2])

        v.delete(index=2)
        self.assertEqual(v._index_values, [6, 12])
        self.assertEqual(v._index_indices, [0, 1])

        v.delete(index=0)
        self.assertEqual(v._index_values, [12])
        self.assertEqual(v._index_indices, [0])

        v.delete(index=0)
        self.assertEqual(v._index_values, [])
        self.assertEqual(v._index_indices, [])

    def test_query_generic(self):
        v = IndexedList([0,5,5,6,1,3,2,4,5,9,8,7])  # 0-9 with 5 repeated 3 times

        result = v.query(eq=5)
        self.assertListEqual(result, [5, 5, 5])

        result = v.query(gt=5)
        self.assertListEqual(result, [6,9,8,7])

        result = v.query(gte=5)
        self.assertListEqual(result, [5,5,6,5,9,8,7])

        result = v.query(lt=2)
        self.assertListEqual(result, [0,1])

        result = v.query(lte=3)
        self.assertListEqual(result, [0,1,3,2])

        # compound filters
        result = v.query(gt=5, lt=8)
        self.assertListEqual(result, [6,7])

        result = v.query(lt=8, eq=5)
        self.assertListEqual(result, [5,5,5])

        # non-integer queries
        result = v.query(lte=2.9)
        self.assertListEqual(result, [0,1,2])

        result = v.query(lt=4.5)
        self.assertListEqual(result, [0,1,3,2,4])

        result = v.query(gte=5.9)
        self.assertListEqual(result, [6,9,8,7])

        # non-integer compound query
        result = v.query(gt=4.9, lt=6.1)
        self.assertListEqual(result, [5,5,6,5])

        # bad input
        result = v.query(gt=8, lt=7)
        self.assertListEqual(result, [])

    # Validate vs BaseList
    def test_vs_baselist(self):

        def assert_methods_equal(baselist, indexedlist, value=3):
            # run a bunch of methods using the same value and ensure the results are the same for both
            self.assertEqual(baselist.query(eq=value), indexedlist.query(eq=value))
            self.assertEqual(baselist.query(gt=value), indexedlist.query(gt=value))
            self.assertEqual(baselist.query(lt=value), indexedlist.query(lt=value))

        setup = [1,7,3,5,6,6,0,3,2]
        baselist = BaseList(setup)
        indexedlist = IndexedList(setup)
        assert_methods_equal(baselist, indexedlist)

        baselist.delete(index=0)
        indexedlist.delete(index=0)
        assert_methods_equal(baselist, indexedlist)

        baselist.delete(value=0)
        indexedlist.delete(value=0)
        assert_methods_equal(baselist, indexedlist)

        baselist.add(29)
        indexedlist.add(29)
        assert_methods_equal(baselist, indexedlist)

        baselist.add(0)
        indexedlist.add(0)
        assert_methods_equal(baselist, indexedlist)


if __name__ == '__main__':
    unittest.main()

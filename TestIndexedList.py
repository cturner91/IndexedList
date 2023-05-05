import unittest

from IndexedList import IndexedList


class TestIndexedList(unittest.TestCase):

    def test_init(self):
        v = IndexedList([2,3,1])
        self.assertListEqual(v.index_values, [1, 2, 3])
        self.assertListEqual(v.index_indices, [2, 0, 1])

    def test_add(self):
        v = IndexedList()

        v.add(5)
        self.assertEqual(len(v.values), 1)
        self.assertEqual(len(v.index_values), 1)
        self.assertListEqual(v.index_values, [5])
        self.assertListEqual(v.index_indices, [0])

        v.add(10)
        self.assertListEqual(v.index_values, [5, 10])
        self.assertListEqual(v.index_indices, [0, 1])

        v.add(7)
        self.assertListEqual(v.index_values, [5, 7, 10])
        self.assertListEqual(v.index_indices, [0, 2, 1])

        v.add(1)
        self.assertListEqual(v.index_values, [1, 5, 7, 10])
        self.assertListEqual(v.index_indices, [3, 0, 2, 1])

        v.add(20)
        self.assertListEqual(v.index_values, [1, 5, 7, 10, 20])
        self.assertListEqual(v.index_indices, [3, 0, 2, 1, 4])

        self.assertEqual(len(v.index_values), len(v.values))


    def test_delete(self):
        v = IndexedList([4,6,9,10,12,14,15])

        v.delete(value=15)
        self.assertEqual(v.index_values, [4, 6, 9, 10, 12, 14])
        self.assertEqual(v.index_indices, [0, 1, 2, 3, 4, 5])

        v.delete(value=4)
        self.assertEqual(v.index_values, [6, 9, 10, 12, 14])
        self.assertEqual(v.index_indices, [0, 1, 2, 3, 4])

        v.delete(value=10)
        self.assertEqual(v.index_values, [6, 9, 12, 14])
        self.assertEqual(v.index_indices, [0, 1, 2, 3])

        v.delete(index=1)
        self.assertEqual(v.index_values, [6, 12, 14])
        self.assertEqual(v.index_indices, [0, 1, 2])

        v.delete(index=2)
        self.assertEqual(v.index_values, [6, 12])
        self.assertEqual(v.index_indices, [0, 1])

        v.delete(index=0)
        self.assertEqual(v.index_values, [12])
        self.assertEqual(v.index_indices, [1])

        v.delete(index=0)
        self.assertEqual(v.index_values, [])
        self.assertEqual(v.index_indices, [])

    def test_query(self):
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


if __name__ == '__main__':
    unittest.main()

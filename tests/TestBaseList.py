import sys
sys.path.append('..')

import unittest

from src.indexed_list import BaseList


class TestBaseList(unittest.TestCase):

    def test_init(self):
        v = BaseList()
        self.assertEqual(len(v.values), 0)

        v = BaseList([1,2,3])
        self.assertEqual(len(v.values), 3)
        self.assertIn(1, v.values)
        self.assertIn(2, v.values)
        self.assertIn(3, v.values)

    def test_add(self):
        v = BaseList()

        v.add(1)
        self.assertEqual(len(v.values), 1)
        self.assertIn(1, v.values)

        v.add(17)
        self.assertEqual(len(v.values), 2)
        self.assertIn(17, v.values)

    def test_delete(self):
        v = BaseList([4,6,9,10])

        v.delete(value=9)
        self.assertEqual(len(v.values), 3)
        self.assertIn(4, v.values)
        self.assertIn(6, v.values)
        self.assertIn(10, v.values)

        v.delete(index=1)
        self.assertEqual(len(v.values), 2)
        self.assertIn(4, v.values)
        self.assertIn(10, v.values)

        with self.assertRaises(ValueError):
            v.delete(value=34)

        with self.assertRaises(IndexError):
            v.delete(index=34)

    def test_query(self):
        v = BaseList([0,1,2,3,4,5,5,5,6,7,8,9])

        result = v.query(eq=5)
        self.assertEqual(len(result), 3)

        result = v.query(gt=5)
        self.assertEqual(len(result), 4)

        result = v.query(gte=5)
        self.assertEqual(len(result), 7)

        result = v.query(lt=2)
        self.assertEqual(len(result), 2)

        result = v.query(lte=2)
        self.assertEqual(len(result), 3)

        # multiple inputs
        result = v.query(lte=2, gt=0)
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

        result = v.query(gte=6, lt=100)
        self.assertEqual(len(result), 4)
        self.assertIn(6, result)
        self.assertIn(7, result)
        self.assertIn(8, result)
        self.assertIn(9, result)


if __name__ == '__main__':
    unittest.main()

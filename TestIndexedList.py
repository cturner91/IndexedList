import unittest

from IndexedList import IndexedList


class TestIndexedList(unittest.TestCase):

    # def test_init(self):
    #     v = IndexedList([2,3,1])

    #     self.assertEqual(len(v.index), 3)

    #     self.assertListEqual(v.index, [
    #         [1, 2],
    #         [2, 0],
    #         [3, 1],
    #     ])
        

    def test_add(self):
        v = IndexedList()

        v.add(5)
        self.assertEqual(len(v.values), 1)
        self.assertEqual(len(v.index), 1)
        self.assertListEqual(v.index, [
            [5, 0]
        ])

        v.add(10)
        self.assertListEqual(v.index, [
            [5, 0],
            [10, 1],
        ])

        v.add(7)
        self.assertListEqual(v.index, [
            [5, 0],
            [7, 2],
            [10, 1],
        ])

        v.add(1)
        self.assertListEqual(v.index, [
            [1, 3],
            [5, 0],
            [7, 2],
            [10, 1],
        ])

        v.add(20)
        self.assertListEqual(v.index, [
            [1, 3],
            [5, 0],
            [7, 2],
            [10, 1],
            [20, 4],
        ])

        self.assertEqual(len(v.index), len(v.values))


    # def test_delete(self):
    #     v = IndexedList([4,6,9,10])

    # def test_query(self):
    #     v = IndexedList([0,1,2,3,4,5,5,5,6,7,8,9])


if __name__ == '__main__':
    unittest.main()

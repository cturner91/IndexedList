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


    def test_delete(self):
        v = IndexedList([4,6,9,10,12,14,15])

        v.delete(value=15)
        self.assertEqual(v.index, [
            [4, 0],
            [6, 1],
            [9, 2],
            [10, 3],
            [12, 4],
            [14, 5],
        ])

        v.delete(value=4)
        self.assertEqual(v.index, [
            [6, 0],
            [9, 1],
            [10, 2],
            [12, 3],
            [14, 4],
        ])

        v.delete(value=10)
        self.assertEqual(v.index, [
            [6, 0],
            [9, 1],
            [12, 2],
            [14, 3],
        ])

        v.delete(index=1)
        self.assertEqual(v.index, [
            [6, 0],
            [12, 1],
            [14, 2],
        ])

        v.delete(index=2)
        self.assertEqual(v.index, [
            [6, 0],
            [12, 1],
        ])


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


if __name__ == '__main__':
    unittest.main()

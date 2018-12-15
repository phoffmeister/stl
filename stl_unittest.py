import unittest
from stl import Vector3


class Vector3Test(unittest.TestCase):
    def test_vec_to_str(self):
        self.assertEqual(str(Vector3(1, 2, 3)), '1, 2, 3')
        self.assertEqual(str(Vector3(0, 0, 0)), '0, 0, 0')
        self.assertEqual(str(Vector3(-1, 2, 3)), '-1, 2, 3')
        self.assertEqual(str(Vector3(1000, 2, 3)), '1000, 2, 3')

    def test_vec_eq(self):
        self.assertEqual(Vector3(1, 2, 3), Vector3(1, 2, 3))
        self.assertEqual(Vector3(3, -33, 99), Vector3(3, -33, 99))
        self.assertFalse(Vector3(1, 2, 3) == Vector3(3, 2, 1))

    def test_vec_add(self):
        a = Vector3(1, 2, 3)
        b = Vector3(4, 2, -9)
        c = Vector3(1, 2, 3)
        e1 = Vector3(5, 4, -6)
        e2 = Vector3(2, 4, 6)

        self.assertEqual(a + b, e1)
        self.assertEqual(a + c, e2)


if __name__ == '__main__':
    unittest.main()

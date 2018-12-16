import unittest
from d3obj import Vector3


class Vector3Test(unittest.TestCase):
    def test_vec_to_str(self):
        self.assertEqual(str(Vector3(1, 2, 3)), '1.0, 2.0, 3.0')
        self.assertEqual(str(Vector3(0, 0, 0)), '0.0, 0.0, 0.0')
        self.assertEqual(str(Vector3(-1, 2, 3)), '-1.0, 2.0, 3.0')
        self.assertEqual(str(Vector3(1000, 2, 3)), '1000.0, 2.0, 3.0')

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

    def test_vec_mul(self):
        a = Vector3(1, 2, 3)
        b = Vector3(4, 5, 6)
        s = 7
        self.assertEqual(a * s, Vector3(7, 14, 21))
        self.assertEqual(b * s, Vector3(28, 35, 42))
        self.assertEqual(a * b, Vector3(-3, 6, -3))

    def test_vec_div(self):
        a = Vector3(9, 12, 36)
        self.assertEqual(a / 3, Vector3(3, 4, 12))

    def test_vec_unify(self):
        a = Vector3(1, 2, 2)
        a.unify()
        self.assertEqual(a, Vector3(1/float(3), 2/float(3), 2/float(3)))


if __name__ == '__main__':
    unittest.main()

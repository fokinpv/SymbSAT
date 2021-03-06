# pylint: disable=invalid-name
import unittest

from symbsat.monom import Monom4 as Monom


class TestBoolMonom(unittest.TestCase):

    def setUp(self):
        #  Monom.size = 4
        self.variables = (
            Monom(vars=[0]),  # a
            Monom(vars=[1]),  # b
            Monom(vars=[2]),  # c
            Monom(vars=[3]),  # d
        )

    def test_init(self):
        abcd = Monom((1, 1, 1, 1))
        ab = Monom(vars=[0, 1])
        abc = Monom(vars=[0, 1, 2])
        c = Monom(vars=[2])
        d = Monom(vars=[3])
        _0 = Monom()

        self.assertEqual(abcd.bits, (1, 1, 1, 1))
        self.assertEqual(abc.bits, (1, 1, 1, 0))
        self.assertEqual(ab.bits, (1, 1, 0, 0))
        self.assertEqual(c.bits, (0, 0, 1, 0))
        self.assertEqual(d.bits, (0, 0, 0, 1))
        self.assertTrue(_0.is_zero())

    def test_one(self):
        _1 = Monom.one()
        self.assertTrue(_1.is_one())
        self.assertFalse(_1.is_zero())

    def test_zero(self):
        _0 = Monom.zero()
        self.assertTrue(_0.is_zero())
        self.assertFalse(_0.is_one())

    def test_str(self):
        _0 = Monom.zero()
        self.assertEqual(str(_0), '0')

        _1 = Monom.one()
        self.assertEqual(str(_1), '1')

    def test_mul(self):
        a, b = self.variables[:2]

        self.assertEqual(a*a, a)
        self.assertEqual(b*a, a*b)

        _0 = Monom.zero()
        self.assertEqual(a*_0, _0)
        self.assertEqual(_0*a, _0)

        _1 = Monom.one()
        self.assertEqual(a*_1, a)
        self.assertEqual(_1*a, a)

    def test_truediv(self):
        a, b, c = self.variables[:3]

        ab = a*b
        bc = b*c
        abc = a*b*c

        _1 = Monom.one()

        # 1/a == 0
        self.assertTrue((_1/a).is_zero())
        # a == a/1
        self.assertEqual(a, a/_1)
        # a/b == 0
        self.assertTrue((a/b).is_zero())
        # ab/b == a
        self.assertEqual(a, ab/b)
        # ab/a == b
        self.assertEqual(b, ab/a)
        # abc/ab == c
        self.assertEqual(c, abc/ab)
        # ab/bc == 0
        self.assertTrue((ab/bc).is_zero())

    def test_isdivisible(self):
        a, b, c = self.variables[:3]
        _1 = Monom.one()

        self.assertFalse(_1.isdivisible(a))

        self.assertTrue(_1.isdivisible(_1))

    def test_isrelativelyprime(self):
        a, b, c = self.variables[:3]

        self.assertTrue(a.isrelativelyprime(b))

        ac = a*c
        self.assertTrue(ac.isrelativelyprime(b))

        self.assertTrue(a.isrelativelyprime(a))

        ab = a*b
        self.assertFalse(ab.isrelativelyprime(b))

    def test_lcm(self):
        self.assertTrue(True)

    def test_vars(self):
        a, b, c = self.variables[:3]

        ac = a*c

        self.assertEqual([0, 2], ac.vars)

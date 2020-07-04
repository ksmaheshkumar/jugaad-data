import unittest
from jugaad_data import util as ut

import numpy as np

class TestUtil(unittest.TestCase):

    def test_np_float_normal(self):
        f = ut.np_float("3.3")
        self.assertAlmostEqual(f, 3.3)

    def test_np_float_dash(self):
        f = ut.np_float("-")
        self.assertTrue(np.isnan(f))
    
    def test_np_date_normal(self):
        d1 = ut.np_date("30-Dec-2019")
        d2 = np.datetime64("2019-12-30")
        self.assertEqual(d1,d2)

    def test_np_date_nat(self):
        d = ut.np_date("32-Dec-2019")
        self.assertTrue(np.isnat(d))

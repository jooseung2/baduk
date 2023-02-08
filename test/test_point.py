import unittest
import json
import sys
import os
sys.path.append(os.path.abspath('../src'))

from point import Point

class Test(unittest.TestCase):
    def test_validate_point_str(self):
        pt1 = "5-c"
        pt2 = "5.2-2"
        pt3 = "a-b"
        pt3 = "ahaah"
        pt4 = "2-5.3"
        pt5 = "2-3-4"
        pt6 = "0-19"
        pt7 = "0-10"
        pt8 = "1-20"

        pts = [pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8]
        for ind, i in enumerate(pts):
            self.assertFalse(Point.validate_point_str(i))
    
    def test_comparisons(self):
        pt22 = Point.from_str("2-2")
        pt23 = Point.from_str("2-3")
        pt32 = Point.from_str("3-2")
        pt33 = Point.from_str("3-3")
        another22 = Point.from_str("2-2")
        # eq
        self.assertTrue(another22 == pt22)
        #ne
        self.assertTrue(pt22 != pt23)
        self.assertTrue(pt22 != pt33)
        # gt
        self.assertTrue(pt32 > pt22)
        # ge
        self.assertTrue(pt32 >= pt22)
        self.assertTrue(pt33 >= pt22)
        self.assertTrue(pt22 >= another22)
        self.assertFalse(pt23 >= pt33)
        # lt
        # showing ge works is enough to show lt works
        # le
        # showing gt works is enough to show le works

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python

import unittest
import xmlrunner
from math import atan2, degrees


class DirectionChecks(unittest.TestCase):
    def testNWDirection(self):
        '''Tests the direction returned between two coords lying in a NW direction is correct.'''
        self.failUnless(getBearing((0,0), (10, 10)) == 45)


def getBearing((start_lat, start_lng), (end_lat, end_lng)):
    '''Returns the initial bearing between two lat lng points.
    http://www.movable-type.co.uk/scripts/latlong.html'''
    return(degrees(atan2(end_lng - start_lng, end_lat - start_lat)))


def main():
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_reports'))

if __name__ == "__main__":
    main()

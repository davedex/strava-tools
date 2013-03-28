#!/usr/bin/env python

import unittest
import xmlrunner
from math import atan2, degrees
from geopy import geocoders

class BearingError(Exception): pass

def getBearing((start_lat, start_lng), (end_lat, end_lng)):
    '''Returns the initial bearing between two lat lng points.
    http://www.movable-type.co.uk/scripts/latlong.html'''
    if not ((-90 <= start_lat <= 90) and (-90 <= start_lng <= 90) and
            (-90 <= end_lat <= 90) and (-90 <= end_lng <= 90)):
        raise(BearingError)
    return(degrees(atan2(end_lng - start_lng, end_lat - start_lat)))

def getLocation(lat, lng):
    '''Uses geopy's reverse geocoding to get a location from a point'''
    g = geocoders.GeoNames()
    (place, point) = g.reverse((lat, lng))
    return place


class BearingChecks(unittest.TestCase):
    def testKnownBearing(self):
        '''Tests the direction returned between two coords lying in a NW direction is correct.'''
        self.failUnless(getBearing((0,0), (10, 10)) == 45)
        self.failUnless(getBearing((-10,-10), (0, 0)) == 45)

    def testErroneousCoordinates(self):
        '''Tests that coords with values outside -90 to 90 fail'''
        self.failUnlessRaises(BearingError, getBearing, (0,0), (10,91))
        self.failUnlessRaises(BearingError, getBearing, (0,0), ('a',10))
        self.failUnlessRaises(BearingError, getBearing, (0,90.0001), (10,91))
        self.failUnlessRaises(BearingError, getBearing, (-100000.0,0), (10,91))
        self.failUnlessRaises(BearingError, getBearing, (-180,180), (120,120))


class ReverseGeocode(unittest.TestCase):
    def testKnownLocation(self):
        '''Tests a known location can be looked up from it's coordinates'''
        self.failUnless(getLocation(37.41785, -122.12793) == u"3998 Ventura Ct, Palo Alto, US 94306")

def main():
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_reports'))

if __name__ == "__main__":
    main()

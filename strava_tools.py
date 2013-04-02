#!/usr/bin/env python

import unittest
import xmlrunner
from math import atan2, degrees
# from geopy import geocoders
import json
import urllib2


class CoordError(Exception): pass

def getBearing((start_lat, start_lng), (end_lat, end_lng)):
    '''Returns the initial bearing between two lat lng points.
    http://www.movable-type.co.uk/scripts/latlong.html'''
    if not ((-90 <= start_lat <= 90) and (-180 <= start_lng <= 180) and
            (-90 <= end_lat <= 90) and (-180 <= end_lng <= 180)):
        raise(CoordError)
    return(degrees(atan2(end_lng - start_lng, end_lat - start_lat)))

def getLocation(lat, lng):
    '''Uses google's reverse geocoding functionality to get a location from a point'''
    if not ((-90 <= lat <= 90) and (-180 <= lng <= 180)):
        raise(CoordError)
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng) + "&sensor=true"
    google_response = urllib2.urlopen(url)
    json_response = json.loads(google_response.read())
    return json.dumps(json_response['results'][0]['formatted_address']).replace('"', '')


class BearingChecks(unittest.TestCase):
    def testKnownBearing(self):
        '''Tests the direction returned between two coords lying in a NW direction is correct.'''
        self.failUnless(getBearing((0,0), (10, 10)) == 45)
        self.failUnless(getBearing((-10,-10), (0, 0)) == 45)

    def testErroneousCoordinates(self):
        '''Tests that impossible coords fail'''
        self.failUnlessRaises(CoordError, getBearing, (0,0), (10,181))
        self.failUnlessRaises(CoordError, getBearing, (0,0), ('a',10))
        self.failUnlessRaises(CoordError, getBearing, (0,180.0001), (10,181))
        self.failUnlessRaises(CoordError, getBearing, (-100000.0,0), (10,181))
        self.failUnlessRaises(CoordError, getBearing, (-180,180), (120,120))


class ReverseGeocode(unittest.TestCase):
    def testKnownLocation(self):
        '''Tests a known location can be looked up from it's coordinates'''
        self.failUnless(getLocation(52.206167, 0.125281) == u"13 Emmanuel Road, Cambridge CB1, UK")
        self.failUnless(getLocation(37.41785, -122.12793) == u"3951 Ventura Court, Palo Alto, CA 94306, USA")

    def testErroneousCoordinates(self):
        '''Tests that impossible coords fail'''
        self.failUnlessRaises(CoordError, getLocation, 91, 0)
        self.failUnlessRaises(CoordError, getLocation, 0, 181)
        self.failUnlessRaises(CoordError, getLocation, -91, 0)
        self.failUnlessRaises(CoordError, getLocation, 0, -181)
        self.failUnlessRaises(CoordError, getLocation, 'a', 0)
        self.failUnlessRaises(CoordError, getLocation, 0, u'!')
        self.failUnlessRaises(CoordError, getLocation, 90.0001, 0)
        self.failUnlessRaises(CoordError, getLocation, 0, -181.00001)

def main():
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_reports'))

if __name__ == "__main__":
    main()

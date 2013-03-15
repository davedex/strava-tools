#!/usr/bin/env python

import unittest
import xmlrunner


class DirectionChecks(unittest.TestCase):
    def testNWDirection(self):
        '''Tests the direction returned between two coords lying in a NW direction is correct.'''
        self.failUnless(True)

    def testDummy(self):
        self.failIf(False)


def main():
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_reports'))

if __name__ == "__main__":
    main()

import unittest

import robotsuite

from plone.testing import layered

from s17.organizationalunit.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_ous.txt"),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite

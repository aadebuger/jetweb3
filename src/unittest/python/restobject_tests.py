'''
Created on Nov 14, 2015

@author: aadebuger
'''
import unittest

from jetcloud import restobject
class Test(unittest.TestCase):


    def testrest2mongo(self):
            print 'rest2mongo'
            restobject.rest2mongo({})
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testrest2mongo']
    unittest.main()
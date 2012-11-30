'''
Created on Nov 28, 2012

@author: marek
'''
import unittest
import json
from sk.marek.barak.paxos.Util import Util

class Test(unittest.TestCase): 


    def testName(self):
        u = Util()
        u.getValue()
        u.getValue()
        u.getValue()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Nov 28, 2012

@author: marek
'''
import unittest
import json

class Test(unittest.TestCase): 


    def testName(self):
        l = list()
        l.append("marek")
        l.append("16")
        s = str(l)
        s = s.replace("[", "")
        s = s.replace("]", "")
        s = s.replace(" ", "")
        s = s.replace("'", "")
        val = s.split(",")
        for i in val:
            print i
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
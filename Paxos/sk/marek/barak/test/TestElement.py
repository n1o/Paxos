'''
Created on Nov 28, 2012

@author: marek
'''
import unittest
import json
from sk.marek.barak.paxos.Client import Item


class Test(unittest.TestCase):


    def testName(self):
        element = Item("Tabulka",json)
        self.assertEqual(element.getName(), "Tabulka")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Nov 28, 2012

@author: marek
'''
import unittest
import time
from sk.marek.barak.paxos.Util import Util
import mysql.connector


class Test(unittest.TestCase): 


    def testName(self):
        
        conx = mysql.connector.connect(user='marek',database='PocitacoveSiete',password='pocitacovesiete')
        curA = conx.cursor(buffered=True)
        query = ("insert into User(user_id,name,last_name,age)"
                 "values(%s,%s,%s,%s)")
        curA.execute(query,('891001/7204','Marek','Barak',23))
        for i in curA:
            print i
        conx.commit()
        conx.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
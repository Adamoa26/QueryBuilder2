from unittest import TestCase
import datetime
from ..features.macfinder import broquery
from ..features.macfinder import esquery


class TestConsole(TestCase):
   #def test_basic(self):

   #def emailparser_test(self):
      #test = emailparser('/home/adam/Documents/ElasticSearch/Automation/querybuilder/tests/testfiles/Email1.txt', 'ES')
      #print test.doAll()

   def broTest(self):
      brotest = broquery.BroQuery(datetime.datetime(2014, 11, 9, 11, 53, 4, 770000), '129.15.127.238', '56787', '22297915215')
      brotest.doall()

   def esqueryTest(self):
      estest = esquery.EsQuery(datetime.datetime(2014, 11, 9, 11, 53, 4, 770000), '129.15.127.238', '56787', '22297915215')
      estest.doAll()


test = TestConsole()
test.broTest()
test.esqueryTest()
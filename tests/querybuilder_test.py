from unittest import TestCase
from modules import emailparser


class TestConsole(TestCase):
   def test_basic(self):

   def emailparser_test(self):
      test = emailparser('/home/adam/Documents/ElasticSearch/Automation/querybuilder/tests/testfiles/Email1.txt', 'ES')
	  print test.doAll()



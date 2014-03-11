import unittest
import configGenerator 

class configGenerator_test(unittest.TestCase):
	def test_mergeXML(self):
		cg = configGenerator.ConfigGenerator()
		cg.loadPlist(file('data/new/xsl_plain.plist').read())
		cg.loadXML(file('data/new/test.xml').read())
		print cg.generateConfig('/tmp/testino')

		#self.assertEquals(new, expected)





if __name__ == '__main__':
	unittest.main()	

#EOF

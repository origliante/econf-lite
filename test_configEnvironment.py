

import configEnvironment
import configSnapshot
import unittest
import utils.delete
import time

class ConfigEnvironment_test(unittest.TestCase):
	def test_creation_and_check(self):
		utils.delete.recursive_delete('/tmp/cenv')
		utils.delete.recursive_delete('/tmp/root-config/')
		os.mkdir('/tmp/root-config/')
		# init config environment
		ce = configEnvironment.ConfigEnvironment('/tmp/cenv/')
		ce.initEnvironment()

		print ce.listSnapshots()

		# generazione cfg, ritorna gli md5
		ce.generateSystemConfig('./data/new', '/tmp/root-config/')

		# check
		ce.checkSystemConfig()

		#
		ce.closeEnvironment()

	def _test_open(self):
		ce = configEnvironment.ConfigEnvironment('/tmp/cenv/')
		ce.openEnvironment()
		print ce.listSnapshots()
		ce.closeEnvironment()


import os

if __name__ == '__main__':
	#try:
	#	utils.delete.recursive_delete('/tmp/cenv')
	#except: pass
	#os.mkdir('/tmp/cenv')
	unittest.main()

#EOF

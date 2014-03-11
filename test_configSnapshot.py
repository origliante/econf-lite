import unittest
import configSnapshot 
import os
import time


class snapshot_test(unittest.TestCase):
	def test_init(self):
		currTime = int(time.time())
		lclTime = time.localtime( currTime )
	        cn = configSnapshot.ConfigSnapshot('/tmp/test-snap/' + time.strftime("%d-%m-%Y_%H:%M.%S", lclTime) + '/')
        	cn.setSnapshotInfo(currTime, 'mysnapname', 'a long and exaustive description.')
        	self.assertEqual( cn.getSnapshotInfo(), (str(currTime), 'mysnapname', 'a long and exaustive description.') )
		#
        	cn.die()

#	def test_plist(self):
 #               currTime = int(time.time())
  #              lclTime = time.localtime( currTime )
   #             cn = configSnapshot.ConfigSnapshot('/tmp/test-snap/' + time.strftime("%d-%m-%Y_%H:%M.%S", lclTime) + '/')
#		cn.setSnapshotInfo(currTime, 'mysnapname', 'a long and exaustive description.')
#		cn.loadConfigFiles('./data/xml/', './data/xsl/', './test/')
		#cn.
####################################################

import stat
from utils.delete import recursive_delete


if __name__ == '__main__':
	try:
		recursive_delete('/tmp/test-snap')
	except: pass

        os.mkdir('/tmp/test-snap')

	unittest.main()

#EOF

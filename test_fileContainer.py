import unittest
import fileContainer



class fileContainer_test(unittest.TestCase):
	def tes_create(self):
        	fc = fileContainer.FileContainer('/tmp/fc/fc1.db')
	        fc.create()
        	fc.addFile('/tmp/fc/testfile1')
        	data = fc.getFile('/tmp/fc/testfile1')
		self.assertEqual('ABCEFGHI', data)
        	fc.close()

	def test_singleton(self):
                fc = fileContainer.FileContainer('/tmp/fc/fc1.db')
                fc.create()
                fc.addFile('/tmp/fc/testfile1')
                data = fc.getFile('/tmp/fc/testfile1')
                self.assertEqual('ABCEFGHI', data)
                fc.close()

                fc = fileContainer.FileContainer('/tmp/fc/fc1.db')
		fc.open()
                data = fc.getFile('/tmp/fc/testfile1')
                fc.close()


	def tes_open(self):
        	fc2 = fileContainer.FileContainer('/tmp/fc/fc1.db')
	        fc2.open()
        	data = fc2.getFile('/tmp/fc/testfile1')
		self.assertEqual('ABCEFGHI', data)
	        fc2.delFile('/tmp/fc/testfile1')
		try:
			fc2.getFile('/tmp/fc/testfile1')
		except IOError, msg:
			self.assertEqual('DBSoul: getKey(): no such key "/tmp/fc/testfile1"', str(msg))

        	fc2.addFile('/tmp/fc/testfile2')
       		data = fc2.getFile('/tmp/fc/testfile2')
		self.assertEqual('1238123876', data)
		fc2.delFile('/tmp/fc/testfile2')
		print fc2.getFileNames()
	        fc2.close()




###############
from utils.delete import recursive_delete
import os
if __name__ == '__main__':

	try:
		recursive_delete('/tmp/fc')
	except: pass

        if not os.access('/tmp/fc', os.F_OK):
                os.mkdir('/tmp/fc')

        f1 = file('/tmp/fc/testfile1', 'w+')
        f1.write('ABCEFGHI')
        f1.close()
                                                                                                                             
        f2 = file('/tmp/fc/testfile2', 'w+')
        f2.write('1238123876')
        f2.close()

	unittest.main()

#EOF

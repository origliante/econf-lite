import unittest
import indexContainer
import os



class index_test(unittest.TestCase):
	def tst_init(self):
		ic = indexContainer.IndexContainer('/tmp/test/index.db')
		ic.initIndexContainer()

		lt = {} 
		lt['name'] = 'DEFAULT_SNAPSHOT_NAME'
                lt['description'] = 'Empty snapshot description.'
                lt['xsl.db'] = ''
                lt['xml.db'] = ''
                #lt['md5.db'] = ''

		ik = ic.runKeys()
		for k in lt:
			for k2 in ik:
				if k == k2:
					break
			self.assertEqual(k, k2)

		ic.dbFilesCheck()
		ic.close()

	def test_single(self):
                ic = indexContainer.IndexContainer('/tmp/test/index.db')
                ic.initIndexContainer()
                ic.close()

                ic = indexContainer.IndexContainer('/tmp/test/index.db')
                ic.initIndexContainer()
                ic.close()


####################################################

import stat

def recdelete(path):
        s = os.lstat(path)
                                                                                                                             
        if not stat.S_ISDIR(s.st_mode):
                print '%s is not a directory' % path
                                                                                                                             
        lt = os.listdir(path)
        for elem in lt:
                fpath = os.path.join(path, elem)
                s = os.lstat(fpath)
                if stat.S_ISDIR(s.st_mode):
                        recdelete(fpath)
                else:
                        os.unlink(fpath)
        os.rmdir(path)


if __name__ == '__main__':

	recdelete('/tmp/test')
        os.mkdir('/tmp/test')

	f = file('/tmp/test/xsl.db', 'w+')
        f.write('TEMPLATES')
        f.close()
        f = file('/tmp/test/xml.db', 'w+')
        f.write('XML')
        f.close()
        f = file('/tmp/test/md5.db', 'w+')
        f.write('MD5')
        f.close()

	unittest.main()

#EOF

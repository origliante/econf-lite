#
#
import unittest
import md5
import dbSoul
import random

class dbSoul_test(unittest.TestCase):
	def test_open_close(self):
		d = dbSoul.DBSoul('/tmp/unittest/test1.db')
		try:
			d.open()
		except Exception, msg:
			self.assertEqual(str(msg), 'DBSoul: openDb(): database not found')
		self.assertEqual(d.isDbOpened(), False)

		try:
			d.close()
		except Exception, msg:
			self.assertEqual(str(msg), 'DBSoul: close(): database is closed')
		self.assertEqual(d.isDbOpened(), False)

	def test_openopen(self):
                d = dbSoul.DBSoul('/tmp/unittest/test10.db')
                try:
                        d.open()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: openDb(): database not found')
                self.assertEqual(d.isDbOpened(), False)
                                                       
                d = dbSoul.DBSoul('/tmp/unittest/test10.db')
                try:
                        d.open()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: openDb(): database not found')
                self.assertEqual(d.isDbOpened(), False)
                                                                                                                             
                try:
                        d.close()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: close(): database is closed')
                self.assertEqual(d.isDbOpened(), False)


	def test_create(self):
                d = dbSoul.DBSoul('/tmp/unittest/test2.db')

		self.assertEqual(d.isDbOpened(), False)
                d.create()
                self.assertEqual(d.isDbOpened(), True)

                try:
                        d.create()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: create(): database already opened')
                self.assertEqual(d.isDbOpened(), True)

                try:
                        d.close()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: close(): database is closed')
                self.assertEqual(d.isDbOpened(), False)

	def test_close(self):
                d = dbSoul.DBSoul('/tmp/unittest/test3.db')
                                                                                                                             
                self.assertEqual(d.isDbOpened(), False)
                try:
                        d.close()
                except Exception, msg:
                        self.assertEqual(str(msg), 'DBSoul: close(): database is closed')
                self.assertEqual(d.isDbOpened(), False)

	def test_keys(self):
		d = dbSoul.DBSoul('/tmp/unittest/test4.db')

		try:
			d.addKey('k', 'v')
			d.setKey('k', 'v')
			d.getKey('k')
			d.delKey('k')
		except Exception, msg:
			self.assertEqual(str(msg)[-33:], 'database is closed, open it first')

		d.create()

		self.assertEqual(d.isDbOpened(), True)

		d.addKey('testkey', 'testdata')
		self.assertEqual('testdata', d.getKey('testkey'))
		d.setKey('testkey', 'datadata')
		self.assertEqual('datadata', d.getKey('testkey'))

		d.delKey('testkey')

		try:
			data = d.getKey('testkey')
		except Exception, msg:
			self.assertEqual(str(msg), 'DBSoul: getKey(): no such key "testkey"')

		d.addKey('key1', 'testdata1')
		d.addKey('key2', 'testdata2')
		d.addKey('key3', 'testdata3')

		keys = d.runKeys()

		for k in keys:
			if k[:3] == 'key': ## skip internal keys
				self.assertEqual(d.getKey(k), 'testdata' + k[-1] )
		d.close()

	def test_runkeys(self):
		d = dbSoul.DBSoul('/tmp/unittest/test5.db')
		d.create()

		dt = {}
		dt2 = {}
		dt['a'] = 'x'
		dt['b'] = 'y'
		dt['c'] = 'z'

		for k in dt:
			d.addKey(k, dt[k])

		rk = d.runKeys()

		for k in rk:
			dt2[k] = d.getKey(k)

		self.assertEqual(dt, dt2)

###########################################################


import os

def gen_bytes(len):
        x = (md5.new(str(random.random())).hexdigest())
        step = len / 32
        s = ''
        while step is not 0:
                s = s + x
                step = step - 1
        return s
                                                                                                                             
                                                                                                                             
def create_stuff(nfiles, klen, flen):
        step = 0
        klist = []
        flist = []
                                                                                                                             
        step = nfiles
        while step is not 0:
                klist.append(gen_bytes(klen))
                step = step - 1
        step = nfiles
        fl = gen_bytes(flen)
        while step is not 0:
                flist.append(fl)
                step = step - 1
        return (klist, flist)

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
	try:
		os.mkdir('/tmp/unittest/')
	except: pass
	recdelete('/tmp/unittest/')
	try:
		os.mkdir('/tmp/unittest/')
	except: pass

	unittest.main()




#EOF

#
# gestisce i file .db
#

import gdbm
import os
from configLog import log



class DBSoul(object):
	_db_singletons = {}
	def __new__(cls, *args, **kwds):
		log.debug('__new__(): %s' % args[0])
		if not cls._db_singletons.has_key(args[0]):
			cls._db_singletons[args[0]] = object.__new__(cls)
		else:
			if not cls._db_singletons[args[0]].isDbOpened():
				cls._db_singletons[args[0]] = object.__new__(cls)
			log.debug('__new__(): someone tried to open the db file "%s" 2 times!' % args[0])
		return cls._db_singletons[args[0]]

	def __init__(self, dbPath):
		try:
			self.isDbOpened()
		except:
			self._dbPath = dbPath
			self._db = None
			self._isDbOpened = False
			self._mode = ''

	def isDbOpened(self):
		return self._isDbOpened

	def isGoodState(self):
		try:
			if self._db['__econf_DB_state'] == 'GOOD'											or (self._db['__econf_DB_state'] == 'BAD' and self.isDbOpened()):
				return True
		except: pass
		return False

	def _setGoodState(self):
		if self.isDbOpened():
			self._db['__econf_DB_state'] = 'GOOD'
		else:
			log.debug('DBSoul: _setGoodState(): database is closed or opened readonly')

	def _setBadState(self):
		if self.isDbOpened():
			self._db['__econf_DB_state'] = 'BAD'
		else:
			log.debug('DBSoul: _setBadState(): database is closed or opened readonly')

	def setKey(self, key, newValue):
		if self.isDbOpened():
			if self.enable_write():
				return None
			try:
				keys = self.runKeys()
				for k in keys:
					if k == key:
						break
				if k != key:
					raise IOError, 'DBSoul: setKey(): no such key "%s"' % key 
				self._db[key] = newValue
			except TypeError:
				raise IOError, 'DBSoul: setKey(): wrong type: 1st param type: "%s", 2nd param type: "%s"'							% (type(key), type(newValue))
		else:
			raise IOError, 'DBSoul: setKey(): database is closed, open it first'
		self.disable_write()

	def getKey(self, key):
		ret = None
		if self.isDbOpened():
			try:
				ret = self._db[key]
			except KeyError:
				raise IOError, 'DBSoul: getKey(): no such key "%s"' % key
			except TypeError:
				raise IOError, 'DBSoul: getKey(): wrong type: 1st param type: "%s"' % type(key) 
		else:
			raise IOError, 'DBSoul: getKey(): database is closed, open it first'
		return ret

	def delKey(self, key):
		if self.isDbOpened():
			if self.enable_write():
				return None
			try:
				del self._db[key]
			except KeyError:
				raise IOError, 'DBSoul: delKey(): no such key "%s" or db is r/o' % key
			except TypeError:
				raise IOError, 'DBSoul: getKey(): wrong type: 1st param type: "%s"' % type(key)
		else:
			raise IOError, 'DBSoul: delKey(): database is closed, open it first'
		self.disable_write()

	def addKey(self, key, value):
		if self.isDbOpened():
			if self.enable_write():
				return None
			try:
				keys = self.runKeys()
				for k in keys:
					if k == key:
						raise IOError, 'DBSoul: addKey(): key "%s" is already present!'
				self._db[key] = value
			except TypeError:
				raise IOError, 'DBSoul: addKey(): wrong type: 1st param type: "%s", 2nd param type: "%s"'                                                    % (type(key), type(value))
		else:
			raise IOError, 'DBSoul: addKey(): database is closed, open it first'
		self.disable_write()

	def runKeys(self):
		l = [] 
		k = self._db.firstkey()
		while k != None:
			if (k[:2] != '__'):
				l.append(k)
			k = self._db.nextkey(k)
		return l

	def create(self):
		log.debug('DBSoul: create()')
		if self.isDbOpened():
			raise IOError, 'DBSoul: create(): database already opened'

		#if not self._db_singletons.has_key(self._dbPath):
		#	self._db_singletons[self._dbPath] = object.__new__(self)

		if os.access(self._dbPath, os.F_OK):
			raise IOError, 'DBSoul: create(): file "%s" exists' % self._dbPath
		else:
			try:
				self._db = gdbm.open(self._dbPath, 'n')
				self._mode = 'w'
				self._isDbOpened = True
			except:
				self._mode = ''
				self._isDbOpened = False
				raise IOError, 'DBSoul: create(): gdbm.open(): cannot create database "%s"!: %s' \
					% (self._dbPath, str(msg))
		self.disable_write()

	def enable_write(self):
		self.closeDb()
		if self.openDb('w') == None:
			raise IOError, 'DBSoul: enable_write(): problems opening db in rw mode'
		self._setBadState()

	def disable_write(self):
		self._setGoodState()
		self.closeDb()
		self.openDb('r')

	def open(self):
		log.debug('DBSoul: open()')
		# ?
		#if not self._db_singletons.has_key(self._dbPath):
		#	self._db_singletons[self._dbPath] = object.__new__(self)
		if self.openDb('r'):
			raise IOError, "DBSoul: open(): problems opening the database!"	

	def openDb(self, mode):
		if self.isDbOpened():
			if mode == self._mode:
				log.debug('DBSoul: openDb(): database already opened with given mode')
				return False
			else:
				log.debug('DBSoul: openDb(): database already opened, close it first')
				return True
		self._mode = mode

		if not os.access(self._dbPath, os.F_OK | os.R_OK | os.W_OK):
			raise IOError, 'DBSoul: openDb(): database not found'
		else:
			try:
				self._db = gdbm.open(self._dbPath, self._mode)
			except gdbm.error, msg:
				raise IOError, 'DBSoul: openDb(): gdbm.open(): database "%s" corrupted: %s' \
					% (self._dbPath, str(msg))

		if not self.isGoodState():
			log.error('DBSoul: openDb(): database in BAD state')
			return True
		self._isDbOpened = True
		if self._mode == 'w':
			self._setBadState()
		return False

	def close(self, unclean=False):
		log.debug('DBSoul: close()')

		if not self.isDbOpened():
			raise IOError, 'DBSoul: close(): database is closed'
		self.closeDb(unclean)
		#print DBSoul._db_singletons[self._dbPath]
		# TODO: il del non funge, in __new__ c'e' ancora
		#print self.__class__.__dict__
		del DBSoul._db_singletons[self._dbPath]
		#try:
		#	print DBSoul._db_singletons[self._dbPath]
		#except KeyError:
		#	global banane
		#	banane = self._dbPath 

	def closeDb(self, unclean=False):
		if self._mode == 'w':
			self._db.reorganize()
			self._db.sync()
			self._setGoodState()
			if unclean == True:
				self._setBadState()
		self._db.close()
		self._isDbOpened = False



#####################################################

import time
import sys
import md5
import random


if __name__ == '__main__':
	print '>> test2: 128 file con chiave di 4k e len di 128k'
	nr_files = 32
	key_len = 1024*4
	file_len = 1024*128

	klist = []
	flist = []
	(klist, flist) = create_stuff(nr_files, key_len, file_len)
	print '>>> generati dati.. creazione db'

	d = DBSoul('/tmp/dbtest2.db')
	d.create()
	for ke in klist:
		for fi in flist:
			d.setKey(ke, fi)
			break
	print '>>> chiudo'
	d.close()


#EOF

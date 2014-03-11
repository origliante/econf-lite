#
import dbSoul
import md5
import time
import os
from configLog import log

#############
#
# classe dell'index file presente nella directory
# di ogni snapshot, contiene:
# - MD5 dei file nella dir snapshot, se stesso compreso (?)
# - MD5 dei file di config in giro per il sistema
#
# contenuto indice:
#
# ['state'] - stato dello snapshot: 'HEALTY' o 'CORRUPTED'
# ['name'] - nome dello snapshot
# ['description'] - descrizione
# ['xsl.db'] - file xsl
# ['xml.db'] - file xml
# ['md5.db'] - md5 dei file di conf
#

class IndexContainer(dbSoul.DBSoul):
	def initIndexContainer(self):
		log.debug('IndexContainer: initIndexContainer()')

		tmp = self._dbPath.split('/')
		del tmp[-1]
		self._snap = str('/').join(tmp)

		if os.access(self._dbPath, os.F_OK):
			self.open()
		else:
			self.create()
			currDate = str(int(time.time()))
			self.addKey('name', 'DEFAULT_SNAPSHOT_NAME')
			self.addKey('description', 'Empty snapshot description.')
			#self.addKey('ctime', currDate)
			#self.addKey('mtime', currDate)
			#self.addKey('atime', currDate)
			self.addKey('date', currDate)
			self.addKey('plist.db', '')
			self.addKey('xml.db', '')
			#self.addKey('md5.db', '')
			self.updateMD5Hashes()

        def __setDate(self, newDate):
		self.setKey('date', newDate)

        def __getDate(self):
		return self.getKey('date')
	date = property(__getDate, __setDate, None, '')

	def __setName(self, newName):
		self.setKey('name', newName)

	def __getName(self):
		return self.getKey('name')
	name = property(__getName, __setName, None, '')

	def __setDescription(self, newDescription):
		self.setKey('description', newDescription)

	def __getDescription(self):
		return self.getKey('description')
	description = property(__getDescription, __setDescription, None, '')

	def updateMD5Hashes(self):
		log.debug('IndexContainer: updateMD5Hashes()')
		filesList = self._getDbFilesFromKeys()

		for dbFile in filesList:
			filePath = os.path.join(self._snap, dbFile)
			try:
				f = file(filePath, 'r')
			except Exception, msg:
				log.error('IndexContainer: updateMD5Hashes(): cannot find db file "%s", marking'								' snapshot as BAD!' % filePath)
				self.close(unclean=True)
				raise IOError, 'Cannot find db file "%s", marking myself as BAD!"' % filePath
				break
			md = md5.new(f.read()).hexdigest()
			self.setKey(dbFile, md)
			f.close()
			log.debug( 'IndexContainer: updateMD5Hashes(): %s md5 hash: %s' % (filePath, self.getKey(dbFile)) )

	def _getDbFilesFromKeys(self):
		retList = []
		keys = self.runKeys()
		for k in keys:
                        if k[-3:] == '.db':
                                retList.append(k)
		return retList

        def dbFilesCheck(self):
		log.debug('IndexContainer: dbFilesCheck()')
		filesList = []
		hash = ''
		filesList = self._getDbFilesFromKeys()

		log.debug('IndexContainer: dbFilesCheck(): filesList to check: %s' % filesList)

		for dbFile in filesList:
			filePath = os.path.join(self._snap, dbFile)
			if os.access(filePath, os.F_OK):
				try:
					orig_hash = self.getKey(dbFile)
				except IOError:
					self.close(unclean=True)
					break	
				f = file(filePath, 'r')
				hash = md5.new(f.read()).hexdigest()
				f.close()

				log.debug('IndexContainer: dbFilesCheck(): %s hash: %s' % (filePath, hash))
				if hash != self.getKey(dbFile):
					tmpkey = self.getKey(dbFile)
					self.close(unclean=True)
					raise IOError, 'IndexContainer: dbFilesCheck(): snapshot file "%s" corrupted: orig hash: "%s", curr hash: "%s"' % (filePath, tmpkey, hash)
			else:
				self.close(unclean=True)
				raise IOError, 'IndexContainer: dbFilesCheck(): snapshot file "%s" not found!' % filePath



###################################

if __name__ == '__main__':
	pass

#EOF

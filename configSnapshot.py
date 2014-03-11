#
# Apre/Crea/Manipola un config snapshot
#
#

# formato struttura snapshot info:
# tupla contenente data_creazione, nome_snapshot, descrizione, (lista files??)
#
#
import os
import time
import indexContainer
import fileContainer
import configGenerator
import md5

from utils.delete import recursive_delete
from configLog import log

# time.strftime("%d-%m-%Y_%H:%M.%S", time.localtime(int(time.time())))
#
#
class ConfigSnapshot(object):
	def __init__(self, snapshotPath):
		self._snapshotPath = snapshotPath
		self._snapshotStateIsOk = True

		# lo snapshot è già esistente
		if os.access(snapshotPath, os.F_OK):
			if not os.access(snapshotPath, os.W_OK | os.R_OK):
				# lo stato dello snapshot e' controllato da configEnvironment
				# tramite self._snapshotStateIsOk
				log.warn('ConfigSnapshot: __init__(): cannot read or write to "%s"!' % snapshotPath)
				self._snapshotStateIsOk = False
				return

			# check esistenza file db
			lt = os.listdir(snapshotPath)
			neededFiles = ['index.db', 'plist.db', 'xml.db']

			for f in lt:
				for n in neededFiles:
					if f == n:
						del neededFiles[neededFiles.index(n)]
						break
	                if len(neededFiles) > 0:
        	                self._snapshotStateIsOk = False
        	                return

		# lo snapshot è da creare
		else:
			log.debug('ConfigSnapshot: __init__(): creating a new configuration snapshot in "%s"' % snapshotPath)
			try:
				os.mkdir(snapshotPath)
			except:
				log.warn('ConfigSnapshot: __init__(): cannot read or write to %s!' % snapshotPath)
				self._snapshotStateIsOk = False
				return
		self._init_db()


	# inizializzazione dei db
	def _init_db(self):
		try:
			self._md5 = fileContainer.FileContainer(os.path.join(self._snapshotPath, 'md5.db'))
			self._md5.initFileContainer()

			self._plist = fileContainer.FileContainer(os.path.join(self._snapshotPath, 'plist.db'))
			self._plist.initFileContainer()

			self._xml = fileContainer.FileContainer(os.path.join(self._snapshotPath, 'xml.db'))
			self._xml.initFileContainer()

                        self._index = indexContainer.IndexContainer(os.path.join(self._snapshotPath, 'index.db'))
                        self._index.initIndexContainer()
                except:
                        self._snapshotStateIsOk = False
                        return
		self._cg = configGenerator.ConfigGenerator()
		self._snapshotStateIsOk = self._index.isGoodState()

	def _close_db(self):
                self._index.updateMD5Hashes()
                self._index.close()
                self._xml.close()
                self._plist.close()
		self._md5.close()

	def _syncSnapshot(self):
		log.debug('ConfigSnapshot: _syncSnapshot()')
		self._close_db()
		try:
			os.system("sync")
		except Exception, e:
			log.err('ConfigSnapshot: _syncSnapshot(): cannot exec sync, %s' % str(e))
		self._init_db()

	def checkSnapshotState(self):
		if self._snapshotStateIsOk:
			log.debug('ConfigSnapshot: checkSnapshotState(): state is OK')
		else:
			log.debug('ConfigSnapshot: checkSnapshotState(): state is BAD')
		return not self._snapshotStateIsOk

	def checkSystemConfig(self):
		log.debug('ConfigSnapshot: checkSystemConfig()')

		if self.checkSnapshotState():
			return True
		deadFiles = []
		flist = self._md5.getFileNames()

		for f in flist:
			h = ""
			origHash = ""
			try:
				h = md5.new(file(f).read()).hexdigest()
			except IOError, e:
				log.debug('ConfigSnapshot: checkSystemConfig(): problems with file [%s] (%s)' % (f, str(e)) )

			origHash = self._md5.getKey(f)
			if h != origHash:
				deadFiles.append(f)
			elif __debug__:
				log.debug('ConfigSnapshot: checkSystemConfig(): file [%s]: [%s - %s]' % (f, h, origHash))

	def getSnapshotInfo(self):
		log.debug('ConfigSnapshot: getSnapshotInfo()')

		if self.checkSnapshotState():
			return (None, None, None)
		# lclTime = time.localtime( self._index.date )
		# time.strftime("%d-%m-%Y_%H:%M.%S", lclTime)
		return (self._index.date, self._index.name, self._index.description)

	def setSnapshotInfo(self, date='', name='', description=''):
		log.debug('ConfigSnapshot: setSnapshotInfo()')

		if self.checkSnapshotState():
			return True

		if str(date) != '':
			self._index.date = str(date)
		if str(name) != '':
			self._index.name = str(name)
		if str(description) != '':
			self._index.description = str(description)

	def closeSnapshot(self):
		log.debug('ConfigSnapshot: closeSnapshot()')

		if self.checkSnapshotState():
			return True 
		self._close_db()

	# delete method 
	def die(self):
		log.debug('ConfigSnapshot: die(): good bye world')
		self.closeSnapshot()
		self._snapshotStateIsOk = False
		log.info('ConfigSnapshot: die(): deleting path "%s"' % self._snapshotPath)
		recursive_delete(self._snapshotPath)
		self._snapshotPath = ''

	def loadConfig(self, cfgPath):
		log.debug('ConfigSnapshot: loadConfig()')

		if self.checkSnapshotState():
			return True
		try:
			lt = os.listdir(cfgPath)
		except OSError:
			return True

		for f in lt:
			cfgFile = os.path.join(cfgPath, f)
			if f[-4:] == '.xml':
				if self._cg.isXMLValid(cfgFile):
					self._xml.addFile(cfgFile)
				else:
					log.warn('ConfigSnapshot: loadConfig(): invalid xml file? %' % f)
					continue

			if f[-6:] == '.plist':
				if self._cg.isPlistValid(cfgFile):
					self._plist.addFile(cfgFile)
				else:
					log.warn('ConfigSnapshot: loadConfig(): invalid plist file? %' % f)
					continue
		if self._xml.getFileNames() == []:
			log.warn('ConfigSnapshot: loadConfig(): no xml files loaded!')
			return True

		self._syncSnapshot()
		return False

	def loadHashList(self, hashList):
		log.debug('ConfigSnapshot: loadHashList()')

		if self.checkSnapshotState():
			return True

		# cleanup roba vecchia
		names = self._md5.getFileNames()
		for n in names:
			self._md5.delFile(n)

		# inserimento nuova lista
		for h in hashList:
			self._md5.addKey(h, hashList[h])

#################################

if __name__ == '__main__':
	#import time
	#cn = ConfigSnapshot('/tmp/cenv/' + time.strftime('%d-%m-%Y_%M:%S') + '/')
	#cn.setSnapshotInfo('12312312', 'mysnapname', 'a long and exaustive description.')
	#print cn.getSnapshotInfo()
	#cn.die()
	cn = ConfigSnapshot('/tmp/cenv/snapshot')
	cn.setSnapshotInfo('', 'CURRENT_SNAPSHOT', '')
	cn.loadConfig('./data/new/')
	#cn.setXMLData("""\
	#		<mappings priority="6">
		#       	        <map hostname="banana.localdomain" alias="localhost" address="127.0.0.88"/>
	#	        </mappings>
	#		""")
	cn.closeSnapshot()

#EOF

#
# Gestisce un config environment cioe'
# il tree dove sono contenuti i config snapshot
#
# ritorna i nomi degli snapshot con la data di
# creazione ecc
#
# ritorna un oggetto ConfigSnapshot relativo
# allo snapshot voluto
#
#
import os
import time
import md5
import random
from utils.copy import recursive_copy
from utils.delete import recursive_delete
from configLog import log
import configSnapshot


class ConfigEnvironment(object):
	def __init__(self, configTree):
		self.__configTree = configTree
		self.__snaps = {}
		self.__corrupted_snaps = {}

	def _addSnapshotToList(self, snapObj):
		log.debug('ConfigEnvironment: _addSnapshotToList()')

		snapName = snapObj.getSnapshotInfo()[1]
		if snapName is None:
			log.debug('ConfigEnvironment: _addSnapshotToList(): cannot add snapshot "%s"!' % snapName)
			return True 
		for n in self.__snaps:
			if n == snapName:
				log.debug('ConfigEnvironment: _addSnapshotToList(): snapName already present!')
				return True
		if type(snapName) is not type(str()):
			log.debug('ConfigEnvironment: _addSnapshotToList(): BUG: snapName "%s" isnt a string"' % snapName)
			snapName = str(snapName)
		self.__snaps[snapName] = snapObj

	def _delSnapshotFromList(self, snapName):
		log.debug('ConfigEnvironment: _delSnapshotFromList()')

		try:
			del self.__snaps[snapName]
		except KeyError:
			log.error('ConfigEnvironment: _delSnapshotFromList(): key "%s" not found' % snapName)
			return True

	def _createSnapshot(self):
		log.debug('ConfigEnvironment: _createSnapshot()')

		newSnap = None
		currDate = int(time.time())
		currDateRepr = time.strftime('%d-%m-%Y_%H:%M.%S', time.localtime( int(currDate) ))
		newPath = self._getNewSnapPath()
		if newPath is not False:
			newSnap = configSnapshot.ConfigSnapshot(newPath)
			newSnap.setSnapshotInfo(currDate, 'default_name_' + str(currDateRepr), 'empty description.')
			self._addSnapshotToList(newSnap)
			return newSnap.getSnapshotInfo()[1]
		else:
			return False

	def _openSnapshot(self, path):
		log.debug('ConfigEnvironment: _openSnapshot()')
		snap = None
		snap = configSnapshot.ConfigSnapshot(path)
		self._addSnapshotToList(snap)
		name = snap.getSnapshotInfo()[1]
		if name is None:
			log.error('ConfigEnvironment: _openSnapshot(): problems opening snapshot "%s"' % path)
			return False
		return name

	def _deleteSnapshot(self, name):
		log.debug('ConfigEnvironment: _deleteSnapshot()')
		snap = self.__snaps[name] 
		self._delSnapshotFromList(name)
		snap.die()

	def _changeSnapName(self, oldName, newName):
		log.debug('ConfigEnvironment: _changeSnapName()')
		oldName = str(oldName)
		newName = str(newName)
		for n in self.__snaps:
			if n == oldName: break
		if n == oldName:
			s = self.__snaps[oldName]
			del self.__snaps[oldName]
			s.setSnapshotInfo(name=newName)
			self.__snaps[newName] = s
		else:
			log.error('ConfigEnvironment: _changeSnapName(): snap "%s" not found!' % oldName)

	def _getNewSnapPath(self, date=''):
		log.debug('ConfigEnvironment: _getNewSnapPath()')
		if not date:
			currDate = int(time.time())
		else:   currDate = date
		currDateRepr = time.strftime( '%d-%m-%Y_%H:%M.%S', time.localtime(int(currDate)) )
		newPath = os.path.join(self.__configTree, "snapshot-" + currDateRepr)
		origPath = newPath
		step = 1
		while os.access(newPath, os.F_OK):
			log.warn('ConfigEnvironment: _getNewSnapPath(): newPath exists! "%s"' % newPath)
			addedStr = ''
			addedStr = md5.new( str(random.random()) ).hexdigest()
			newPath = origPath + '_' + addedStr
			if step > 3:
				self.logger.do('EMERG', '_getNewSnapPath') # TODO
				newPath = ''
				break
			step = step + 1
		if newPath:
			return newPath

		return False

	def _backupCurrentSnapshot(self, srcPath):
		log.debug('ConfigEnvironment: _backupCurrentSnapshot()')

		bkPath = os.path.join(self.__configTree, 'snapshot-BACKUP')
		if os.access(bkPath, os.F_OK):
			log.debug('ConfigEnvironment: _backupCurrentSnapshot(): deleting old backup')
			recursive_delete(bkPath)
		if os.access(srcPath, os.F_OK):
			log.debug('ConfigEnvironment: _backupCurrentSnapshot(): creating new backup')
			try:
				os.mkdir(bkPath)
				recursive_copy(srcPath, bkPath)
			except Exception, msg:
				log.error('ConfigEnvironment: _backupCurrentSnapshot(): unhandled exception: %s' \
							% str(msg))
				return True
			snapBackup = configSnapshot.ConfigSnapshot(bkPath)
			snapBackup.setSnapshotInfo(name = 'snapshot-BACKUP')
			snapBackup.closeSnapshot()
			if not self._openSnapshot(srcPath):
				return True
		else:
			return True

		return False

################ metodi pubblici

	def initEnvironment(self):
		log.debug('ConfigEnvironment: initEnvironment()')
		try:
			os.mkdir(self.__configTree)
		except OSError: pass
		#raise OSError, 'ConfigEnvironment: initEnvironment(): cannot create "%s"' % self.__configTree
		sName = self._createSnapshot()
		self.__snaps[sName].setSnapshotInfo(name = 'CURRENT_SNAPSHOT')
		self.closeEnvironment()
		self.openEnvironment()

	def openEnvironment(self):
		log.debug('ConfigEnvironment: openEnvironment()')
		configPath = ''
		lt = os.listdir(self.__configTree)
		bkPath = os.path.join(self.__configTree, 'snapshot-BACKUP')

		if not lt:
			log.crit('ConfigEnvironment: openEnvironment(): No snapshots found!')
			return None

		for elem in lt:
			if elem[:8] == 'snapshot' and elem[-6:] != 'BACKUP':
				configPath = os.path.join(self.__configTree, elem)
				break

		log.debug('ConfigEnvironment: openEnvironment(): loading snapshot "%s"' % configPath)
		currentSnap = configSnapshot.ConfigSnapshot(configPath)
		if not currentSnap.checkSnapshotState():
			currentSnap.closeSnapshot()
			if self._backupCurrentSnapshot(configPath):
				log.err('ConfigEnvironment: openEnvironment(): problems backupping current snapshot')
		else:
			log.err('ConfigEnvironment: openEnvironment(): configuration snapshot "%s"' 								' corrupted, restoring backup' % configPath)
			backupPath = os.path.join(self.__configTree, 'snapshot-BACKUP')
			if os.access(bkPath, os.F_OK):
				# open backup snap and set some infos
				backupSnap = configSnapshot.ConfigSnapshot(backupPath)
				if not backupSnap.checkSnapshotState():
					snapDate = backupSnap.getSnapshotInfo()[0]
					dateString = time.strftime( "%d-%m-%Y_%H:%M.%S", time.localtime(int(snapDate)) )
					snapPath = os.path.join(self.__configTree, 'snapshot-' + dateString)
					backupSnap.setSnapshotInfo(name = 'CURRENT_SNAPSHOT')
					backupSnap.closeSnapshot()

					if os.access(snapPath, os.F_OK):
						recursive_delete(snapPath)
					os.mkdir(snapPath)
					recursive_copy(backupPath, configPath)
					snap = configSnapshot.ConfigSnapshot(configPath)
					# TODO: UHM, capire se serve
					self.__snaps[snap.getSnapshotInfo()[1]] = snap
					return

			log.alert('ConfigEnvironment: openEnvironment(): the last CURRENT_SNAPSHOT' 									' BACKUP is invalid!')
		#TODO: riscarica config/reinit environment


	def listSnapshots(self):
		log.debug('ConfigEnvironment: listSnapshots()')
		lt = []
		for key in self.__snaps:
			snap = self.__snaps[key]
			if snap.checkSnapshotState():
				log.warn('ConfigEnvironment: listSnapshots(): snapshot "%s" corrupted' % snap.name)
				self._delSnapshotFromList(snap.name)
				try:
					snap.close(unclean=True)
				except: pass
			else:
				lt.append(snap.getSnapshotInfo())
		if lt:
			return lt
		return None

	def closeEnvironment(self):
		log.debug('ConfigEnvironment: closeEnvironment()')
		k = None
		for k in self.__snaps:
			self.__snaps[k].closeSnapshot()
		for k in self.__corrupted_snaps:
			self.__corrupted_snaps[k].closeSnapshot()
		# if there's only the backup snap probably it's corrupted
		# so delete it
		if k == None:
			bkPath = os.path.join(self.__configTree, 'snapshot-BACKUP')
			recursive_delete(bkPath)
		self.__snaps = {}
		self.__corrupted_snaps = {}

	def generateSystemConfig(self, cfgPath, dstRoot):
		log.debug('ConfigEnvironment: generateSystemConfig()')
		s = self.__snaps['CURRENT_SNAPSHOT']
		s.loadConfig(cfgPath)

		# TODO: sistemare qui
		try:
			s._cg.loadPlist(s._plist.getFile( s._plist.getFileNames()[0] ))
			s._cg.loadXML( s._xml.getFile( s._xml.getFileNames()[0] ) )
		except IndexError: pass

		hashList = s._cg.generateConfig(dstRoot)
		if hashList is None:
			log.error('ConfigEnvironment: generateSystemConfig(): problems loading new system config')
			self._deleteSnapshot('CURRENT_SNAPSHOT')
		else:
			s.loadHashList(hashList)

	def checkSystemConfig(self):
		log.debug('ConfigEnvironment: checkSystemConfig()')
		s = self.__snaps['CURRENT_SNAPSHOT']
		return s.checkSystemConfig()

#####################################################################à

import sys

def econf_exit(exception_msg):
	print 'ECONF:: an exception has occurred: [' + str(msg) + ']'
	print 'ECONF:: exiting'
	sys.exit(0)


if __name__ == '__main__':
	#try:
	#	ce = ConfigEnvironment('/tmp/cenv/')
	#	ce.initEnvironment()
	#except Exception, msg:
	#	econf_exit(msg)

	#ce.closeEnvironment()

	print '>'
	print '>>>>>>> fase 2'
	print '>'

	try:
		ce = ConfigEnvironment('/tmp/cenv/')
		ce.openEnvironment()
	except Exception, msg:
		econf_exit(msg)

	lista = ce.listSnapshots()
	print lista
	ce.closeEnvironment()

#EOF

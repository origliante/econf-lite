#
#
#
import dbSoul 
import os
from configLog import log

#############
#
# classe per gestire i db che contengono file
# (xml, xsl)
#
#
class FileContainer(dbSoul.DBSoul):
	def initFileContainer(self):
               	log.debug('FileContainer: initFileContainer()')

		tmp = self._dbPath.split('/')
		del tmp[-1]
		self._file = str('/').join(tmp)
		if os.access(self._dbPath, os.F_OK):
			self.open()
		else:
			self.create()

        def addFile(self, filePath):
		log.debug('FileContainer: addFile(): %s' % filePath)
                try:
                	f = open(filePath)
                except IOError:
			raise IOError, 'FileContainer(): addFile(): File "%s" not found' % filePath
		self.addKey(filePath, f.read())
		f.close()

        def delFile(self, filePath):
		log.debug('FileContainer: delFile(): %s' % filePath)
		self.delKey(filePath)

	def getFile(self, filePath):
		log.debug('FileContainer: getFile(): %s' % filePath)
		return self.getKey(filePath)

	def getFileNames(self):
		log.debug('FileContainer: getFileNames()')
		l = self.runKeys()
		return l


###################################

if __name__ == '__main__':
	pass

#EOF

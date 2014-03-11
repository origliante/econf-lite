############################################
#
# genera i file di configurazione partendo
# da un template e utilizzando xml
#
############################################
import libxml2
import libxslt
import xml.dom.minidom
from configLog import log
from utils import plist
import md5
import os

class ConfigGenerator(object):
	def __init__(self):
		self._plist = ''
		self._xml = ''

	def _computeHash(self, srcFile):
		f = file(srcFile)	
		h = md5.new(f.read()).hexdigest()
		f.close()
		return h

	def loadPlist(self, data):
		log.debug('ConfigGenerator: loadPlist()')
		try:
			self._plist = plist.parsePlist(data)
                except:
                        log.error('ConfigGenerator: loadPlist(): cannot parse/load given plist')

	def loadXML(self, data):
		log.debug('ConfigGenerator: loadXML()')
		try:
			self._xml = libxml2.parseDoc(data)
		except:
			log.error('ConfigGenerator: loadXML(): cannot parse/load given xml')

	def generateConfig(self, dstRoot):
		log.debug('ConfigGenerator: generateConfig()')

		if not os.access(dstRoot, os.R_OK|os.W_OK):
			log.err('ConfigGenerator: generateConfig(): cannot access dstRoot!')
			return None
		if self._xml == '' or self._plist == '':
			log.err('ConfigGenerator: generateConfig(): no config provided!')
			return None

		hashList = {} 
		for cfgFile in self._plist:
			dest = os.path.join(dstRoot, cfgFile[1:])
			# remove the file part from the path and
                        # creates needed dirs
                        try:
                        	os.makedirs( "/".join( dest.split('/')[:-1] ) )
                        except OSError:
                        	pass

			if self._plist[cfgFile]['type'] == 'xsl':
				# load xsl script
				styledoc = libxml2.parseDoc(self._plist[cfgFile]['data'])
				style = libxslt.parseStylesheetDoc(styledoc)

				# apply it to the xml cfg
				result = style.applyStylesheet(self._xml, None)

				# save
				style.saveResultToFilename(dest, result, 0)
                        	result.freeDoc()
                        	style.freeStylesheet()
			elif self._plist[cfgFile]['type'] == 'plain':
				file(dest, 'w+').write(self._plist[cfgFile]['data'])
			else:
				if __debug__:
					print 'ConfigGenerator::generateConfig(): unknown cfgFile type!'
			if os.access(dest, os.R_OK):
				hashList[dest] = self._computeHash(dest)
		self._xml.freeDoc()
		return hashList

	def isXMLValid(self, xmlFilePath):
		log.debug('ConfigGenerator: isXMLValid(): code me!')
		return True

	def isPlistValid(self, xslFilePath):
		log.debug('ConfigGenerator: isPlistValid(): code me!')
		return True

############################

if __name__ == '__main__':
	cg = ConfigGenerator()

	f1 = file('data/xml/config.xml')
	cg.loadXML(f1.read())
	f1.close()

	f2 = file('data/xsl/resolv.conf.xsl')
	cg.loadXSL(f2.read())
	f2.close()
	print cg.generateConfig('cfg1')
	cg.endGeneration()


#EOF

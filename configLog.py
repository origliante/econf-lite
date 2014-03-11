#################
#
# INFO, WARNING, ERROR
#
#################

# chiamerà via XML-RPC engine
# per i log locali usa il modulo di logging di python
#import logging

#TODO: integrazione con engine

class LogWrapper(object):
	_log_singletons = {}
	def __new__(inst, *args, **kwds):
		if not inst._log_singletons.has_key(inst):
			inst._log_singletons[inst] = object.__new__(inst)
		return inst._log_singletons[inst]

	def __init__(self):
		pass

	def do(self, level, msg):
		print 'REMOTE_LOGGING:: ' + msg

	def debug(self, msg):
		if __debug__:
			print 'DEBUG:: ' + str(msg)
		else:
			pass # scrivi su disco

	def info(self, msg):
		print 'INFO:: ' + str(msg)

	def error(self, msg):
		print 'ERROR:: ' + str(msg)
	
	def err(self, msg):
		self.error(msg)

	def alert(self, msg):
		print 'ALERT:: ' + str(msg)

	def warn(self, msg):
		print 'WARN:: ' + str(msg) 

	def crit(self, msg):
		print 'CRIT:: ' + str(msg)


log = LogWrapper()

#EOF

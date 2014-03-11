#
#
#
import configEnvironment
from optparse import OptionParser
import os
import sys


def main():
	parser = OptionParser()
	parser.add_option("-s", "--config-src", dest="configSrc", help="read config from PATH", metavar="PATH")
	parser.add_option("-d", "--config-dst", dest="configDst", help="write config to PATH (example: '/')", metavar="PATH")
	parser.add_option("-e", "--config-env", dest="configEnv", help="config environment PATH", metavar="PATH")
	(opts, args) = parser.parse_args()	

	if opts.configEnv is None:
		opts.configEnv = '/data/econf-env'

	if not os.access(opts.configEnv, os.F_OK):
		print 'ERROR:: main(): cannot find config environment path "%s". exiting.' % opts.configEnv
		sys.exit(0)

	ce = configEnvironment.ConfigEnvironment(opts.configEnv)

	if opts.configSrc is not None and opts.configDst is not None:
		ce.initEnvironment()
		ce.generateSystemConfig(opts.configSrc, opts.configDst)
	else:
		print parser.error('i need --config-src and --config-dst')
	ce.closeEnvironment()




if __name__ == '__main__':
	main()


#EOF

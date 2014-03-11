import stat
import os
import warnings

def recursive_delete(path):
	s = os.lstat(path)

	if not stat.S_ISDIR(s.st_mode):
		raise IOError, 'recursive_delete(): %s is not a directory' % path
                                                                                                                             
	lt = os.listdir(path)
	for elem in lt:
		fpath = os.path.join(path, elem)
		s = os.lstat(fpath)
		if stat.S_ISDIR(s.st_mode):
			recursive_delete(fpath)
		else:
			os.unlink(fpath)
	os.rmdir(path)


#EOF

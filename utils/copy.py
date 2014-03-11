import stat
import os
import warnings

def recursive_copy(srcPath, dstPath):
	s = os.lstat(srcPath)
        if not stat.S_ISDIR(s.st_mode):
                raise IOError, 'recursive_copy(): %s is not a directory' % srcPath

	if not os.access(dstPath, os.F_OK):
		os.mkdir(dstPath)
	else:
		s = os.lstat(dstPath)
		if not stat.S_ISDIR(s.st_mode):
			raise IOError, 'recursive_copy(): %s is not a directory' % dstPath

	lt = os.listdir(srcPath)
	for elem in lt:
		sPath = os.path.join(srcPath, elem)
		dPath = os.path.join(dstPath, elem)
		s = os.lstat(sPath)
		if stat.S_ISDIR(s.st_mode):
			os.mkdir(dPath)
			recursive_copy(sPath, dPath)
		else:
			f1 = file(sPath)
			f2 = file(dPath, 'w+')
			f2.write(f1.read())
			f1.close()
			f2.close()



if __name__ == '__main__':
	os.mkdir('/tmp/copy-test/')
	os.mkdir('/tmp/copy-test/dir1')
	os.mkdir('/tmp/copy-test/dir2')
	os.mkdir('/tmp/copy-test/dir1/dir1')
	f1 = file('/tmp/copy-test/file1', 'w+')
	f1.write('XYZ')	
	f1.close()
        f1 = file('/tmp/copy-test/dir1/file1', 'w+')
        f1.write('XYZ')
        f1.close()
        f1 = file('/tmp/copy-test/dir1/file2', 'w+')
        f1.write('XYZ')
        f1.close()
        f1 = file('/tmp/copy-test/dir2/file1', 'w+')
        f1.write('XYZ')
        f1.close()
        f1 = file('/tmp/copy-test/dir1/dir1/file1', 'w+')
        f1.write('XYZ')
        f1.close()
        f1 = file('/tmp/copy-test/dir1/dir1/file2', 'w+')
        f1.write('XYZ')
        f1.close()
	os.mkdir('/tmp/copy-test2/')
	recursive_copy('/tmp/copy-test', '/tmp/copy-test2')


#EOF

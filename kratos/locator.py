import os
import sys
#
# Module used by the kratoslib.get_kratos_home function
# to find the path of the executable
#

# Check if we are built-in to an exe with the interpreter
def are_builtin():
	return hasattr(sys, 'frozen')

def get_path():
	encoding = sys.getfilesystemencoding()
	if are_builtin():
		return os.path.dirname(unicode(sys.executable, encoding))
	return os.path.dirname(unicode(__file__, encoding))

import time, atexit
from rich import print
from inspect import currentframe, getframeinfo
from os import getcwd
from os.path import relpath, basename, dirname, join as pathjoin

DEBUG_COLOR		= "green"
INFO_COLOR		= "cyan"
WARNING_COLOR	= "yellow"
ERROR_COLOR		= "red"
ANALYZE_COLOR	= "dark_orange3"
HEAD_BACK_COLOR = "black"

STYLE_CLEAR			= "[/]"
STYLE_DEBUG_HEAD	= "[" + DEBUG_COLOR + " on " + HEAD_BACK_COLOR + "]"
STYLE_DEBUG_BODY	= STYLE_CLEAR + "[" + DEBUG_COLOR + "]"
STYLE_INFO_HEAD		= "[" + INFO_COLOR + " on " + HEAD_BACK_COLOR + "]"
STYLE_INFO_BODY		= STYLE_CLEAR + "[" + INFO_COLOR + "]"
STYLE_WARNING_HEAD	= "[" + WARNING_COLOR + " on " + HEAD_BACK_COLOR + "]"
STYLE_WARNING_BODY	= STYLE_CLEAR + "[" + WARNING_COLOR + "]"
STYLE_ERROR_HEAD	= "[" + ERROR_COLOR + " on " + HEAD_BACK_COLOR + "]"
STYLE_ERROR_BODY	= STYLE_CLEAR + "[" + ERROR_COLOR + "]"
STYLE_ANALYZE	= "[" + ANALYZE_COLOR + " on " + HEAD_BACK_COLOR + "]"

DEFAULT_VERBOSE	 = True
verbose = DEFAULT_VERBOSE

SUPPRESS_ALL_DEBUG = False
SUPPRESS_ALL_INFO = False
SUPPRESS_ALL_WARNING = False
SUPPRESS_ALL_ERROR = False
SUPPRESS_ALL_OUTPUT = False
DEBUG_BLACKLIST = [
		'gas_application_extreme_detail',
		'bb subscriber removal',
		'pipeline_tx',
		'pipeline_rx'
	]

#PROGRESS_BARS = ProgressManager()
#PROGRESS_BARS.start()
#atexit.register(PROGRESS_BARS.stop)

#lock_output = Lock()

def debug(s, key = None, forceprint = False, **kwargs):
	# abort if all debug suppressed
	if (SUPPRESS_ALL_OUTPUT or SUPPRESS_ALL_DEBUG):
		return
	
	# abort if key is blacklisted
	if key in DEBUG_BLACKLIST and not forceprint:
		return
	
	if verbose:
		to_stdout(STYLE_DEBUG_HEAD + "DEBUG in " + caller_str() + ":" + STYLE_DEBUG_BODY + " " + rich_escape(s), **kwargs)
	else:
		to_stdout(STYLE_DEBUG_HEAD + "DEBUG:" + STYLE_DEBUG_BODY + " " + rich_escape(s), **kwargs)

def info(s, **kwargs):
	if SUPPRESS_ALL_OUTPUT or SUPPRESS_ALL_INFO:
		return

	if verbose:
		to_stdout(STYLE_INFO_HEAD + "INFO in " + caller_str() + ":" + STYLE_INFO_BODY + " "  + rich_escape(s), **kwargs)
	else:
		to_stdout(STYLE_INFO_HEAD + "INFO:" + STYLE_INFO_BODY + " " + rich_escape(s), **kwargs)

def warning(s, **kwargs):
	if SUPPRESS_ALL_OUTPUT or SUPPRESS_ALL_WARNING:
		return
	
	if verbose:
		to_stdout(STYLE_WARNING_HEAD + "WARNING in " + caller_str() + ":" +  STYLE_WARNING_BODY + " "  + rich_escape(s), **kwargs)
	else:
		to_stdout(STYLE_WARNING_HEAD + "WARNING:" + STYLE_WARNING_BODY + " " + rich_escape(s), **kwargs)

def error(s, **kwargs):
	if SUPPRESS_ALL_OUTPUT or SUPPRESS_ALL_ERROR:
		return
	
	if verbose:
		to_stdout(STYLE_ERROR_HEAD + "ERROR in " + caller_str() + ":" +  STYLE_ERROR_BODY + " " + rich_escape(s), **kwargs)
	else:
		to_stdout(STYLE_ERROR_HEAD + "ERROR:" + STYLE_ERROR_BODY + " " + rich_escape(s), **kwargs)

def analyze(var_name, **kwargs):
	if SUPPRESS_ALL_OUTPUT or SUPPRESS_ALL_DEBUG:
		return

	frame = currentframe()
	if frame.f_back is None:
		raise "Cannot analyze variable without a previous frame."
	
	path = var_name.split(".")
	value = frame.f_back.f_locals[path[0]]
	for v in path[1:]:
		value = value.__dict__[v]
	
	val_string = var_name + " = " + str(value) + " (" + str(type(value).__name__) + ")"
	
	
	if verbose:
		to_stdout(STYLE_ANALYZE + "ANALYZE FROM " + caller_str() + ": " + rich_escape(val_string), **kwargs)
	else:
		to_stdout(STYLE_ANALYZE + "ANALYZE: " + rich_escape(val_string))
	
def printraw(s, **kwargs):
	#lock_output.acquire()
	to_stdout(s, **kwargs)
	#lock_output.release()
	
def to_stdout(str, **kwargs):
	#lock_output.acquire()
	print(str, **kwargs)
	#lock_output.release()
		
# get the most recent frame in the current traceback that originates outside of this module
# if no such frame exists (ie: traceback exists fully in within this file), returns the topmost frame
def most_recent_external_frame():
	frame = currentframe()
	while frame.f_back is not None and getframeinfo(frame).filename == __file__:
		frame = frame.f_back
	return frame

def caller_info():
	caller = getframeinfo(most_recent_external_frame())
	f_path = caller.filename
	rel_path = pathjoin(relpath(dirname(f_path), getcwd()), basename(f_path))
	l_no = caller.lineno
	return (rel_path, l_no)

# get the file name and line number from the code that called the print function
def caller_str():
	# get the caller info and put it in a string
	caller = caller_info()
	return caller[0] + "@" + str(caller[1])

def rich_escape(s):
	return str(s).replace("[", "\[")

def blacklist_key(key):
	DEBUG_BLACKLIST += [key]
	
def whitelist_key(key):
	DEBUG_BLACKLIST -= [key]
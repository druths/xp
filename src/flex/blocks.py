import subprocess
import tempfile
import os, os.path
import logging

logger = logging.getLogger(os.path.basename(__file__))

def get_total_context(context):
	total_context = dict(os.environ)
	for k,v in context.items():
		total_context[k] = v

	return total_context

def run_shell(context,cwd,content):
	"""
	Raises a CalledProcessError if this fails.
	"""
	subprocess.call('\n'.join(content),shell=True,cwd=cwd,env=get_total_context(context))

def run_python(context,cwd,content):

	# write python code to a tmp file
	fh,pyfilename = tempfile.mkstemp(suffix='py')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote python content to %s' % pyfilename)
	
	cmd = 'python %s' % pyfilename
	subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))

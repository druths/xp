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
	retcode = subprocess.call('\n'.join(content),shell=True,cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode

def run_python(context,cwd,content):

	# write python code to a tmp file
	fh,tmp_filename = tempfile.mkstemp(suffix='py')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote python content to %s' % tmp_filename)
	
	exec_name = context.get('PYTHON','python')
	cmd = '%s %s' % (exec_name,tmp_filename)
	logger.debug('using cmd: %s' % cmd)
	retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode

def run_gnuplot(context,cwd,content):
	
	# write gnuplot code to a tmp file
	fh,tmp_filename = tempfile.mkstemp(suffix='gp')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote gnuplot content to %s' % tmp_filename)
	
	exec_name = context.get('GNUPLOT','gnuplot')
	cmd = '%s %s' % (exec_name,tmp_filename)
	logger.debug('using cmd: %s' % cmd)
	retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode



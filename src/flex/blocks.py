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

def run_shell(arg_str,context,cwd,content):
	"""
	Raises a CalledProcessError if this fails.
	"""

	if len(arg_str.strip()) > 0:
		logger.warn('shell block ignoring argument string: %s' % arg_str)

	retcode = subprocess.call('\n'.join(content),shell=True,
							  cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode

def run_python(arg_str,context,cwd,content):

	# write python code to a tmp file
	fh,tmp_filename = tempfile.mkstemp(suffix='py')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote python content to %s' % tmp_filename)
	
	exec_name = context.get('PYTHON','python')
	cmd = '%s %s %s' % (exec_name,arg_str,tmp_filename)
	logger.debug('using cmd: %s' % cmd)
	retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode

def run_gnuplot(arg_str,context,cwd,content):
	
	# write gnuplot code to a tmp file
	fh,tmp_filename = tempfile.mkstemp(suffix='gp')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote gnuplot content to %s' % tmp_filename)
	
	exec_name = context.get('GNUPLOT','gnuplot')
	cmd = '%s %s %s' % (exec_name,arg_str,tmp_filename)
	logger.debug('using cmd: %s' % cmd)
	retcode = subprocess.call(cmd,shell=True,
				cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError, 'return code: %d' % retcode

def run_test(arg_str,context,cwd,content):
	
	# create all fils in the arg str
	for fname in arg_str.split():
		fh = open(fname,'w')
		fh.close()

	# echo the content
	print '\n'.join(content)

	# done
	return

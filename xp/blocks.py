"""
Copyright 2016 Derek Ruths

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
from subprocess import CalledProcessError
import tempfile
import os, os.path
import inspect
import logging

logger = logging.getLogger(os.path.basename(__file__))

########
# Code block base class
########
registered_code_blocks = {}
class CodeBlockImpl:

	def __init__(self,block_prefix,short_help,long_help,env_vars,run_fxn):
		global registered_code_blocks

		self._block_prefix = block_prefix
		self._short_help = short_help
		self._long_help = long_help
		self._env_vars = env_vars

		self._run_fxn = run_fxn

		# register the code block
		if self._block_prefix in registered_code_blocks:
			raise Exception, 'attempt to register two code blocks for the same prefix: %s' % self._block_prefix

		registered_code_blocks[self._block_prefix] = self	

	@property
	def block_prefix(self):
		return self._block_prefix

	@property
	def short_help(self):
		return self._short_help

	@property
	def long_help(self):
		return self._long_help

	@property
	def env_vars(self):
		return self._env_vars

	def run(self,arg_str,context,cwd,content):
		self._run_fxn(arg_str,context,cwd,content)	

########
# Decorator
########
#################################
# decorator
#################################
def codeblock(fxn=None,**kwargs):
	"""
	This decorator is used to register functions that implement
	a particular code block type.
	"""
	if inspect.isfunction(fxn):
		return codeblock_fxn(fxn,kwargs)
	else:
		def inner_codeblock(fxn):
			return codeblock_fxn(fxn,kwargs)

		return inner_codeblock

def codeblock_fxn(cb_fxn,kwargs):

	block_prefix = kwargs.pop('block_prefix')
	short_help = kwargs.pop('short_help')
	long_help = kwargs.pop('long_help')
	env_vars = kwargs.pop('env_vars',dict())

	clazz = CodeBlockImpl(block_prefix,short_help,long_help,env_vars,cb_fxn)

   	return cb_fxn


########
# Helper function
########
def get_total_context(context):
	"""
	Return the total environmental context, including the
	local context and all environment variables from the
	OS-level.
	"""
	total_context = dict(os.environ)
	for k,v in context.items():
		total_context[k] = v

	return total_context

########
# Some standard codeblocks
########

### OS-specific shell
@codeblock(	block_prefix='sh',
			short_help='run a shell script (OS-specific)',
			long_help='Run the commands in whatever the default shell on the host operating system.')
def run_shell(arg_str,context,cwd,content):
	"""
	Raises a CalledProcessError if this fails.
	"""

	if len(arg_str.strip()) > 0:
		logger.warn('shell block ignoring argument string: %s' % arg_str)

	cmd = '\n'.join(content)
	retcode = subprocess.call(cmd,shell=True,
							  cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError(retcode,cmd,None)

### Python
@codeblock(	block_prefix='py',
			short_help='run python code',
			long_help='Run the commands in whatever the default python VM is on the host system.')
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
		raise CalledProcessError(retcode,cmd,None)

### Gnuplot
@codeblock(	block_prefix='gnuplot',
			short_help='run a gnuplot script',
			long_help='Run the commands in GNUPlot.')
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
		raise CalledProcessError(retcode,cmd,None)

### awk
# TODO: Add info to how to use the BEGIN section
@codeblock(	block_prefix='awk',
			short_help='run an AWK script',
			long_help='Run an awk script. Note that in order to read/write particular files, use the BEGIN preamble.')
def run_awk(arg_str,context,cwd,content):
	
	# write awk code to a tmp file
	fh,tmp_filename = tempfile.mkstemp(suffix='awk')
	os.write(fh,'\n'.join(content))
	os.close(fh)

	logger.debug('wrote awk content to %s' % tmp_filename)
	
	exec_name = context.get('AWK','awk')
	cmd = '%s -f %s %s' % (exec_name,tmp_filename,arg_str)
	logger.debug('using cmd: %s' % cmd)
	retcode = subprocess.call(cmd,shell=True,
				cwd=cwd,env=get_total_context(context))

	if retcode != 0:
		raise CalledProcessError(retcode,cmd,None)

### A codeblock for basic testing
@codeblock(	block_prefix='test',
			short_help='a codeblock for internal testing',
			long_help='This code block will write the content to the file named in the argument string.')
def run_test(arg_str,context,cwd,content):
	
	# create all fils in the arg str
	for fname in arg_str.split():
		fh = open(fname,'w')
		fh.close()

	# echo the content
	print '\n'.join(content)

	# done
	return

### Hadoop map-reduce
@codeblock( block_prefix='pyhmr',
			short_help='Hadoop map-reduce in python',
			long_help="""This code block type encapsulates a Hadoop map-reduce task implemented in
Python. The map-reduce capability is mediated through the Hadoop streaming API.
This code block should contain two functions: map(stream) and reduce(stream).

For map(stream), stream is an iterable over string lines, no format assumed.
The output should be printed to stdout with the format, string key-value pairs
with some character separator (tab separators are typical).

For reduce(stream), stream is an iterable over the output of one or more
map(stream) functions. The output of the reduce should also be string key-value
pairs.

Note that in order for this block to run, three environment variables MUST be
set: PYHMR_INPUT, PYHMR_OUTPUT, and PYHMR_STREAMING_API_JAR.""",
			env_vars={	'PYHMR_HADOOP_CMD':'the Hadoop executable that should be invoked. Default is "hadoop"',
						'PYHMR_PYTHON_CMD':'the Python executable that should be invoked on the DataNodes. Default is "python"',
						'PYHMR_INPUT':'the input files in the HDFS (required)',
						'PYHMR_OUTPUT':'the output location on the HDFS (required)',
						'PYHMR_STREAMING_API_JAR':'the absolute path to the streaming API jar included with the Hadoop installation (required)',
						'PYHMR_EXTRA_FILES':'any extra files that should be bundled with the task on the DataNodes',
						'PYHMR_NUM_REDUCERS':'the number of reducers that should be used in performing this task',
						'PYHMR_TEST_CMD':'a command that can be used to test this map-reduce task. If this is set, then the task will be run in test mode (Hadoop will not be run, the HDFS will not be accessed).  The output of this command will be used as input to the mapper (which will then be used as input to the reducer).  The output will be printed to STDOUT.',
						'PYHMR_TEST_OUTPUT':'the file that the result of the test will be written to.  If not specified, STDOUT will be used.'})
def run_python_hadoop_mapreduce(arg_str,context,cwd,content):
	
	# get configuration
	HADOOP_CMD_EV = 'PYHMR_HADOOP_CMD'
	PYTHON_CMD_EV = 'PYHMR_PYTHON_CMD'
	STREAMING_API_JAR_EV = 'PYHMR_STREAMING_API_JAR'
	INPUT_EV = 'PYHMR_INPUT'
	OUTPUT_EV = 'PYHMR_OUTPUT'
	EXTRA_FILES_EV = 'PYHMR_EXTRA_FILES'
	NUM_REDUCERS_EV = 'PYHMR_NUM_REDUCERS'
	TEST_CMD_EV = 'PYHMR_TEST_CMD'
	TEST_OUTPUT_EV = 'PYHMR_TEST_OUTPUT'

	hadoop_cmd = context.get(HADOOP_CMD_EV,'hadoop')
	python_cmd = context.get(PYTHON_CMD_EV,'python')

	streaming_api_jar = context.get(STREAMING_API_JAR_EV)
	input_location = context.get(INPUT_EV)
	output_location = context.get(OUTPUT_EV)

	extra_files = context.get(EXTRA_FILES_EV,'')
	num_reducers = context.get(NUM_REDUCERS_EV,None)

	test_cmd = context.get(TEST_CMD_EV,None)
	test_output = context.get(TEST_OUTPUT_EV,None)
	is_test = test_cmd is not None

	# make the mapper file
	fh,mapper_filename = tempfile.mkstemp(suffix='py')
	os.write(fh,'\n'.join(content))
	os.write(fh,"""

if __name__ == '__main__':
	import sys
	map(sys.stdin)
""")
	os.close(fh)

	logger.debug('wrote mapper to %s' % mapper_filename)

	# make the reducer file
	fh,reducer_filename = tempfile.mkstemp(suffix='py')
	os.write(fh,'\n'.join(content))
	os.write(fh,"""

if __name__ == '__main__':
	import sys
	reduce(sys.stdin)
""")
	os.close(fh)

	logger.debug('wrote reducer to %s' % reducer_filename)

	# switch behavior conditional on testing
	if is_test:
		logger.warn('running map-reduce task in test mode')

		cmd = '%s | %s %s | %s %s' % (test_cmd,python_cmd,mapper_filename,python_cmd,reducer_filename)

		if test_output is not None:
			cmd += ' > %s' % test_output

		logger.debug('using cmd: %s' % cmd)
		retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))
	
		if retcode != 0:
			raise CalledProcessError(retcode,cmd,None)
	else:
		logger.info('running map-reduce task in normal mode')

		cmd = '%s jar %s' % (hadoop_cmd,streaming_api_jar)
		cmd += ' -input "%s" -output "%s"' % (input_location,output_location)
		cmd += ' -mapper "%s %s" -reducer "%s %s"' % (python_cmd,mapper_filename,python_cmd,reducer_filename)
		cmd += ' -files "%s"' % ','.join([mapper_filename,reducer_filename,extra_files])
		if num_reducers is not None:
			cmd += ' -D mapred.reduce.tasks=%s' % num_reducers

		logger.debug('using cmd: %s' % cmd)
		retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))
	
		if retcode != 0:
			raise CalledProcessError(retcode,cmd,None)
	

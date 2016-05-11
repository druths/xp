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

	def __init__(self,block_prefix,short_help,long_help,run_fxn):
		global registered_code_blocks

		self._block_prefix = block_prefix
		self._short_help = short_help
		self._long_help = long_help

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

	clazz = CodeBlockImpl(block_prefix,short_help,long_help,cb_fxn)

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

@codeblock(	block_prefix='sh',
			short_help='run a shell script (OS-specific)',
			long_help='run the commands in whatever the default shell on the host operating system')
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

@codeblock(	block_prefix='py',
			short_help='run python code',
			long_help='run the commands in whatever the default python VM is on the host system')
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

@codeblock(	block_prefix='gnuplot',
			short_help='run a gnuplot script',
			long_help='run the commands in GNUPlot')
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

@codeblock(	block_prefix='awk',
			short_help='run an AWK script',
			long_help='run an awk script. Note that in order to read/write particular files, use the BEGIN preamble.')
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

@codeblock(	block_prefix='test',
			short_help='a codeblock for internal testing',
			long_help='this codeblock will write the content to the file named in the argument string')
def run_test(arg_str,context,cwd,content):
	
	# create all fils in the arg str
	for fname in arg_str.split():
		fh = open(fname,'w')
		fh.close()

	# echo the content
	print '\n'.join(content)

	# done
	return


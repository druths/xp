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

import os.path
import logging

from xp.kernels.base import Kernel, get_total_context

logger = logging.getLogger(os.path.basename(__file__))

class TestKernel:

	@property
	def short_help(self):
		"""
		Return a short description of the kernel.
		"""
		return 'a codeblock for internal testing'

	@property
	def long_help(self):
		"""
		Return a detailed description of the kernel, how it works, how it is configured, and used.
		"""
		return 'This code block will write the content to the file named in the argument string.'

	@property
	def env_vars_help(self):
		"""
		Return a dictionary of environment variables (keys) and their meaning (values).
		"""
		return {}

	def run(self,arg_str,context,cwd,content):
		"""
		Raises a CalledProcessError if this fails.
		"""
		# create all fils in the arg str
		for fname in arg_str.split():
			fh = open(fname,'w')
			fh.close()
	
		# echo the content
		print '\n'.join(content)
	
		# done
		return
	


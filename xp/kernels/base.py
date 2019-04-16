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

import os

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

#######
# The Kernel base class
#######
class Kernel:

	@staticmethod
	def default_lang_suffix():
		"""
		Return the language suffix the kernel is linked to.
		"""
		raise NotImplemented('lang_suffix not implemented')

	@staticmethod
	def short_help():
		"""
		Return a short description of the kernel.
		"""
		raise NotImplemented('short_help not implemented')

	@staticmethod
	def long_help():
		"""
		Return a detailed description of the kernel, how it works, how it is configured, and used.
		"""
		raise NotImplemented('long_help not implemented')

	@staticmethod
	def env_vars_help():
		"""
		Return a dictionary of environment variables (keys) and their meaning (values).
		"""
		raise NotImplemented('env_vars_help not implemented')

	def run(self,arg_str,context,cwd,content):
		"""
		Run the block.

		Params
		------

		  - arg_str is the argument string on the block definition line
		  - context is the set of environment variables the block is aware of
		  - cwd is the current working directory
		  - content is the actual raw text content of the block
		"""
		raise NotImplemented('run not implemented')

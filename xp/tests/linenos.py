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

import unittest
from xp.pipeline import *
import xp.pipeline as pipeline
import os, os.path
import shutil
import time

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class LinenosTestCase(unittest.TestCase):

	def test_preamble_linenos(self):
		ep = get_pipeline(get_complete_filename('ddir_prefix'),
							default_prefix=USE_FILE_PREFIX)

		var_assign = ep.get_stmt_from_lineno(3)
		no_stmt = ep.get_stmt_from_lineno(4)

		task = ep.get_stmt_from_lineno(6)
		
		self.assertTrue(isinstance(var_assign,VariableAssignment))
		self.assertEquals(no_stmt,None)
		self.assertEquals(task.name,'task1')


import unittest
from flex.pipeline import get_pipeline, expand_variables, PIPELINE_PREFIX_VARNAME, ParseException
import flex.pipeline as pipeline
import os, os.path
import shutil

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class PrefixTestCase(unittest.TestCase):
	
	def test_default_file_prefix(self):
		p = get_pipeline(get_complete_filename('dfile_prefix'))
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename('dfile_prefix_hello_world.txt')))

		os.remove(get_complete_filename('dfile_prefix_hello_world.txt'))

		p.unmark_all_tasks(recur=True)

	def test_spec_file_prefix(self):
		p = get_pipeline(get_complete_filename('sfile_prefix'))
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename('sfp_hello_world.txt')))

		os.remove(get_complete_filename('sfp_hello_world.txt'))

		p.unmark_all_tasks(recur=True)

	def test_default_dir_prefix(self):
		p = get_pipeline(get_complete_filename('ddir_prefix'))
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename(os.path.join('ddir_prefix_data','hello_world.txt'))))

		shutil.rmtree(get_complete_filename('ddir_prefix_data'))

		p.unmark_all_tasks(recur=True)

	def test_spec_dir_prefix(self):
		p = get_pipeline(get_complete_filename('sdir_prefix'))
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename(os.path.join('sdir_foo','bar','hello_world.txt'))))

		shutil.rmtree(get_complete_filename('sdir_foo'))

		p.unmark_all_tasks(recur=True)



import unittest
from flex.pipeline import *
import flex.pipeline as pipeline
import os, os.path
import time

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class DependencyTestCase(unittest.TestCase):

	def test_unmarked_dep_execution(self):

		p = get_pipeline(get_complete_filename('ext_dep_test'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		t1_file = get_complete_filename('ext_dep_test_t1.txt')
		t1 = p.get_task('task1')
		t2_file = get_complete_filename('ext_dep_test_t2.txt')
		t2 = p.get_task('task2')
		t3_file = get_complete_filename('ext_dep_test_t3.txt')
		t3 = p.get_task('task3')
			
		# clear out the products of this pipeline
		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		# mark tasks
		t1.mark()
		t3.mark()

		# make sure that the timestamps are different
		time.sleep(1)

		# run task 3
		t3.run() #force=FORCE_NONE)

		# check the output
		self.assertFalse(os.path.exists(t1_file))
		self.assertTrue(os.path.exists(t2_file))
		self.assertTrue(os.path.exists(t3_file))

		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		p.unmark_all_tasks(recur=True)


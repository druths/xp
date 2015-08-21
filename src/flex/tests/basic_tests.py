import unittest
from flex.pipeline import *
import flex.pipeline as pipeline
import os, os.path

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class BasicTestCase(unittest.TestCase):

	def test_parse_empty_file(self):

		ep = get_pipeline(get_complete_filename('empty'),default_prefix=USE_FILE_PREFIX)

		self.assertEquals(len(ep.preamble),0)
		self.assertEquals(len(ep.tasks),0)
	
	def test_simple_preamble(self):
		p = get_pipeline(get_complete_filename('preamble1'),default_prefix=USE_FILE_PREFIX)

		self.assertEquals(len(p.preamble),3)
		self.assertTrue(isinstance(p.preamble[0],pipeline.VariableAssignment))
		self.assertTrue(isinstance(p.preamble[1],pipeline.DeleteVariable))
		self.assertTrue(isinstance(p.preamble[2],pipeline.VariableAssignment))
		self.assertEquals(len(p.tasks),0)

	def test_simple_tasks(self):
		p = get_pipeline(get_complete_filename('tasks1'),default_prefix=USE_FILE_PREFIX)

		self.assertEquals(len(p.preamble),3)
		self.assertEquals(len(p.tasks),1)

		task0 = p.tasks[0]
		self.assertEquals(len(task0.blocks),3)
		self.assertTrue(isinstance(task0.blocks[0],pipeline.ExportBlock))

		self.assertTrue(isinstance(task0.blocks[1],pipeline.CodeBlock))
		self.assertEquals(task0.blocks[1].lang,'sh')
		self.assertEquals(task0.blocks[1].content,['echo $X'])

		self.assertTrue(isinstance(task0.blocks[2],pipeline.CodeBlock))
		self.assertEquals(task0.blocks[2].lang,'py')

	def test_simple_tasks2(self):
		p = get_pipeline(get_complete_filename('tasks2'),default_prefix=USE_FILE_PREFIX)

		self.assertEquals(len(p.preamble),3)
		self.assertEquals(len(p.tasks),2)

		task1 = p.tasks[1]
		self.assertEquals(len(task1.blocks),3)
		self.assertTrue(isinstance(task1.blocks[0],pipeline.ExportBlock))

		self.assertTrue(isinstance(task1.blocks[1],pipeline.CodeBlock))
		self.assertEquals(task1.blocks[1].lang,'sh')
		self.assertEquals(task1.blocks[1].content,['echo $X','touch task2_foobar.sh'])

		self.assertTrue(isinstance(task1.blocks[2],pipeline.CodeBlock))
		self.assertEquals(task1.blocks[2].lang,'py')

	def test_extend(self):
		p = get_pipeline(get_complete_filename('extend1'),default_prefix=USE_FILE_PREFIX)

		self.assertEquals(len(p.preamble),5)

	def test_nop_unmark(self):
		p = get_pipeline(get_complete_filename('tasks2'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks()

	def test_run_tasks2(self):
		p = get_pipeline(get_complete_filename('tasks2'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the marking
		self.assertTrue(os.path.exists(get_complete_filename('.tasks2-task1.mark')))
		self.assertTrue(os.path.exists(get_complete_filename('.tasks2-task2.mark')))

		# check the results
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.sh')))
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.py')))

		os.remove(get_complete_filename('task2_foobar.sh'))
		os.remove(get_complete_filename('task2_foobar.py'))

		p.unmark_all_tasks(recur=True)

	def test_task_comment(self):
		p = get_pipeline(get_complete_filename('task_comm1'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)

		p.run()

		p.unmark_all_tasks(recur=True)
	
	def test_block_comment(self):
		p = get_pipeline(get_complete_filename('comm1'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)

		p.run()

		p.unmark_all_tasks(recur=True)

	def test_run_extend1(self):
		p = get_pipeline(get_complete_filename('extend1'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the marking
		self.assertTrue(os.path.exists(get_complete_filename('.extend1-task1.mark')))
		self.assertTrue(os.path.exists(get_complete_filename('.extend1-task2.mark')))
		self.assertTrue(os.path.exists(get_complete_filename('.extend1-extra1.mark')))

		# check the results
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.sh')))
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.py')))
		self.assertTrue(os.path.exists(get_complete_filename('extend1_2.txt')))

		os.remove(get_complete_filename('task2_foobar.sh'))
		os.remove(get_complete_filename('task2_foobar.py'))
		os.remove(get_complete_filename('extend1_2.txt'))

		p.unmark_all_tasks(recur=True)
	
	def test_run_use1(self):
		p = get_pipeline(get_complete_filename('use1'),default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.sh')))
		self.assertTrue(os.path.exists(get_complete_filename('task2_foobar.py')))
		self.assertTrue(os.path.exists(get_complete_filename('extend1_2.txt')))
		self.assertTrue(os.path.exists(get_complete_filename('use1_3.txt')))

		os.remove(get_complete_filename('task2_foobar.sh'))
		os.remove(get_complete_filename('task2_foobar.py'))
		os.remove(get_complete_filename('extend1_2.txt'))
		os.remove(get_complete_filename('use1_3.txt'))	

		p.unmark_all_tasks(recur=True)

class ForceTestCase(unittest.TestCase):

	def test_no_passthrough(self):
		p = get_pipeline(get_complete_filename('force_test'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		t1_file = get_complete_filename('force_test_t1.txt')
		t1 = p.get_task('task1')
		t2_file = get_complete_filename('force_test_t2.txt')
		t2 = p.get_task('task2')
		t3_file = get_complete_filename('force_test_t3.txt')
		t3 = p.get_task('task3')
			
		# clear out the products of this pipeline
		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		# mark tasks
		t2.mark()

		# run task 3
		t3.run(force=FORCE_NONE)

		# check the output
		self.assertFalse(os.path.exists(t1_file))
		self.assertFalse(os.path.exists(t2_file))
		self.assertTrue(os.path.exists(t3_file))

		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		p.unmark_all_tasks(recur=True)

	def test_force_none(self):
		p = get_pipeline(get_complete_filename('force_test'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		t1_file = get_complete_filename('force_test_t1.txt')
		t1 = p.get_task('task1')
		t2_file = get_complete_filename('force_test_t2.txt')
		t2 = p.get_task('task2')
		t3_file = get_complete_filename('force_test_t3.txt')
		t3 = p.get_task('task3')
			
		# clear out the products of this pipeline
		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		# mark tasks
		t3.mark()

		# run task 3
		t3.run(force=FORCE_NONE)

		# check the output
		self.assertFalse(os.path.exists(t1_file))
		self.assertFalse(os.path.exists(t2_file))
		self.assertFalse(os.path.exists(t3_file))

		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		p.unmark_all_tasks(recur=True)

	def test_force_top(self):
		p = get_pipeline(get_complete_filename('force_test'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		t1_file = get_complete_filename('force_test_t1.txt')
		t1 = p.get_task('task1')
		t2_file = get_complete_filename('force_test_t2.txt')
		t2 = p.get_task('task2')
		t3_file = get_complete_filename('force_test_t3.txt')
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

		# run task 3
		t3.run(force=FORCE_TOP)

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

	def test_force_all(self):
		p = get_pipeline(get_complete_filename('force_test'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)
		t1_file = get_complete_filename('force_test_t1.txt')
		t1 = p.get_task('task1')
		t2_file = get_complete_filename('force_test_t2.txt')
		t2 = p.get_task('task2')
		t3_file = get_complete_filename('force_test_t3.txt')
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
		t2.mark()
		t3.mark()

		# run task 3
		t3.run(force=FORCE_ALL)

		# check the output
		self.assertTrue(os.path.exists(t1_file))
		self.assertTrue(os.path.exists(t2_file))
		self.assertTrue(os.path.exists(t3_file))

		if os.path.exists(t1_file):
			os.remove(t1_file)
		if os.path.exists(t2_file):
			os.remove(t2_file)
		if os.path.exists(t3_file):
			os.remove(t3_file)

		p.unmark_all_tasks(recur=True)

class LineNoTestCase(unittest.TestCase):

	def test_varexpands1(self):
		p = get_pipeline(get_complete_filename('lineno1'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)

		try:
			p.run()
		except ParseException as e:
			self.assertTrue(e.source_file.endswith('lineno1'))
			self.assertEquals(e.lineno,4)

		return

	def test_use_varexpands1(self):
		p = get_pipeline(get_complete_filename('lineno2'),
						 default_prefix=USE_FILE_PREFIX)
		p.unmark_all_tasks(recur=True)

		try:
			p.run()
		except ParseException as e:
			self.assertTrue(e.source_file.endswith('lineno1'))
			self.assertEquals(e.lineno,4)

		return

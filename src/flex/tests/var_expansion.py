import unittest
from flex.pipeline import get_pipeline, expand_variables, PIPELINE_PREFIX_VARNAME, ParseException
import flex.pipeline as pipeline
import os, os.path

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class InnerVarExpansionTestCase(unittest.TestCase):
	"""
	This tests the functionality of the expand_variables function.
	"""
	def test_basic1(self):
		context = {'var1':'hello'}

		exval = expand_variables('$var1.txt',context,-1)
		self.assertEquals(exval,'hello.txt')

		exval = expand_variables('${var1}.txt',context,-1)
		self.assertEquals(exval,'hello.txt')
			
		exval = expand_variables('hello_$var1.txt',context,-1)
		self.assertEquals(exval,'hello_hello.txt')

	def test_multvars1(self):
		context = {'var1':'hello', 'foobar':'test'}

		exval = expand_variables('${var1}_$foobar.txt',context,-1)
		self.assertEquals(exval,'hello_test.txt')

		exval = expand_variables('${var1}_${foobar}.txt',context,-1)
		self.assertEquals(exval,'hello_test.txt')
			
		exval = expand_variables('echo $var1 $foobar',context,-1)
		self.assertEquals(exval,'echo hello test')

	def test_pipeline_fxn1(self):
		context = {'var1':'hello', PIPELINE_PREFIX_VARNAME:'/foo/bar_'}

		exval = expand_variables('touch $PLN(test1.txt)',context,-1)
		self.assertEquals(exval,'touch /foo/bar_test1.txt')

		exval = expand_variables('touch $PLN($var1.txt)',context,-1)
		self.assertEquals(exval,'touch /foo/bar_hello.txt')

	def test_escape1(self):
		context = {'var1':'hello'}

		exval = expand_variables('\$var1.txt',context,-1)
		self.assertEquals(exval,'$var1.txt')

		exval = expand_variables('\${var1.txt',context,-1)
		self.assertEquals(exval,'${var1.txt')
			
		exval = expand_variables('\${var1}.txt',context,-1)
		self.assertEquals(exval,'${var1}.txt')
			
		exval = expand_variables('hello_$var1.txt',context,-1)
		self.assertEquals(exval,'hello_hello.txt')

class VarExpansionTestCase(unittest.TestCase):
	
	def test_varexpand1(self):
		"""
		This test case checks:

			- basic variable expansion
			- basic pipeline filename expansion
			- nested pipeline filename expansion
		"""
		p = get_pipeline(get_complete_filename('varexpand1'))
		p.unmark_all_tasks(recur=True)
		p.run()

		# check the output
		self.assertTrue(os.path.exists(get_complete_filename('hello_world.txt')))
		self.assertTrue(os.path.exists(get_complete_filename('varexpand1_pln_expand1.txt')))
		self.assertTrue(os.path.exists(get_complete_filename('varexpand1_hello.txt')))
		self.assertTrue(os.path.exists(get_complete_filename('varexpand1_pytest.dat')))

		os.remove(get_complete_filename('hello_world.txt'))
		os.remove(get_complete_filename('varexpand1_pln_expand1.txt'))
		os.remove(get_complete_filename('varexpand1_hello.txt'))
		os.remove(get_complete_filename('varexpand1_pytest.dat'))

		p.unmark_all_tasks(recur=True)


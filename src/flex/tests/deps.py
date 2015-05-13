import unittest
from flex.pipeline import get_pipeline, USE_FILE_PREFIX
import flex.pipeline as pipeline
import os, os.path

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class DependenciesTestCase(unittest.TestCase):
	
	def test_within_pipeline_graph(self):
		p = get_pipeline(get_complete_filename('dep_test1'),default_prefix=USE_FILE_PREFIX)

		vl = p.get_visitation_list()
		vl = {x[0].name:x[1] for x in vl}	

		self.assertDictEqual(vl,{'t4':0,'t3':1,'t2':1,'t1':2})

	def test_cross_pipeline_graph(self):
		p = get_pipeline(get_complete_filename('dep_test2'),default_prefix=USE_FILE_PREFIX)

		vl = p.get_visitation_list()
		vl = {x[0].name:x[1] for x in vl}	

		self.assertDictEqual(vl,{'p1_t4':0,'p1_t3':1,'p1_t2':1,'p1_t1':2,'p0_t3':3,'p0_t2':4,'p0_t1':5})


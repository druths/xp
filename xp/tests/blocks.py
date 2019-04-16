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
from xp.pipeline import get_pipeline, USE_FILE_PREFIX
import xp.pipeline as pipeline
import os, os.path

# check for gnuplot
gnuplot_installed = os.system('gnuplot -V') == 0

__all__ = ['BlockArgStringTestCase','AwkTestCase','PYHMRTestCase']

if gnuplot_installed:
    __all__.append('GnuplotTestCase')
else:
    print('gnuplot not found: skipping tests')

################
# define all the test cases

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
    return os.path.join(BASE_PATH,'pipelines',fname)

class BlockArgStringTestCase(unittest.TestCase):

    def test_basic1(self):
        p = get_pipeline(get_complete_filename('argstr_basic1'),
                        default_prefix=USE_FILE_PREFIX)
        p.unmark_all_tasks()
        p.run()

        fname = get_complete_filename('argstr_basic1_a1.txt')

        self.assertTrue(os.path.exists(fname))
        os.remove(fname)

class AwkTestCase(unittest.TestCase):

    def test_awk1(self):
        p = get_pipeline(get_complete_filename('awk1'),
                        default_prefix=USE_FILE_PREFIX)
        p.unmark_all_tasks()
        p.run()

        fname = get_complete_filename('awk1_out.txt')

        self.assertTrue(os.path.exists(fname))
        os.remove(fname)

class GnuplotTestCase(unittest.TestCase):
    
    def test_basic1(self):
        
        p = get_pipeline(get_complete_filename('gpl_basic1'),default_prefix=USE_FILE_PREFIX)
        p.unmark_all_tasks()
        p.run()

        self.assertTrue(os.path.exists(get_complete_filename('gpl_basic1_output1.png')))
        self.assertTrue(os.path.exists(get_complete_filename('output2.png')))

        os.remove(get_complete_filename('gpl_basic1_output1.png'))
        os.remove(get_complete_filename('output2.png'))

class PYHMRTestCase(unittest.TestCase):

    def test_basic1(self):
        p = get_pipeline(get_complete_filename('pyhmr_test1'),
                        default_prefix=USE_FILE_PREFIX)
        p.unmark_all_tasks()
        p.run()

        fname = get_complete_filename('pyhmr_test1.out')

        self.assertTrue(os.path.exists(fname))
        contents = open(fname,'r').read()

        self.assertTrue('test\t2' in contents)
        self.assertTrue('hello\t3' in contents)

        os.remove(fname)



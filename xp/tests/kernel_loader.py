"""
Copyright 2017 Derek Ruths

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

import xp.config as config
import xp.kernel_loader as kernel_loader

BASE_PATH = os.path.dirname(__file__)

def get_complete_filename(fname):
	return os.path.join(BASE_PATH,'pipelines',fname)

class KernelLoaderTestCase(unittest.TestCase):

	def test_no_kernels(self):
		config.initialize_config_info_from_string("""
[Kernels]
active_kernels:
""")
		kl = kernel_loader.KernelLoader.reinitialize_singleton()

		self.assertEquals(len(kl.kernels()),0)

		config.initialize_config_info()
		kernel_loader.KernelLoader.reinitialize_singleton()

	def test_one_kernels(self):
		config.initialize_config_info_from_string("""
[Kernels]
active_kernels: xp.kernels.test.TestKernel
""")
		kl = kernel_loader.KernelLoader.reinitialize_singleton()

		self.assertEquals(len(kl.kernels()),1)

		config.initialize_config_info()
		kernel_loader.KernelLoader.reinitialize_singleton()

	def test_custom_kernel_lang_suffix(self):
		config.initialize_config_info_from_string("""
[Kernels]
active_kernels: xp.kernels.test.TestKernel(mytest)
""")
		kl = kernel_loader.KernelLoader.reinitialize_singleton()

		self.assertEquals(len(kl.kernels()),1)
		self.assertEquals(kl.lang_suffixes(),['mytest'])

		config.initialize_config_info()
		kernel_loader.KernelLoader.reinitialize_singleton()


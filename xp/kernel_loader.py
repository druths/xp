import os.path
import logging

import config

logger = logging.getLogger(os.path.basename(__file__))

class KernelLoader:

	_singleton = None

	@staticmethod
	def singleton():
		if KernelLoader._singleton is None:
			KernelLoader()

		return KernelLoader._singleton

	def __init__(self):
		if KernelLoader._singleton is not None:
			raise Exception, 'A KernelLoader already exists'

		self.__initialize()

		KernelLoader._singleton = self

	def __initialize(self):
		config_info = config.config_info()

		# TODO: add the kernel paths to the PYTHONPATH
		pass

		# load the lang_suffix to kernel mapping
		self._lang_map = {}

		kernel_names = config_info.get(config.KERNELIMPL_SECTION,config.ACTIVE_KERNELS_OPT).split()
		for kname in kernel_names:
			kernel_class = self.__get_kernel_class(kname)
			self._lang_map[kernel_class.default_lang_suffix()] = kernel_class

		# done

	def __get_kernel_class(self,full_class_name):
		module_path,class_name = full_class_name.rsplit('.',1)
		logger.debug('getting kernel: %s.%s' % (module_path,class_name))

		#module = get_module(module_path) 
		#print module.__file__
		#print dir(module)
		#kernel_class = getattr(module,class_name)
		module = __import__(module_path, fromlist=[class_name])
		kernel_class = getattr(module,class_name)

		return kernel_class

	def __contains__(self,lang_suffix):
		return lang_suffix in self._lang_map

	def get_kernel(self,lang_suffix):
		# instantiate a kernel
		return self._lang_map[lang_suffix]()

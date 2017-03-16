import os.path
import logging
import re

import config

logger = logging.getLogger(os.path.basename(__file__))

ACTIVE_KERNEL_CLASS_PATTERN = re.compile('(\w[\w_\.]*)(\([\w_]+\))?')

class KernelLoader:

	_singleton = None

	@staticmethod
	def reinitialize_singleton():
		"""
		Re-create the singleton and return the new object.  This is typically only used for unit testing.
		"""
		KernelLoader._singleton = None
		return KernelLoader.singleton()

	@staticmethod
	def singleton():
		"""
		Return the KernelLoader instance that is used in this VM.
		"""
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

		kernel_names = config_info.get(config.KERNELS_SECTION,config.ACTIVE_KERNELS_OPT).split()
		for kname in kernel_names:
			m = ACTIVE_KERNEL_CLASS_PATTERN.match(kname)
			if not m:
				raise Exception, 'unable to parse kernel name: %s' % kname

			kname = m.group(1)
			lang_suffix = m.group(2)

			kernel_class = self.__get_kernel_class(kname)
			if not lang_suffix:
				lang_suffix = kernel_class.default_lang_suffix()
			else:
				lang_suffix = lang_suffix[1:-1]

			self._lang_map[lang_suffix] = kernel_class

		# done

	def __get_kernel_class(self,full_class_name):
		module_path,class_name = full_class_name.rsplit('.',1)
		logger.debug('getting kernel: %s.%s' % (module_path,class_name))

		module = __import__(module_path, fromlist=[class_name])
		kernel_class = getattr(module,class_name)

		return kernel_class

	def __contains__(self,lang_suffix):
		return lang_suffix in self._lang_map

	def get_kernel(self,lang_suffix):
		# instantiate a kernel
		return self._lang_map[lang_suffix]()

	def kernels(self):
		return self._lang_map.values()

	def lang_suffixes(self):
		return self._lang_map.keys()

import logging
import os, os.path
from ConfigParser import RawConfigParser

logger = logging.getLogger(os.path.basename(__file__))

KERNEL_SECTION = 'Kernel'
KERNELIMPL_SECTION = 'KernelImpl'
ACTIVE_KERNELS_OPT = 'active_kernels'

DEFAULT_CONFIG_DIR = os.path.join(os.environ['HOME'],'.config','xp')

__config_info = None

def configure_parser(config_parser):
	"""
	Load the default configurations and constraints into the RawConfigParser object provided.	
	"""
	logger.debug('configuring the parser with defaults')
		
	#config_parser.add_section('DEFAULT')

	config_parser.add_section(KERNEL_SECTION)
	config_parser.set(KERNEL_SECTION,'config_dir',DEFAULT_CONFIG_DIR)
	config_parser.set(KERNEL_SECTION,'kernel_paths','%(config_dir)s/kernels')
	
	config_parser.add_section(KERNELIMPL_SECTION)
	config_parser.set(KERNELIMPL_SECTION,'active_kernels',
		"""	xp.kernels.test.TestKernel 
			xp.kernels.shell.ShellKernel
			xp.kernels.gnuplot.GNUPlotKernel
			xp.kernels.awk.AwkKernel
			xp.kernels.python.PythonKernel
			xp.kernels.pyhmr.PythonHadoopMapReduceKernel""")

	return

def initialize_config_info(config_filename=None):
	"""
	Return a RawConfigParser for the platform.

	If config_filename is None, then an attempt is made to load the user-specific configuration file.
	If this is not found, then the fall back is the contents provided by the default configurations,
	supplied by configure_parser(config_info).
	"""
	global __config_info

	__config_info = RawConfigParser()
	configure_parser(__config_info)

	# try to read in a configuration
	user_config_filename = os.path.join(DEFAULT_CONFIG_DIR,'xp.ini')

	if config_filename is not None:
		logger.info('reading non-default config file: %s' % config_filename)
		__config_info.read(config_filename)
	elif os.path.exists(user_config_filename):
		logger.info('reading default config file: %s' % user_config_filename)
		__config_info.read(user_config_filename)
	else:
		logger.info('no config file read')
	
def config_info():
	"""
	Return the initialized config_info object.
	"""
	global __config_info

	if __config_info is None:
		initialize_config_info()

	return __config_info

from distutils.core import setup	
import os.path
import sys

setup(
	name = 'flexds',
	version = '1.1',
	packages = ['flex','flex.tests','flex.tests.pipelines'],
	package_data = {'flex.tests.pipelines' : ['*'] },

	scripts = ['scripts/fx'],

	# # dependencies

	# # testing suite
	#test_suite = 'flex.test',

	# # project metadata
	author = 'Derek Ruths',
	author_email = 'druths@networkdynamics.org',
	description = 'Flex is a framework for building and executing computing pipelines',
	license = 'Apache',
	url = 'https://github.com/druths/flex',
	keywords = ['data science','research','build','automation'],
	classifiers=[
		'Development Status :: 5 - Production/Stable',

		'Environment :: Console',

		'Intended Audience :: Science/Research',
		'Intended Audience :: Information Technology',

		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Utilities',

		'License :: OSI Approved :: Apache Software License',

		'Programming Language :: Python :: 2.7']
)

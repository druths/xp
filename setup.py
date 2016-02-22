from distutils.core import setup	
import os.path
import sys

setup(
	name = 'xp',
	version = '1.1',
	packages = ['xp','xp.tests','xp.tests.pipelines'],
	package_data = {'xp.tests.pipelines' : ['*'] },

	scripts = ['scripts/xp'],

	# # dependencies

	# # testing suite
	#test_suite = 'xp.test',

	# # project metadata
	author = 'Derek Ruths',
	author_email = 'druths@networkdynamics.org',
	description = 'xp is a framework for building and executing computing pipelines',
	license = 'Apache',
	url = 'https://github.com/druths/xp',
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

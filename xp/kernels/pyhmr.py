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

import subprocess
from subprocess import CalledProcessError
import logging
import os.path
import tempfile

from xp.kernels.base import Kernel, get_total_context

logger = logging.getLogger(os.path.basename(__file__))

class PythonHadoopMapReduceKernel(Kernel):

    @staticmethod
    def default_lang_suffix():
        return 'pyhmr'

    @staticmethod
    def short_help():
        """
        Return a short description of the kernel.
        """
        return 'Hadoop map-reduce in python'

    @staticmethod
    def long_help():
        """
        Return a detailed description of the kernel, how it works, how it is configured, and used.
        """
        return """This code block type encapsulates a Hadoop map-reduce task implemented in
Python. The map-reduce capability is mediated through the Hadoop streaming API.
This code block should contain two functions: map(stream) and reduce(stream).

For map(stream), stream is an iterable over string lines, no format assumed.
The output should be printed to stdout with the format, string key-value pairs
with some character separator (tab separators are typical).

For reduce(stream), stream is an iterable over the output of one or more
map(stream) functions. The output of the reduce should also be string key-value
pairs.

Note that in order for this block to run, three environment variables MUST be
set: PYHMR_INPUT, PYHMR_OUTPUT, and PYHMR_STREAMING_API_JAR.""",

    @staticmethod
    def env_vars_help():
        """
        Return a dictionary of environment variables (keys) and their meaning (values).
        """
        return {    'PYHMR_HADOOP_CMD':'the Hadoop executable that should be invoked. Default is "hadoop"',
                    'PYHMR_PYTHON_CMD':'the Python executable that should be invoked on the DataNodes. Default is "python"',
                    'PYHMR_INPUT':'the input files in the HDFS (required)',
                    'PYHMR_OUTPUT':'the output location on the HDFS (required)',
                    'PYHMR_STREAMING_API_JAR':'the absolute path to the streaming API jar included with the Hadoop installation (required)',
                    'PYHMR_EXTRA_FILES':'any extra files that should be bundled with the task on the DataNodes',
                    'PYHMR_NUM_REDUCERS':'the number of reducers that should be used in performing this task',
                    'PYHMR_TEST_CMD':'a command that can be used to test this map-reduce task. If this is set, then the task will be run in test mode (Hadoop will not be run, the HDFS will not be accessed).  The output of this command will be used as input to the mapper (which will then be used as input to the reducer).  The output will be printed to STDOUT.',
                    'PYHMR_TEST_OUTPUT':'the file that the result of the test will be written to.  If not specified, STDOUT will be used.'}

    def run(self,arg_str,context,cwd,content):
        """
        Raises a CalledProcessError if this fails.
        """
        # get configuration
        HADOOP_CMD_EV = 'PYHMR_HADOOP_CMD'
        PYTHON_CMD_EV = 'PYHMR_PYTHON_CMD'
        STREAMING_API_JAR_EV = 'PYHMR_STREAMING_API_JAR'
        INPUT_EV = 'PYHMR_INPUT'
        OUTPUT_EV = 'PYHMR_OUTPUT'
        EXTRA_FILES_EV = 'PYHMR_EXTRA_FILES'
        NUM_REDUCERS_EV = 'PYHMR_NUM_REDUCERS'
        TEST_CMD_EV = 'PYHMR_TEST_CMD'
        TEST_OUTPUT_EV = 'PYHMR_TEST_OUTPUT'
    
        hadoop_cmd = context.get(HADOOP_CMD_EV,'hadoop')
        python_cmd = context.get(PYTHON_CMD_EV,'python')
    
        streaming_api_jar = context.get(STREAMING_API_JAR_EV)
        input_location = context.get(INPUT_EV)
        output_location = context.get(OUTPUT_EV)
    
        extra_files = context.get(EXTRA_FILES_EV,'')
        num_reducers = context.get(NUM_REDUCERS_EV,None)
    
        test_cmd = context.get(TEST_CMD_EV,None)
        test_output = context.get(TEST_OUTPUT_EV,None)
        is_test = test_cmd is not None
    
        # make the mapper file
        fh,mapper_filename = tempfile.mkstemp(suffix='py')
        os.write(fh,'\n'.join(content).encode())
        os.write(fh,"""
    
if __name__ == '__main__':
    import sys
    map(sys.stdin)
""".encode())
        os.close(fh)
    
        logger.debug('wrote mapper to %s' % mapper_filename)
    
        # make the reducer file
        fh,reducer_filename = tempfile.mkstemp(suffix='py')
        os.write(fh,'\n'.join(content).encode())
        os.write(fh,"""
    
if __name__ == '__main__':
    import sys
    reduce(sys.stdin)
""".encode())
        os.close(fh)
    
        logger.debug('wrote reducer to %s' % reducer_filename)
    
        # switch behavior conditional on testing
        if is_test:
            logger.warn('running map-reduce task in test mode')
    
            cmd = '%s | %s %s | %s %s' % (test_cmd,python_cmd,mapper_filename,python_cmd,reducer_filename)
    
            if test_output is not None:
                cmd += ' > %s' % test_output
    
            logger.debug('using cmd: %s' % cmd)
            retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))
        
            if retcode != 0:
                raise CalledProcessError(retcode,cmd,None)
        else:
            logger.info('running map-reduce task in normal mode')
    
            cmd = '%s jar %s' % (hadoop_cmd,streaming_api_jar)
            cmd += ' -input "%s" -output "%s"' % (input_location,output_location)
            cmd += ' -mapper "%s %s" -reducer "%s %s"' % (python_cmd,mapper_filename,python_cmd,reducer_filename)
            cmd += ' -files "%s"' % ','.join([mapper_filename,reducer_filename,extra_files])
            if num_reducers is not None:
                cmd += ' -D mapred.reduce.tasks=%s' % num_reducers
    
            logger.debug('using cmd: %s' % cmd)
            retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))
        
            if retcode != 0:
                raise CalledProcessError(retcode,cmd,None)
        

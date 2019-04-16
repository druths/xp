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

class PythonKernel(Kernel):

    @staticmethod
    def default_lang_suffix():
        return 'py'

    @staticmethod
    def short_help():
        """
        Return a short description of the kernel.
        """
        return 'run python code'

    @staticmethod
    def long_help():
        """
        Return a detailed description of the kernel, how it works, how it is configured, and used.
        """
        return 'Run the commands in whatever the default python VM is on the host system.'

    @staticmethod
    def env_vars_help():
        """
        Return a dictionary of environment variables (keys) and their meaning (values).
        """
        return {
            'PYTHON_CMD': 'the python executable that will be run to execute the block code'
        }

    def run(self,arg_str,context,cwd,content):
        """
        Raises a CalledProcessError if this fails.
        """
    
        # write python code to a tmp file
        fh,tmp_filename = tempfile.mkstemp(suffix='py')
        os.write(fh,'\n'.join(content).encode())
        os.close(fh)

        logger.debug('wrote python content to %s',tmp_filename)

        exec_name = context.get('PYTHON_CMD','python')
        cmd = '%s %s %s' % (exec_name,arg_str,tmp_filename)
        logger.debug('using cmd: %s',cmd)
        retcode = subprocess.call(cmd,shell=True,cwd=cwd,env=get_total_context(context))
    
        if retcode != 0:
            raise CalledProcessError(retcode,cmd,None)


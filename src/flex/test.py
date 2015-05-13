import unittest
import logging

from tests.basic_tests import *
from tests.var_expansion import *
from tests.prefix import *
from tests.deps import *
from tests.blocks import *

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)

	unittest.main()

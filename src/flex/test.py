import unittest
import logging

from tests.basic_tests import *
from tests.config import *
from tests.var_expansion import *
from tests.prefix import *
from tests.deps import *
from tests.blocks import *
from tests.overload import *
from tests.dep_cases import *

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)

	unittest.main()

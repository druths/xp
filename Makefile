
all:

test_inplace:
	PYTHONPATH=.:$$PYTHONPATH python -m xp.test $(TEST)

install_user:
	python setup.py install --user

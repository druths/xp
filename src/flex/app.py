import os, os.path
import argparse
import logging

logger = logging.getLogger(os.path.basename(__file__))

LOG_LEVELS = ['DEBUG','WARN','ERROR','FATAL']

def do_info(args):
	parser = argparse.ArgumentParser('fx info',description='print information on a particular pipeline')
	parser.add_argument('pipeline_file',help='the pipeline to unmark tasks in')

	# TODO
	pass

def do_unmark(args):
	parser = argparse.ArgumentParser('fx unmark',description='unmark one or more tasks')
	parser.add_argument('-r','--recur',action='store_true',help='unmark all dependent tasks as well')
	parser.add_argument('pipeline_file',help='the pipeline to unmark tasks in')
	parser.add_argument('task_name',nargs='?',help='the specific task to unmark. If omitted, the entire pipeline will be unmarked')

	# TODO
	pass

def do_mark(args):
	parser = argparse.ArgumentParser('fx unmark',description='unmark one or more tasks')
	parser.add_argument('-r','--recur',action='store_true',help='unmark all dependent tasks as well')
	parser.add_argument('pipeline_file',help='the pipeline to unmark tasks in')
	parser.add_argument('task_name',nargs='?',help='the specific task to unmark. If omitted, the entire pipeline will be unmarked')

	# TODO
	pass

def do_run(args):
	parser = argparse.ArgumentParser('fx run',description='run a flex pipeline')
	parser.add_argument('-f','--force',action='store_true',help='force the task to run, even if it is already marked')
	parser.add_argument('pipeline_file',help='the pipeline to run')
	parser.add_argument('task_name',nargs='?',help='the specific task to run. If omitted, the entire pipeline will be run')

	# TODO
	pass

def main():
	parser = argparse.ArgumentParser('fx')
	parser.add_argument('-l','--log_level',choices=LOG_LEVELS,'ERROR')
	parser.add_argument('command',choice=COMMANDS)
	parser.add_argument('args',nargs=argparse.REMAINDER)

	args = parser.parse_args()

	# configure the logger
	log_level = eval('logging.%s' % args.log_level)
	logging.basicConfig(level=log_level)

	# run the command
	logger.debug('running command: %s' % args.command)
	eval('do_%s(args.args)' % args.command)

	return

if __name__ == '__main__':
	main()


.. toctree::
	:maxdepth: 2

*****************
The ``xp`` command
*****************

All of xp's functionality is accessed through the ``xp`` command line tool.
You'll first need a pipeline, of course.  For illustration purposes, throughout
this section, we'll use the pipeline ``foobar``, which has the following
contents::

	use configurator as config

	download_data: config.setup_env
		code.sh:
			curl www.greatdata.com/dataset1.tsv > $PLN(dataset1.tsv)

	extract_col1: download_data
		code.sh:
			cut -f 1 $PLN(dataset1.tsv) > $PLN(col1.txt)

A bit of vocabulary will help our discussion of the behavior of the ``xp``
command:

  * a *direct dependency of a task* (say, ``taskX``) is another task which
	appears in the dependency list of ``taskX``.  In ``foobar``,
	``download_data`` is direct dependency of ``extract_col1``.

  * the *dependencies of a task* (say, ``taskX``) are *all* the direct 
	dependencies of ``taskX`` as well as the direct dependencies of those tasks
	and so forth. In ``foobar``, the dependencies of ``extract_col1`` includes
	``download_data`` as well as ``config.setup_env`` and an tasks that
	``setup_env`` depends on.

  * a *terminal task* is a task that isn't in the dependency list of any other
	task in the pipeline.  In ``foobar``, ``extract_col1`` is the only terminal
	task.

  * a task becomes *marked* when it is successfully run. Typically this is used
	to ensure that the task isn't run again.

##################
Running a pipeline
##################

The most fundamental activity we'll need to do is running a tasks in a pipeline. 

**Running a complete pipeline.** To run all tasks in your pipeline, use ``xp
run <pipeline_file>``. This will run all unmarked terminal tasks and their
dependencies. They are run in dependency order - so the terminal task will be
the last task run.  For details on the rules that govern if and when a
dependency is run, see :ref:`dependency_running`.

**Running a specific task.** To run a specific task in your pipeline, use ``xp
run <pipeline_file> <task_name>``.  This will run the task (if unmarked) as
well as its dependencies.

**Running marked tasks.** If you do want to run a task that has already been
marked, you have two options.

  1. Unmark the relevant task using the ``xp unmark`` command.

  2. Use the ``-f`` flag to force tasks to be run. This flag takes an argument
  which determines what tasks are forced to run. 
  
	* ``run -f=NONE`` doesn't override any markings. This is the default
	behavior.

	* ``run -f=TOP`` overrides the marking on only the terminal task/specified
	task.

	* ``run -f=ALL`` overrides the markings on all tasks encountered during the
	run. *Be careful* when using this option as it can cause tasks far down the dependency tree to be re-run.

	* ``run -f=SOLO`` ignores any dependencies the named task may have and runs just that task.


.. _dependency_running:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When and if dependencies are run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, when xp wants to run a task (we'll call this the *final task*),
it will first check to see if any of the dependencies of that task need to be
run first.

The order of dependency evaluation is set such that a particular task is never
evaluated before its direct dependencies. When this policy is applied to all
dependencies of the final task, we end with an ordering that starts with the
tasks which have no dependencies and end with the final task.

When a task is being evaluated, it is run if either of the following conditions
are true:

  1. the task is unmarked

  2. the task's mark is older than one of its direct dependencies.

In either of these cases, the task will be run and, if successful, it will be
marked.

###########################
Marking and unmarking tasks
###########################

To mark a specific task, use ``xp mark <pipeline_file> <task_name>``. If the
task specified is not marked, it will be marked.  If the task is already
marked, then the timestamp on the task's mark will be updated.

To unmark a specific task, use ``xp unmark <pipeline_file> <task_name>``. This
will remove the mark on the task (if it exists).

#################################
Checking status of pipeline tasks
#################################

You can use the ``xp tasks <pipeline_file>`` command to print out information
about all the tasks in the pipeline. This will print the tasks in the pipeline
as well as any tasks in other pipelines on which it depends. The timestamp of
any marked tasks will be given.

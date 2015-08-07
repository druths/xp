

.. toctree::
	:maxdepth: 2

*****************
Pipeline overview
*****************

The purposes of a pipeline are to:

  * make explicit the high-level logic that achieves some goal

  * connect the pipeline logic to the intermediate and final data produced

In much the same way as a make file, a flex pipeline consists of two parts:

  * *tasks* - these perform coherent chunks of work.  In this regard, tasks are
	very much the heart of the flex pipeline. In a departure from make, flex
	tasks themselves consist of blocks which are small language-specific units
	of work. For more details on this, see :ref:`tasks_section`.

  * *global definitions* - while the tasks are the heart of flex, some
	additional configurations are needed in order to make tasks easier to write
	and make connections between the pipeline and other pipelines.  As a
	result, a flex pipeline starts with a global section, which allows for the
	definition of variables as well as for the specification of pipeline
	configurations and connections.  For more details on this, see
	:ref:`global_section`.

From a more functional perspective, most pipelines will have two properties
that need to be addressed with additional high-level designs and pipeline
conventions:

  * they produce data

  * they conceptually depend on pipelines (in a variety of ways)

These are discussed in the following subsections.

.. _data_namespacing:

##################
Data Namespacing
##################

In order to ensure that data produced by the pipeline is always linkable to it,
the pipeline maintains a namespace on the filesystem which a pipeline can
easily add files to.  The namespace can be one of two things:

  * a prefix that is added to any given filename.  By default the prefix would
	be the name of the pipeline.  So if the pipeline `clean_census_info` had a
	task which added the file `census.tsv` to the pipeline namespace, the file
	would actually be named `clean_census_info_census.tsv` on disk.
	
  * a directory into which all files in the namespace are added. By default the
	directory name is `<pipeline_name>_data`. So, given the situation above
	with `clean_census_info`, `census.tsv` would be written to
	`clean_census_info_data/census.tsv`.

The namespacing behavior can be configured in the global section, see
:ref:`config_data_prefixing`.

###############################
Dependencies on other pipelines
###############################

A pipeline can depend on other pipelines in two different ways.

The first and most mundane is when the tasks in one pipeline depend on the
tasks in another pipeline.  One can imagine that this second pipeline is
*using* the first pipeline in order to build a bigger "mega" pipeline (that
consists of both of them).  This crops up a lot in even small-scale projects.
One pipeline might deal with data download and curation, another with
pre-processing data, and a third with training models or doing analysis.  Each
phase could be put in a separate pipeline, but they would all use one another.

The second and more subtle kind of dependency is when one pipeline is basically
a modification of another pipeline.  For example, suppose we want to run the
same analysis using different thresholds: it's the same analysis running on the
same data - with just one or two parameters set differently.  Rather than
duplicating all the code for the pipeline, we can create a second pipeline that
*extends* the first one, just setting some specific variables to different
values. 

For details on these, see :ref:`declaring_dependencies`.

.. _global_section:

##########
Comments
##########

Thoroughly commenting pipelines is an important part of making them readable
and maintainable. Within a flex pipeline, a comment is always one line long:
beginning with a `#` symbol and continuing to the end of the line.

******************
The global section
******************

The global section permits the specification of configurations and variables
that will affect and be available to all tasks in the pipeline.

####################
Declaring variables
####################

Note that here we offer a detailed discussion of variables within the context of the global section. For more information on variables and functions in general, see :ref:`variables_and_functions`.

In keeping with UNIX shell syntax, variables are set using the syntax::

	set <var_name>=<var_value>

Throughout a pipeline, the `$` character denotes a variable or function
reference.

.. _config_data_prefixing:

##########################
Configuring data prefixing
##########################

The flex system provides an easy way to create and access files and directories
within the pipelines namespace.  The namespace can be either a file prefix name
or a directory (see :ref:`data_namespacing` for details).  The `prefix` command
is used to configure this option for a given pipeline.

The general syntax for this command is::

	prefix file/dir [prefix_path]

if `prefix_path` is omitted, then the following defaults are used:

  * `<pipeline name>` for file prefixes
  * `<pipeline name>_data` for dir prefixes

Here are some examples:

  * to set the prefix to be the default file prefix, use `prefix file`

  * to set the prefix to the file prefix *foobar*, use `prefix file foobar`

  * to set the prefix to the default directory prefix, use `prefix dir`

  * to set the prefix to the **data** directory above the pipeline's 
	containing directory, use `prefix dir ../data`

##########################
Connecting other pipelines
##########################

The tasks in a single pipeline may comprise only one portion of an entire
workflow.  Supposing that we have a pipeline `phase1` with task `t1`, we can
connect it into another pipeline using the `use` keyword in the global section.

::

	use phase1

	p2_task: phase1.t1
		# task stuff goes here

The `use` keyword also allows easier or more readable aliases to be defined::

	use phase1 as p1

	p2_task: p1.t1
		# task stuff goes here

###########################
Inheriting another pipeline
###########################

In some cases, a pipeline will be a specialization of another pipeline - it will need to use the same tasks, but perhaps define constants or parameters differently.  This can often arise in machine learning contexts - different pipelines might invoke the same classifier, only with different parameters.

One way to achieve this without duplicating large sections of code is to write the shared code (tasks and variables) into one pipeline and have all the related pipelines inherit that pipeline using the `extend` keyword.

For example, suppose that we have a pipeline named `ml_master` which declares two
tasks `train` and `classify` that use the value of the variable `GRID_SIZE` to
build and run the classifier.

We could build a pipeline `ml_0.5` that inherits the behavior of `ml_master`,
but with a specific choice of `GRID_SIZE`::

	extend ml_master

	set GRID_SIZE=0.5

.. _tasks_section:

*******************
The tasks section
*******************

Tasks form the heart of a pipeline: they contain the logical steps that perform
actions.  A single task should correspond to some meaningful and self-contained
unit of work.

#######################
The structure of a task
#######################

Since flex is entirely concerned with capturing computational workflows, tasks
contain code in executable units called *blocks*.  In order to link tasks to
one another, a task can depend on one or more other tasks (called its
*dependencies*).

A task has the following structure::

	<task_name>: [<dep1> <dep2> ...]
		<block1>
		<block2>
		...
		<blockN>

As a simple example, here is a task named `hworld` that simply prints "Hello"
followed by "world" on two separate lines::

	hworld: other_task
		code.sh:
			MSG=Hello
			echo \$MSG
		code.py:
			msg = 'world'
			print msg

The task depends on another task named `other_task`.  In order to print the
results, it uses two code blocks - one containing a shell script and one
containing a python script.  The details of the syntax here will be discussed
in the following section.

.. _declaring_dependencies:

######################
Declaring dependencies
######################

A dependency is another task.  To declare a dependency, simply put the task name in the task declaration line after the colon::

	# first_pipeline

	first:
		code.sh:
			echo 'first'

	second: first
		code.sh:
			echo 'second'

In the example above, the task `second` has one dependency: `first`.

In situations where a pipeline has been included with the `use` keyword, tasks in the included pipeline can be dependencies.  To do this, use `<pipeline_name>.<task_name>` to refer to the task.  If an alias was given for the pipeline, then the alias must be used::

	use first_pipeline as fp

	third: fp.second
		code.sh:
			echo 'third'


################
Declaring blocks
################

A block corresponds to a unit of executable code *in a specific language*. A single block might be written in bash, python, or any other supported language.

A block consists of the block declaration line (indented one tab) followed by the block contents (all of which is intended two levels).

**Block declaration.** The block declaration line indicates what language is
being used. `code.sh` corresponds to the shell language, `code.py` corresponds
to python.  Currently the following languages are supported:

  * Bash - `code.sh`
  * Python - `code.py`
  * Gnuplot - `code.gpl`
  * Awk - `code.awk`

There is also another special block called `export` which accepts variable
declarations using the same format as the globals section.  *export* blocks can
be used to set variables within the scope of this specific task.

**Block content.** Block content is further indented under the block declaration line. For example::

	task1:
		code.sh:
			ls -1 > contents.txt
		code.py:
			x = 1
			y = 2
			print 'Two numbers: %d %d' % (x,y)

In this example, there are two code blocks. The contents of the code block can
contain arbitrary content that adheres to the language of the block.

**Execution order.** When a task contains more than one block, the blocks are
executed in the order in which they are declared in the pipeline file. So in
the example above, the shell block would be executed, followed by the python
block.

**Use of variables.** Variables and functions will be discussed in much more
detail in :ref:`variables_and_functions`.  While discussing blocks, however,
several points are worth noting.

Before the block content is passed to the appropriate execution system (e.g.,
the python interpreter), flex variables and functions are first evaluated.  All
variables and functions begin with a `$` character::

	# var_test pipeline
	in_dir=/etc
	out_fname=output.dat

	do_it:
		export:
			tmp_file=__foobar.txt
		code.sh:
			export PATH=~/local/bin:\$PATH
			ls -l $in_dir > $tmp_file
			cut -f1 > $out_fname

In the example above, the shell code block makes use of three flex-defined
variables, `in_dir`, `tmp_file`, and `out_fname`.  Notice that it also
references the shell variable `PATH` and that, in order to make this reference,
a backslash is used to escape the `$` character.

#################
Overloading tasks
#################



.. _variables_and_functions:

***********************
Variables and functions
***********************

As alluded to in earlier sections, variables and functions are important to
writing modular, readable, and maintainable pipelines.  Here we discuss the
guts of how variables, variable references, and function invocations are
handled and resolved.

##############
Syntax
##############

###################
Available functions
###################

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Referencing another pipelines resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At times it may be necessary for one pipeline to access a resource in another
pipeline's namespace.  The `$PLN(p,r)` function can be used for this purpose.
Here the function accepts two arguments. `p` is the name of the pipeline (which
must be mentioned in a `use` statement) and `r` is the resource name.  For
example, in the following code

```
	use phase1 as p1

	p2_task: p1.t1
		code.sh:
			head $PLN(p1,foobar.txt)
```

`p2_task` will access the file `foobar.txt` in the namespace of the phase1
pipeline.



################
Resolution rules
################

######################
Global vs. block scope
######################



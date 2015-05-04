
Feature TODO list
~~~~~~~~~~~~~~~~~
	
v0.1
----

	* Implement $PLN(pipeline_alias,fname) capabilities

	* Implement command line tool 'fx' to do the following
		- 'run' = Run a particular task
		- 'wipe' = Delete all files for a particular pipeline
		- 'unmark' = Eliminate all marks for tasks in the pipeline specified

	* code block support for:
		gnuplot
		X python
		X sh

	* Implement $(...) command which executes the information in the shell within the current context 

	* Implement overloading of tasks (the last task of the given name kills all earlier ones)

v0.2
----
	* modularize the code block execution code

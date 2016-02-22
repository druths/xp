
XP Roadmap
~~~~~~~~~~~~
	
v0.1
----

	* Write tutorial blog post

	* Make a couple example pipelines

	* Post to Reddit

	* Post to Twitter

v0.2
----
	
	* Implement fx commands: import, export, info, and dry_run 

	* Add support for code block execution code checking
		* block_type.check()
		* fx command: check_block_support

	* Modularize the code block execution code

	* Add parallel task execution

v0.3
----

	* Add task generators. Something like this::

		# there are two general approaches we might take here...

		# Approach 1: internal task generators
		gen_${year}_data: download_${year}_data
			generator.py:
				for x in range(2011,2015):
					yield {'year':x}

		# Approach 2: combined task generators
		download_${year}_data (dd):
			code.sh:
				curl http://some.web.server/myfile_${year}.tgz > $PLN(myfile_${year}.tgz)

		gen_${year}_data (gd): download_${year}_data
			code.sh:
				blah blah

		task generator:
			

Distant Future
--------------

	* Add distributed task execution (flex cluster)

	* Implement notebook interface (ala ipython & jupyter)
		* Add support for comment blocks that have markdown format or something.  This would allow pipelines to be workbooks in themselves.

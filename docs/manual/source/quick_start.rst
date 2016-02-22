
Quick Start
===========

xp makes it easy to create and update computational workflows (called
pipelines) that always retain a connection to the data that the pipeline
produced.

------------
Installation
------------

The easiest way to install xp is using pypi::

	pip install xp

Alternatively, install xp by downloading the source and running::

	python setup.py install

or::

	sudo python setup.py install

depending on permission settings for your python site-packages.

---------------------
Writing a pipeline
--------------------

A *pipeline* is a sequence of steps (called *tasks*) that manipulates data.  On
a very practical level, each task takes some data as input and produces
other data as output. In the example below, there are four tasks, each
involved in a different part of the workflow.

::

	# Pipeline: cluster_data

	DATA_URL=http://foobar:8080/data.tsv
	NAME_COLUMN=1
	COUNT_COLUMN=2
	ALPHA=2
	
	download_data:
		code.sh:
			curl $DATA_URL > data.tsv
	
	extract_columns: download_data
		code.sh:
			cut -f $NAME_COLUMN,$COUNT_COLUMN data.tsv | tail +2 > xdata.tsv
		code.py:
			from csv import reader
			fout = open('xdata2.tsv','w')
			for data in reader(open('xdata.tsv','r'),delimiter='\t'):
				fout.write('%s\t%s\n' % (data[0],data[1][1:-1])
		
	cluster_rows: extract_columns
		code.sh:
			./cluster.sh --alpha $ALPHA xdata2.tsv > clusters.tsv
	
	plot_clusters: cluster_rows
		code.gnuplot:
			plot "clusters.tsv" using 1:2 title 'Cluster quality'
	
Tasks can depend on other tasks (e.g., ``extract_columns`` depends on
``download_data``) - either in the same pipeline or in other pipelines.  By
making tasks depend on other pipelines, it's possible to treat pipelines as
modular parts of much larger workflows.

Once a task completes without error, it is *marked* - which flags it as not
needing to be run again.  In order to re-run a task, one can simply unmark it
and run it again.

If you choose to run a task which has unmarked dependencies, these will be run
before the task itself is run - in this way, an entire workflow can be run
using a single command.

A task contains *blocks* which describe the actual computational steps being
taken. As is seen in the example above, blocks can contain code for various
different languages - making it possible to stitch together workflows that
involve different languages. A single task can even contain multiple blocks for
the same or different languages.

Currently, xp supports four block types:

  - *export* (``export``) - this allows environment variables to be set and 
  	unset within the context of a specific task

  - *python* (``code.py``)

  - *shell* (``code.sh``)

  * *gnuplot* (``code.gnuplot``)

These, of course, require that the appropriate executables are present on the
system. To customize the executable used, environment variables can be set
(``PYTHON_EXEC`` and ``GNUPLOT_EXEC``, respectively).

Future releases will support additional languages natively and also provide a
plugin mechanism for adding new block types. 

Once a pipeline has been written, it can be run using the xp command-line tool::

  xp run <pipeline_file>

The command-line tool also allows easy marking (``mark``), unmarking (``unmark``),
and querying task info (``tasks``) for a pipeline.

~~~~~~~~~~~~~~~~~~~~~~~~~
Pipeline-specific Data
~~~~~~~~~~~~~~~~~~~~~~~~~

A common activity that creates a lot of data management issues is running
effectively the same or similar pipelines using different parameter settings:
files can get overwritten and, more generally, the user typically loses track
of exactly which files came from what setting.

In xp, files produced by a pipeline can be easily bound to their pipeline,
eliminating this confusion::

	DATA_URL=http://foobar:8080/data.tsv
	ALPHA=2
	...
	
	download_data:
		code.sh:
			curl $DATA_URL > $PLN(data.tsv)
	
	...

In the excerpt above, the file ``data.tsv`` is being bound to this pipeline using
the ``$PLN(.)`` function. In effect, the file is prefixed (either by name or
placed in a pipeline-specific directory).  Future references to this file via
``$PLN(data.tsv)`` will access only this pipeline's version of the file - even if
many pipelines are downloading the files at various times.

~~~~~~~~~~~~~~~~~~~~
Extending Pipelines
~~~~~~~~~~~~~~~~~~~~

In some cases, one will want to run exactly the same pipeline over and over
with different parameter settings. To support this, xp allows *extending*
pipelines.  Much like subclassing, extending a pipeline brings all the content
of one pipeline into another one.  Assume we are clustering some data using the
process here (in pipeline ``cluster_pln``).  The process is parameterized by the
alpha value.

::

	# Pipeline: cluster_pln
	
	cluster_rows: extract_columns
		code.sh:
			./cluster.sh --alpha $ALPHA xdata2.tsv > $PLN(clusters.tsv)
	
	plot_clusters: cluster_rows
		code.gnuplot:
			plot "$PLN(clusters.tsv)" using 1:2 title 'Cluster quality at alpha=$ALPHA'

We can extend this pipeline to retain the same workflow, but use different values::

	# Pipeline: cluster_a2
	extend cluster_pln
	
	ALPHA=2

and again for a different value::

	# Pipeline: cluster_a3
	extend cluster_pln
	
	ALPHA=3

Note that in each case the cluster data will be stored to ``$PLN(clusters.tsv)``,
so that each pipeline will have its own separate stored data.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Connecting Pipelines Together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's quite reasonable to expect that one pipeline could feed into another
pipeline. xp supports this - pipelines can depend on the tasks in other
pipelines - and in doing so, create even larger workflows that retain their
nice modular organization.

Consider that the earlier pipeline given above, ``cluster_a2``, could actually be
assembling the data for a classifier. Let's break this classifier portion of
the project into its own workflow::

	# Pipeline: lda_classifier
	
	use cluster_a2 as cdata
	
	NEWS_ARTICLES=articles/*.gz
	
	build_lda: cdata.cluster_rows
		export:
			LDA_CLASSIFIER=lda_runner
	
		code.sh:
			${LDA_CLASSIFIER} -input $PLN(cdata,clusters.tsv) -output $PLN(lda_model.json)
	
	label_articles: build_lda
		export:
			LDA_LABELER=/opt/bin/lda_labeler
		code.sh:	
			${LDA_LABELER} -model $PLN(lda_model.json) -data "$NEWS_ARTICLES" > $PLN(news.labels)
	
In the example above, notice how the task ``build_lda`` both depends on a task
from the ``cluster_a2`` pipeline and *also* uses data from that pipeline's
namespace, ``$PLN(cdata,clusters.tsv)``.

Of course, we might want to try multiple classifiers on the same source data,
so we can create other pipelines that use ``cluster_a2``, shown next::

	# Pipeline: crf_classifier
	
	use cluster_a2 as cdata
	
	NEWS_ARTICLES=articles/*.gz
	
	build_crf_model: cdata.cluster_rows
		code.sh:
			/opt/bin/build_crf -data $PLN(cdata,clusters.tsv) -output $PLN(crf_model.json)
	
	label_articles: build_crf_model
		code.py:
			import crf_model
	
			model = crf_model.load_model('$PLN(crf_model.json)')
			model.label_documents(docs='$NEWS_ARTICLES',out_file='$PLN(news.labels)')

~~~~~~~~
Examples
~~~~~~~~

See the ``examples/`` directory in the xp root directory to see some real
pipelines that demonstrate the core features of the tool.

----------------------
Command-line usage
----------------------

The ``xp`` command provides several core capabilities:

  - ``xp tasks <pipeline>`` will out info about one or more tasks in the pipeline including whether they are marked

  - ``xp run <pipeline>`` will run a pipeline (or a task within a pipeline)

  - ``xp mark <pipeline>`` will mark specific tasks or an entire pipeline

  - ``xp unmark <pipeline>`` will unmark specific tasks or an entire pipeline

All of these commands have help messages to help their correct use.


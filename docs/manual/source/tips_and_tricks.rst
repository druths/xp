
.. toctree::
	:maxdepth: 2

***************
Tips and Tricks
***************

xp is a too young to have conventions, per say.  But there are some tips and
tricks that can be useful.

###############
Pipeline naming
###############

**Use nouns.** Name pipelines for the literal thing they're doing.  For
example, a pipeline that obtains and prepares data from the US census might be
called ``us_census_grabber``.

**No suffixes.** Like makefiles, pipelines should be named without a suffix.
Since the default namespace is based off of the pipeline's filename, this
avoids ugly file and directory names.

**Abstract pipelines.** Abstract pipelines should be named in such a way that
it is clear that they contain placeholders. If the pipeline is designed to
model a particular country, then the name might be ``XX_model_builder`` where
``XX`` is a stand-in for the country code (which will be specified in the
derived pipelines.

#########################
Extending pipelines
#########################

**When to extend.** When you have a certain kind of analysis that you'd like to
run on different datasets or using different parameter values, write an
abstract pipeline.

**Don't make extended pipelines functional.** In order to avoid confusing the
purpose of an abstract pipeline with those that actually do work, avoid running
a pipeline that will be extended.


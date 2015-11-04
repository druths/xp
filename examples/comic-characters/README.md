## Comic character gender disparities

In this example workflow we consider gender representations in comic books.
This is based on data collected for the fivetheirtyeight story [Comic Books Are
Still Made By Men, For Men And About
Men](http://fivethirtyeight.com/features/women-in-comic-books/).  We'll compare
the distributions of traits among male and female superheros.  The results are
surprising and not surprising at the very same time.

### Files

The entire project consists of four pipelines.

  * `downloader.fx` is responsible for downloading the data file from the fivethirtyeight github repository and liberating the data from the cursed CSV format.
  * `analyze_template.fx` is a pipeline that contains all the logic for performing analysis on a trait of interest. Pipelines for specific traits will extend this pipeline.
  * `analyze_eye_color.fx` extends the `analyze_template.fx` pipeline and looks at eye color.
  * `analyze_hair_color.fx` extends the `analyze_template.fx` pipeline and looks at hair color.
  * `analyze_align.fx` extends the `analyze_template.fx` pipeline and looks at the distribution of superheros who are good vs. bad.

### Setup

For this analysis to run, you'll need to be in a Unix (or cygwin) environment with the following installed:

  * standard unix command line tools (`cut`, `grep`, `tr`)
  * Python 2.7 or later
  * flex

### Running analyses

To run the eye color analysis, use `fx run analyze_eye_color`.  For other analyses, just swap in the other traits files.  Note that you can't run the `analyze_template.fx` pipeline ... well, you can, but it won't work.


# Download the relevant files for analysis

download_dc_data:
	code.sh:
		curl https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/dc-wikia-data.csv > $PLN(dc-wikia-data.csv)

download_marvel_data:
	code.sh:
		curl https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/marvel-wikia-data.csv > $PLN(marvel-wikia-data.csv)

prep_tsvs: download_dc_data download_marvel_data
	# convert to TSVs because the CSV format is evil
	code.py:
		import csv

		def convert_to_tsv(fname,out_fname):
			ofh = open(out_fname,'w')
			reader = csv.reader(open(fname,'rU'))
			riter = iter(reader)
			
			for data in riter:
				print >>ofh, '\\t'.join(data)

			ofh.close()

		convert_to_tsv('$PLN(dc-wikia-data.csv)','$PLN(dc-wikia-data.tsv)')
		convert_to_tsv('$PLN(marvel-wikia-data.csv)','$PLN(marvel-wikia-data.tsv)')


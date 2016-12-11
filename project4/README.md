1. Aditional Files

	Resources and Results folder can be downloaded respectively at:
	
	http://www.recod.ic.unicamp.br/~alberto/mo601-project4/resources.tar
	http://www.recod.ic.unicamp.br/~alberto/mo601-project4/results.tar
	
	- resources.tar contain additional files required to run the result
	generation scripts, such as imaps, automata, executable dumps and
	the lisc source code;
	
	- results.tar contain all the results file, some of which were not
	included in the report;
	
2. Scripts

	Scripts are available in the 'src' folder. The execution logs generated
	in the execution are in the resources package.

-- combine_imap.py --

		Combines .imap files into a single .imap
	
usage: combine_imap.py [-h] [-o OUTFILE]
                       input_imap_files [input_imap_files ...]

positional arguments:
  input_imap_files      Input .imap file list

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Combined .imap file name. Default is 'combined.imap'
						
	
-- run_disass.py --
	
		Disassemble programs, saving their unique instructions in a single .bin file.
		Uses the disass.sh script from the lisc package.
	
usage: run_disass.py [-h] [--outfile OUTFILE] [--execdir EXECDIR] dpath

positional arguments:
  dpath                 Disassembly script path (disass.sh)

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE, -o OUTFILE
                        Output file name. Default: outfile.bin
  --execdir EXECDIR, -e EXECDIR
                        Path with executables. If empty, gets all executables
                        from the system. Default is empty
			
			
-- run_disass_2.py --
	
		Disassemble programs, saving each disassembled program in its own .bin
		file. Uses the disass.sh script from the lisc package.
		
usage: run_disass_2.py [-h] [--outdir OUTDIR] [--execdir EXECDIR] dpath

positional arguments:
  dpath                 Disassembly script path (disass.sh)

optional arguments:
  -h, --help            show this help message and exit
  --outdir OUTDIR, -o OUTDIR
                        Output directory. Default: empty
  --execdir EXECDIR, -e EXECDIR
                        Path with executables. If empty, gets all executables
                        from the system. Default is empty

						
-- run_lisc.py --
	
		Runs lisc for a directory of disassembled programs (.bin extension)
						
usage: run_lisc.py [-h] [--outroot OUTROOT] [--log LOG] [--csv CSV]
                   liscdir automata execdumpdir

positional arguments:
  liscdir               directory containing lisc
  automata              Automata path
  execdumpdir           Path with executable dumps.

optional arguments:
  -h, --help            show this help message and exit
  --outroot OUTROOT, -o OUTROOT
                        Output root directory. Two folders will be created in
                        the root: log and res. Default is ./
  --log LOG, -l LOG     Run lisc log file. If empty, no log is created.
                        Default is empty
  --csv CSV, -c CSV     Run lisc csv file. Logs program size vs time to lift
                        If empty, no csv is created. Default is empty
						
						
-- run_parsing.py --

		Parses the resulting files from LISC, into a single .csv file

usage: run_parsing.py [-h] [--outfile OUTFILE] resdir

positional arguments:
  resdir                Directory containing result files

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE, -o OUTFILE
                        Output file name. Default is results.csv


-- plot_results_time.py --

		Plot time and size curves, given a timing .csv file (produced by run_lisc.py)

usage: plot_results_time.py [-h] csvfname outfprefix

positional arguments:
  csvfname    Input Csv file.
  outfprefix  Prefix to output file.

optional arguments:
  -h, --help  show this help message and exit


-- plot_results_automata_comparison.py --
  
		Plots automata size x time results, given a list of timing CSV files (produced by run_lisc.py)

usage: plot_results_automata_comparison.py [-h] [-p OUTPREFIX]
                                           csvfiles [csvfiles ...]

positional arguments:
  csvfiles              Input csv file list

optional arguments:
  -h, --help            show this help message and exit
  -p OUTPREFIX, --outprefix OUTPREFIX
                        Prefix to output file. Default is output.pdf
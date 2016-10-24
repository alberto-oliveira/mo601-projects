##### MO601 PROJECT 2 Source #####

1. Pintools-memory_stats_4kB_pages-linux64-amd64-gcc43+.cfg

This file is a modified Config file to run Pin tool in the
selected benchmark(s). The Pintool purpose is generating memory
statistics when 4k pages are used. It adds the following lines
to the config file:

use_submit_for_speed = yes

which allows the submission of a some bash lines before running the 
benchmark. And 

submit = <bash_lines> $command

which defines the desired lines to be submitted. In this project,
the submit command used was:

submit = /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/pin -t /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/source/tools/Memory/obj-intel64/memory_stats_4kB_pages.so -c /home/alberto/disciplinas/mo601/mo601-projects/project2/memory_stats_4kB_pages_csv/"$benchmark"_"$workload"_memory_stats_4kB_pages.csv -o /home/alberto/disciplinas/mo601/mo601-projects/project2/memory_stats_4kB_pages_pintool_out/"$benchmark"_"$workload"_memory_stats_4kB_pages.out  -b "$benchmark"_"$workload" -- $command

where:

- /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/pin is the local of pin;

- /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/source/tools/Memory/obj-intel64/memory_stats_4kB_pages.so 
  (defined by the parameter -t) is the location of the pintools file;
  
- /home/alberto/disciplinas/mo601/mo601-projects/project2/memory_stats_4kB_pages_csv/"$benchmark"_"$workload"_memory_stats_4kB_pages.csv
  (defined by the parameter -c) is the output csv file from pin;
  
- /home/alberto/disciplinas/mo601/mo601-projects/project2/memory_stats_4kB_pages_pintool_out/"$benchmark"_"$workload"_memory_stats_4kB_pages.out
  (defined by the parameter -o) is the output human readable file from pin;
  
- "$benchmark"_"$workload"
  (defined by the parameter -b) is the name to be used for this benchmark run;
  
The output file uses two variables defined in the config file: 
$benchmark and $workload. The first is the name of the benchmark being
run, and the second is the number of the workload being run as input
to the benchmark. An example output file is:

403.gcc_2_memory_stats_4kB_pages.csv

which is memory statistics for GCC, with input workload number 2 (c-typeck.in)

2. Pintools-memory_stats_4MB_pages-linux64-amd64-gcc43+.cfg

Same as the above, but for 4MB pages instead.


3. memory_stats_4kB_pages.cpp

Pintool to collect memory statistics from a program, when page size is 4kB.
Accepts the following parameters:

-c <output_csv_file_name>
-o <output_human_readable_file_name>
-b <benchmark_name>

4. memory_stats_4MB_pages.cpp

Same as the above, but for 4MB page size instead.

5. call_pin_benchmark_run.py start end configpath stdoutdir --print

Python script that runs the selected benchmarks sequentially. This scripts acceps four
positional arguments, and one optional argument:

    start: number between 0 and 28 of the starting benchmark to
           be run;
		  
    end: number (exclusive) between 1 and 29 of the ending benchmark
	     to be run;
		 
	configpath: path to the configuration file to be run with runspec;
	
	stdoutdir: stdout dir for runspec;
		 
	--print: print the number and name of each benchmark, and exit;
	
	
This script will always run the benchmark in the 'ref' dataset, with
one iteration and maximum verbosity. The script produces an stdout
file with name "output_<benchmark_name>.out", inside stdoutdir.

IMPORTANT: This script should be called from inside SPEC2006 installation
directory, and after running ". ./shrc" inside the same directory.

To run the script, Python 2.7 is required. The remaining packages used
'sys', 'argparse', and 'subprocess', are default from Python's install.
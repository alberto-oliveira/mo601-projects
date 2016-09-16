##### MO601 PROJECT 1 Source #####

1. Pintools-inscount-linux64-amd64-gcc43+.cfg

This file is a modified Config file to run Pintools inscount in the
selected benchmark(s). To do so, it adds two new lines:

use_submit_for_speed = yes

which allows the submission of a some bash lines before running the 
benchmark. And 

submit = <bash_lines> $command

which defines the desired lines to be submitted. In this project,
the submit command used was:

submit = /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/pin -t /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/source/tools/ManualExamples/obj-intel64/inscount0.so -o /home/alberto/disciplinas/mo601/mo601-projects/project1/inscount_out/"$benchmark"_"$workload"_inscount.out -- $command

where:

- /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/pin is the local of pin;
- /home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/source/tools/ManualExamples/obj-intel64/inscount0.so 
  is the location of the pintools file;
- /home/alberto/disciplinas/mo601/mo601-projects/project1/inscount_out/"$benchmark"_"$workload"_inscount.out 
  is the output file from pin;
  
The output file uses two variables defined in the config file: 
$benchmark and $workload. The first is the name of the benchmark being
run, and the second is the number of the workload being run as input
to the benchmark. An example output file is:

403.gcc_2_inscount.out

which is the instruction count for GCC, with input workload number 2 
(c-typeck.in)

2. call_benchmark_run.py start end --print

Python script that runs the selected benchmarks sequentially. This scripts acceps two
positional arguments, and one optional argument:

    start: number between 0 and 28 of the starting benchmark to
           be run;
		  
    end: number (exclusive) between 1 and 29 of the ending benchmark
	     to be run;
		 
	--print: print the number and name of each benchmark, and exit;
	
	
This script will always run the benchmark in the 'ref' dataset, with
one iteration and maximum verbosity. The script produces an stdout
file with name "output_<benchmark_name>.out". To modify the config file
path, the SPEC bin path, and the stdout dir, the variables 'runspec_list',
'runspec_dir', and 'stdout_dir' have to be modified inside the script.

To run the script, Python 2.7 is required. The remaining packages used
'sys', 'argparse', and 'subprocess', are default from Python's install.
path an
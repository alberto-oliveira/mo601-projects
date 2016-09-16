##### MO601 PROJECT 1 Source #####

1. Pintools-inscount-linux64-amd64-gcc43+.cfg

This file is a modified Config file to run Pin tool inscount in the
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


2. Pintools-branchcount-linux64-amd64-gcc43+.cfg

Similarly the aforementioned file, this one runs the custom Pin tool 
branchcount with the selected benchmark(s).

This file works exactly like the one for inscount, however, it 
produces the output file "$benchmark"_"$workload"_branchcount.out
instead.

3. branchcount.cpp

The custom Pin tool developed for this project that performs
branc counting. It can be compiled by running the make command
inside the pin-3.0-76991-gcc-linux/source/tools/ManualExamples/
directory.


2. call_pin_benchmark_run.py start end configpath stdoutdir --print

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
path an
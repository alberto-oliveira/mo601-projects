Infrastructure: PIN, and 10 benchmarks

Task:

Evaluate Virtual to Physical memory translation for 4KB and 4MB pages.
Consider up to 512 entries TLB for instruction and data.
Consider 3 or 4 levels page table.
Look for benchmarks with large memory footprint.
Create one toy benchmark to check your environment.
Report:

Create a folder called project1 in your repository
Due to 20/Oct (end of the day)
Report document. SBC Template. You can choose either English or Portuguese for your report. Maximum of 6 pages containing the count (item 3 above) and the description and result of your pintool. Filename: report.pdf
Presentation Document. Create a file called presentation.pdf containing slides for a 5 minutes presentation of your project.
CSV file. Include a file results.csv containing your results. For each benchmark, include the following columns: benchmark name (nd input if necessary), total memory access for instructions, total TLB misses for instructions, total page table access for instructions, total memory access for data, total TLB misses for data, total page table access for data.
Source code. Include your source code in the folder src. This folder should contain all code that you created/modified together with scripts to execute and a README.md file explaining dependencies. Your script could rely on environment variables for pre-requisites.
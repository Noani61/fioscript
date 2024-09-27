
# Description
This is a FIO benchmark scripts. Using this you can generate
datasets and plots regarding device IOPS, Throughput and Latency.

# Dependencies
Make sure you have:
- FIO
- Python 3+ (with matplotlib and numpy)

# Run scripts manually
To run FIO on a device manually use the runfio.py script:
```
Usage:
      python3 runfio.py -d <device> -n <njobs> -i <iodepth> -f <script> -o <output-dir> [-h]

options:
  -h, --help       show this help message and exit
  -d DEVICE        Block device to test
  -s SIZE          How much data are we going to be reading/writing.
  -b BENCHMARK     Benchmark file name from /script_configs
  -i IODEPTH       Number of outstanding I/Os (iodepth)
  -n NJOBS         Number of FIO processes/threads (numjobs)
  -t TIME          Limit runtime. The test will run until it completes the configured I/O workload or until it has run for this specified amount of time, whichever occurs first.
  -o OUTPUT        Output directory. By default /output
  --rwm RWMIXREAD  Percentage of a mixed workload that should be reads. The remaining percentage up to 100 will be given to writing

```
An example run is the following:
```bash
runfio.py -d sda -b rand-RW.fio -t 30 --rwm 50
```
This configuration will run with a variety of different block sizes by default.
Apart from the output produced for each block size, in the end we will have a
csv type file with name "out.txt" holding the throughput achieved for each
block size.

In order to create a plot from the output, you can use the plotfio.py script:

```
Usage:
       plotfio.py [ -h ]
                    -f FILES      [FILES ... ]
                    -l LABELS    [LABELS ... ]
                    -o OUTPUTFOLDER
                    -n NAME
                    -t TITLE

Options:
       -h, --help                Show this help message and exit
       -f FILES     [FILES ...]  The out.txt files
       -l LABELS   [LABELS ...]  Label for each curve
       -o OUTPUTFOLDER           Ouput folder
       -n NAME                   Name of output plot
       -t TITLE                  Title of output plot
```
An example run is the following:
```bash
plotfio.py -f output/27-09-2024_18:20:21/rand-RW.fio_sda_16iodepth_1threads_50r_50w/read.csv  \
              output/27-09-2024_18:20:21/rand-RW.fio_sda_16iodepth_1threads_50r_50w/write.csv \
           -l "rand-RW-read" "rand-RW-write"                                                  \                                                      \
           -o "plotout"                                                               \
           -n "rand-RW"                                                                    \
           -t "Random read and write in RW"
```



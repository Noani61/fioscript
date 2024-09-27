#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess

if __name__ == '__main__':

    block_sizes = ( 4, 8, 16, 32, 64, 128, 256, 512, 1024 )

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="device", required=True, type=str, help="Block device to test")
    parser.add_argument("-s", dest="size", default='80%', type=str, help="How much data are we going to be reading/writing.")
    parser.add_argument("-b", dest="benchmark", required=True, type=str, help="Benchmark file name from /script_configs")
    parser.add_argument("-i", dest="iodepth", default=16, type=int, help="Number of outstanding I/Os (iodepth)")
    parser.add_argument("-n", dest="njobs", default=1, type=int, help="Number of FIO processes/threads (numjobs)")
    parser.add_argument("-t", dest="time", required=True, type=int, help="Limit runtime. The test will run until it completes the configured I/O workload or until it has run for this specified amount of time, whichever occurs first.")
    parser.add_argument("-o", dest="output", default="output", help="Output directory. By default /output")
    parser.add_argument("--rwm", dest="rwmixread", default=50, type=int, help="Percentage of a mixed workload that should be reads. The remaining percentage up to 100 will be given to writing")
    args = parser.parse_args()

    current_time = subprocess.getoutput("date +%d-%m-%Y_%H:%M:%S")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    test_case = f"{args.benchmark}_{args.device}_{args.iodepth}iodepth_{args.njobs}threads_{args.rwmixread}r_{100-args.rwmixread}w"
    output_directory = os.path.join(script_directory, args.output, current_time, test_case)
    config_directory = f"{script_directory}/script_configs/{args.benchmark}"

    block_device_path = f"/dev/{args.device}"
    if not os.path.exists(block_device_path):
        print(f"ERROR: Block device {block_device_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    if os.system(f"mount | grep -q '{block_device_path}'") == 0:
        print(f"ERROR: Block device {args.device} is in use. Use another one.")
        sys.exit(1)
    if not os.path.isfile(f"{config_directory}"):
        print(f"ERROR: Benchmark {args.benchmark} does not exist.", file=sys.stderr)

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    print("\n" + "=" * 72 + "\n")
    print(f"Starting run with: {config_directory}")
    print()
    print(f"    Device:  {args.device}")
    print(f"    IODEPTH: {args.iodepth}")
    print(f"    NUMJOBS: {args.njobs}")
    print()
    print("     Block Size: ")

    start_time = int(subprocess.getoutput("date +%s"))

    for bs in block_sizes:
        if int(subprocess.getoutput(f"cat /sys/block/{args.device}/queue/rotational")) == 0:
            subprocess.run(f"sudo blkdiscard /dev/{args.device}", shell=True)

        print(f"{bs}KB ")
        subprocess.run(
            f"sudo SIZE='{args.size}' BLOCK_SIZE='{bs}k' DEVICE='{args.device}' RWM='{args.rwmixread}' "
            f"IODEPTH='{args.iodepth}' NUMJOBS='{args.njobs}' RUNTIME='{args.time}' "
            f"fio --output-format=json '{config_directory}' >> '{output_directory}/{bs}.json'",
            shell=True
        )

    print()
    end_time = int(subprocess.getoutput("date +%s"))
    elapsed_time = end_time - start_time
    formatted_time = f"{elapsed_time // 3600}h:{(elapsed_time % 3600) // 60}m:{elapsed_time % 60}s"

    print(f"\n    Benchmark time elapsed: {formatted_time}\n")
    print("=" * 72 + "\n")

    subprocess.run(["python3", "parser.py", output_directory] + [str(bs) for bs in block_sizes])
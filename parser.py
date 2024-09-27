import os
import json
import csv
import sys

def main(directory, block_sizes):

    read_file_path = os.path.join(directory, "read.csv")
    write_file_path = os.path.join(directory, "write.csv")

    with open(read_file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Block size (KB)", "IOPS", "Throughput (MB/s)", "Latency (us)"])

        for bs in block_sizes:
            with open(os.path.join(directory, f"{bs}.json"), 'r') as file:
                data = json.load(file)
            if data['jobs'][0]['job options']['rwmixread'] != 0:
                iops_avg = data['jobs'][0]['read']['iops']
                bw_avg_kb = data['jobs'][0]['read']['bw']
                lat_avg_ns = data['jobs'][0]['read']['lat_ns']['mean']
                def format_iops(iops):
                    return f"{int(iops)}"
                def format_bw(bw_kb):
                    return f"{int(bw_kb // 1000)}"
                def format_lat(lat):
                    return f"{int(lat // 1000)}"
                iops = format_iops(iops_avg)
                bw_avg_mb = format_bw(bw_avg_kb)
                lat_avg_us = format_lat(lat_avg_ns)

            writer.writerow([bs, iops, bw_avg_mb, lat_avg_us])

    with open(write_file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Block size (KB)", "IOPS", "Throughput (MB/s)", "Latency (us)"])

        for bs in block_sizes:
            with open(os.path.join(directory, f"{bs}.json"), 'r') as file:
                data = json.load(file)
            if data['jobs'][0]['job options']['rwmixread'] != 100:
                iops_avg = data['jobs'][0]['write']['iops']
                bw_avg_kb = data['jobs'][0]['write']['bw']
                lat_avg_ns = data['jobs'][0]['write']['lat_ns']['mean']
                def format_iops(iops):
                    return f"{int(iops)}"
                def format_bw(bw_kb):
                    return f"{int(bw_kb // 1000)}"
                def format_lat(lat):
                    return f"{int(lat // 1000)}"
                iops = format_iops(iops_avg)
                bw_avg_mb = format_bw(bw_avg_kb)
                lat_avg_us = format_lat(lat_avg_ns)

            writer.writerow([bs, iops, bw_avg_mb, lat_avg_us])

if __name__ == "__main__":
    directory = sys.argv[1]
    block_sizes = [int(size) for size in sys.argv[2:]]

    main(directory, block_sizes)
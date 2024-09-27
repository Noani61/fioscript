#!/usr/bin/env python3


import numpy as np
import csv, argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="files", type=str, nargs='+', required=True, help='The write/read.csv files')
    parser.add_argument('-l', dest="labels", type=str, nargs='+', required=True, help='Label for each curve')
    parser.add_argument('-o', dest="outputfolder", required=True, help="Output folder")
    parser.add_argument('-n', dest="name", required=True, help="Name of output plot")
    parser.add_argument('-t', dest="title", required=True, help="Title of output plot")
    args = parser.parse_args()

    xlabel = 'Block Size (KB)'
    max_rows = 9

    def iops():
        import matplotlib.pyplot as plt
        ylabel = 'IOPS'
        index = 0
        for f in args.files:
            with open(f, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)

                x, y = [0], [0]
                for i, row in enumerate(reader):
                    if i >= max_rows:
                        break
                    x.append(int(row[0]))
                    y.append(float(row[1]))

            n = len(x)
            x2 = np.arange(n)

            plt.plot(x2, y, label=args.labels[index])

            plt.xticks(x2, x, rotation=90)

            index += 1

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xlim(left=0)
        plt.ylim(bottom=0)

        plt.title(args.title)
        plt.legend()

        plt.tight_layout()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        plt.savefig(f"{script_directory}/{args.outputfolder}/{args.name}_iops.png", format="png")
        plt.clf()

    def throughput():
        import matplotlib.pyplot as plt
        ylabel = 'Throughput (MB/s)'
        index = 0
        for f in args.files:
            with open(f, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)

                x, y = [0], [0]
                for i, row in enumerate(reader):
                    if i >= max_rows:
                        break
                    x.append(int(row[0]))
                    y.append(float(row[2]))

            n = len(x)
            x2 = np.arange(n)

            plt.plot(x2, y, label=args.labels[index])

            plt.xticks(x2, x, rotation=90)

            index += 1

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xlim(left=0)
        plt.ylim(bottom=0)

        plt.title(args.title)
        plt.legend()

        plt.tight_layout()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        plt.savefig(f"{script_directory}/{args.outputfolder}/{args.name}_throughput.png", format="png")
        plt.clf()

    def latency():
        import matplotlib.pyplot as plt
        ylabel = 'Latency (us)'
        index = 0
        for f in args.files:
            with open(f, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)

                x, y = [0], [0]
                for i, row in enumerate(reader):
                    if i >= max_rows:
                        break
                    x.append(int(row[0]))
                    y.append(float(row[3]))

            n = len(x)
            x2 = np.arange(n)

            plt.plot(x2, y, label=args.labels[index])

            plt.xticks(x2, x, rotation=90)

            index += 1

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xlim(left=0)
        plt.ylim(bottom=0)

        plt.title(args.title)
        plt.legend()

        plt.tight_layout()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        plt.savefig(f"{script_directory}/{args.outputfolder}/{args.name}_latency.png", format="png")
        plt.clf()

    iops()
    throughput()
    latency()
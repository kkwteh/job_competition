#!/Users/teh/code/kaggle/ENV/bin/python

"""
This script takes a data file and samples several rows without replacement and places it into a new file. The first row is always kept, in case it is a header

An example usage is ./parefile --percent 0.1 foo.csv
The smaller file will be named mini_foo.csv
"""

import random
import sys

def pare_file(data_file, percent):
    """
    This method does the paring.
    Args:
    data_file: name of the file to be pared down
    percent: percentage of rows to sample (roughly)
    """

    mini_data_file = "mini_" + data_file
    with open(data_file, 'r') as f:
        with open(mini_data_file, 'wb') as g:
            line = f.readline()
            g.write(line)
            for line in f.xreadlines():
                if random.random() < percent:
                    g.write(line)

def main():
    """
    Standard main function boilerplate to accept command line arguments
    """
    args = sys.argv[1:]

    if not args:
        print 'usage: [--percent percent] datafile '
        sys.exit(1)

    percent = 0.1
    if args[0] == '--percent':
        percent = float(args[1])
        del args[0:2]

    data_file = args[0]

    pare_file(data_file, percent)

if __name__ == '__main__':
    main()

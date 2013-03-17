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
    This method pares down the file, keeping the header and writes the result
    to "mini_" + data_file.
    Args:
    data_file: name of the file to be pared down
    percent: percentage of rows to sample (roughly)
    """

    mini_data_file = "mini_" + data_file
    with open(data_file, 'rb') as f:
        with open(mini_data_file, 'wb') as g:
            line = f.readline()
            g.write(line)
            for line in f.xreadlines():
                if random.random() < percent:
                    g.write(line)

def split_file(data_file, percent=0.1):
    """This method splits the data file into two pieces, a training set,
    and a validation set, keeping the header. The training set is written to
    "train_part_" + data_file and the validation set is written to
    "validation_part_" + data_file
    Args:
    data_file: name of the file
    percent: approximate percent of file to be written to validation set.
    """
    train_data_file =  "train_part_" + data_file
    validation_data_file = "validation_part_" + data_file
    with open(data_file, 'rb') as f:
        with open(train_data_file, 'wb') as g:
            with open(validation_data_file, 'wb') as h:
                line = f.readline()
                g.write(line)
                h.write(line)
                for line in f.xreadlines():
                    if random.random() > percent:
                        g.write(line)
                    else:
                        h.write(line)
def main():
    """
    Standard main function boilerplate to accept command line arguments and runs
    pare_file method
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

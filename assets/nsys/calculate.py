#!/usr/bin/env python

import pandas as pd
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--flag', type=str, help='The flag for display.')
parser.add_argument('--csv_path', type=str, help='The path of the csv file.')
parser.add_argument('--num_batch', type=int, help='The num of batches.')
args = parser.parse_args()

data = pd.read_csv(args.csv_path, sep=',')[r'Total Time (ns)']
# ns --> ms
res = "{}, {}\n".format(args.flag, data.sum() / 1e6 / args.num_batch)
print(res)


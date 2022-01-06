#!/usr/bin/env python

import pandas as pd
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--flag', type=str, help='The flag for display.')
parser.add_argument('--csv_path', type=str, help='The path of the csv file.')
parser.add_argument('--save_file', type=str, help='The file used to save the processed result.')
args = parser.parse_args()

data = pd.read_csv(args.csv_path, sep=',')[r'Total Time (ns)']
# ns --> ms
res = "{}, {}\n".format(args.flag, data.sum() / 1e6 / 20.)
print(res)

with open(args.save_file, 'a') as f:
    f.write(res)

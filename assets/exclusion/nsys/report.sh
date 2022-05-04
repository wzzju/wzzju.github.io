#!/bin/bash

# Refer to https://developer.download.nvidia.cn/compute/DCGM/docs/nvidia-smi-367.38.pdf
# nvidia-smi --id=5 --query-compute-apps=used_memory --format=csv -lms 100
# nvidia-smi --id=3 --query-gpu=utilization.gpu --format=csv,nounits --loop-ms=100 --filename=utilization.csv

profile_name=${1:-'./perf_profile/laplace2d_static_0412_cinn_10layers.nsys-rep'}
# gpukernsum / gpumemtimesum / gpumemsizesum / gpusum / cudaapitrace / gputrace
target=${2:-'gpukernsum'}
# Refer to https://docs.nvidia.com/nsight-systems/UserGuide/index.html

# Extract file information, refer to https://blog.csdn.net/ljianhui/article/details/43128465
# prefix_path=${profile_name%/*}
prefix_path=$(dirname $profile_name)
# echo $prefix_path

ext=${profile_name##*.}
# echo $ext

file_name=$(basename $profile_name ".$ext")
# echo $file_name

# generate the gpukernsum.csv file
# nsys stats --report gputrace --report gpukernsum --report cudaapisum --format csv,column --output .,- ${profile_name}
nsys stats --report ${target} --report cudaapisum --format csv,column --force-overwrite true --force-export true --output .,- ${profile_name}

csv_name=${profile_name%.*}_${target}.csv
# echo $csv_name

# calculate the tatal gpu kernel time
python calculate.py --flag ${target} --csv_path ${csv_name} --num_batch 10


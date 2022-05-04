#!/bin/bash -ex

SAVE_FILE=xla_pass_${1:-'unspecified'}.csv
PROFILE_NAME=`pwd`/perf_profile/resnet50_graph_test_${1:-'unspecified'}
GPU_ID=${2:-'4'}
FLAG=${3:-'DIS_None'}

# export NVIDIA_TF32_OVERRIDE=0

# generate the nsys-rep file
CUDA_VISIBLE_DEVICES=${GPU_ID} TF_XLA_FLAGS=--tf_xla_auto_jit=2 \
        nsys profile --stats=false -t cuda,nvtx,osrt,cudnn,cublas -o ${PROFILE_NAME} --force-overwrite=true --capture-range=cudaProfilerApi --capture-range-end=stop \
        python resnet50_graph_test.py --benchmarks=.

# generate the gpukernsum.csv file
# nsys stats --report gputrace --report gpukernsum --report cudaapisum --format csv,column --output .,- report1.nsys-rep
nsys stats --report gpukernsum --format csv,column --force-overwrite true --force-export true --output .,- ${PROFILE_NAME}.nsys-rep

# calculate the tatal gpu kernel time
CSV_NAME=${PROFILE_NAME}_gpukernsum.csv
python cal_gpu_total.py --flag ${FLAG} --csv_path ${CSV_NAME} --save_file=${SAVE_FILE}

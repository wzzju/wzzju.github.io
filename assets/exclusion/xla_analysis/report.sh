#!/bin/bash

SAVE_FILE=xla_pass_${1:-'unspecified'}.csv
GPU_ID=${2:-'4'}

PASS_STR="AlgebraicSimplifier,AllGatherBroadcastReorder,AllGatherCombiner,AllReduceCombiner,AllReduceFolder,AllReduceReassociate,AllToAllDecomposer,BFloat16Normalization,BatchNormExpander,BitcastDtypesExpander,CallInliner,CollectivesScheduleLinearizer,ComparisonExpander,ConditionalCanonicalizer,ConditionalSimplifier,Convolution4DExpander,CublasPadForGemms,CudnnFusedConvRewriter,CudnnPadForConvolutions,CudnnVectorizeConvolutions,DotDecomposer,DotMerger,DynamicDimensionSimplifier,DynamicIndexSplitter,DynamicPadder,EighExpander,FlattenCallGraph,FusionBitcastLift,FusionMerger,GatherExpander,GemmAlgorithmPicker,GemmBroadcastFoldingRewriter,GemmRewriter,GpuConvAlgorithmPicker,GpuConvPaddingLegalization,GpuConvRewriter,GpuHorizontalInputFusion,GpuHorizontalLoopFusion,GpuInstructionFusion,GpuLayoutAssignment,GpuMultiOutputFusion,GpuScatterExpander,GpuTreeReductionRewriter,GpusolverRewriter,HloCSE,HloConstantFolding,HloDCE,HloVerifier,LogisticExpander,OperandUpcaster,QrExpander,RealImagExpander,ReduceScatterCombiner,ReduceScatterCreator,ReductionDegenerateDimRemover,ReductionDimensionGrouper,ReductionLayoutNormalizer,ReductionSplitter,ReshapeMover,ResultCaster,RngBitGeneratorExpander,RngExpander,ScatterExpander,SortSimplifier,StableSortExpander,TransposeFolding,TupleSimplifier,VariadicOpSplitter,WhileLoopConstantSinking,WhileLoopSimplifier,WhileLoopTripCountAnnotator,ZeroSizedHloElimination"

PASSES=(${PASS_STR//,/ })

echo "-- Total passes: ${PASS_STR}."
echo "-- The length of total passes: ${#PASSES[@]}."
echo "-------------------------------------------------------------------------------------"

for p in ${PASSES[@]};
do
    PROFILE_NAME=`pwd`/perf_profile/resnet50_graph_test_dis_$p
    FLAG="DIS_$p"
    ENV_PASSES=${PASS_STR//$p,/}
    ENV_PASSES=${ENV_PASSES//,$p/}
    echo "-- Disable ${p}, and the used passes: ${ENV_PASSES}."
    # generate the nsys-rep file
    CUDA_VISIBLE_DEVICES=${GPU_ID} USED_XLA_PASSES=${ENV_PASSES} TF_XLA_FLAGS=--tf_xla_auto_jit=2 \
            nsys profile --stats=false -t cuda,nvtx,osrt,cudnn,cublas -o ${PROFILE_NAME} --force-overwrite=true --capture-range=cudaProfilerApi --capture-range-end=stop \
            python resnet50_graph_test.py --benchmarks=.
    
    # generate the gpukernsum.csv file
    # nsys stats --report gputrace --report gpukernsum --report cudaapisum --format csv,column --output .,- report1.nsys-rep
    nsys stats --report gpukernsum --format csv,column --force-overwrite true --force-export true --output .,- ${PROFILE_NAME}.nsys-rep
    
    # calculate the tatal gpu kernel time
    CSV_NAME=${PROFILE_NAME}_gpukernsum.csv
    python cal_gpu_total.py --flag ${FLAG} --csv_path ${CSV_NAME} --save_file=${SAVE_FILE}
    echo "-------------------------------------------------------------------------------------"
done

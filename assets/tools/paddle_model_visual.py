#!/usr/bin/env python

import paddle.fluid as fluid
from paddle.fluid import core
from paddle.fluid.framework import IrGraph
import subprocess
import os
import argparse

def get_graph(program_path):
    with open(program_path, 'rb') as f:
        binary_str = f.read()
    program = fluid.framework.Program.parse_from_string(binary_str)
    return IrGraph(core.Graph(program.desc), for_test=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Paddle Model Visual Tool.")
    parser.add_argument("-p", "--path", default="mobilenetv1/__model__", type=str, help="model path")
    parser.add_argument("-n", "--name", default="mobilenetv1", type=str, help="visual graph name")
    args = parser.parse_args()

    # visualize the saved program
    program_path = args.path
    offline_graph = get_graph(program_path)
    marked_nodes = set()
    for op in offline_graph.all_op_nodes():
        if op.name().find('mul') > -1:
            marked_nodes.add(op)
    offline_graph.draw('.', args.name, marked_nodes)

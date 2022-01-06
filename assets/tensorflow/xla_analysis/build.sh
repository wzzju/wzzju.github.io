#!/bin/bash -ex

export CUDA_VISIBLE_DEVICES=1,2,3,4

# bazel build --config=cuda --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0" -c dbg //tensorflow/tools/pip_package:build_pip_package
# bazel build -c opt --config=cuda --copt="-g" --cxxopt="-g" --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0" --verbose_failures //tensorflow/tools/pip_package:build_pip_package
bazel build --config=opt --config=cuda --verbose_failures //tensorflow/tools/pip_package:build_pip_package

# ./bazel-bin/tensorflow/tools/pip_package/build_pip_package ./tensorflow_pkg # release branch
./bazel-bin/tensorflow/tools/pip_package/build_pip_package --nightly_flag ./tensorflow_pkg # master branch

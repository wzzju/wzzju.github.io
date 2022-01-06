#!/bin/bash -ex

pip uninstall tf-nightly  # remove current version

pip install ./tensorflow_pkg/tf_nightly-2.8.0-cp38-cp38-linux_x86_64.whl 
cd /tmp  # don't import from source directory
python -c "import tensorflow as tf; print(\"Num GPUs Available: \", len(tf.config.list_physical_devices('GPU')))"

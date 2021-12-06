# Copyright (c) 2021 Zhen Wang. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Please use jupyter notebook to execute this python file.

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
sns.set(rc={'figure.figsize': (16, 9)})

# required by jupyter notebook
%matplotlib inline


# get data for a log file
def process_data(file_name,
                 anchor_word="train step:",
                 key_word_begin="loss:",
                 key_word_end="top1:"):
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            conds = {
                re.search(anchor_word, line), re.search(key_word_begin, line),
                re.search(key_word_end, line)
            }
            if None not in conds:
                values = re.split(key_word_begin, line.strip())
                if len(values) > 1:
                    loss = re.split(key_word_end, values[1].strip())[0].strip()
                    data.append(float(loss))
    return data


# draw comparision line by using processed data
def compare(cinn_data,
            paddle_data,
            compare_label='loss',
            print_step=10,
            xlabel_key="batch"):
    fig = plt.figure(num=1, figsize=(15, 8), dpi=80)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(
        np.arange(0, len(cinn_data) * print_step, print_step),
        cinn_data,
        color='r',
        label='cinn train {}'.format(compare_label))
    ax1.plot(
        np.arange(0, len(paddle_data) * print_step, print_step),
        paddle_data,
        color='g',
        label='paddle train {}'.format(compare_label))

    plt.xlabel('{} ID'.format(xlabel_key.capitalize()))
    plt.ylabel('{} Value'.format(compare_label.capitalize()))
    plt.title("{} Comparison Line".format(compare_label.capitalize()))
    plt.legend()
    plt.show()


# enable nine ops: conv2d;conv2d_grad;batch_norm;batch_norm_grad;
# elementwise_add;elementwise_add_grad;relu;relu_grad;sum
log_dir = "/Path/To/Your/LogDir"

# draw train loss
train_cinn_loss_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"))
train_paddle_loss_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"))
compare(train_cinn_loss_data, train_paddle_loss_data, compare_label='train loss')

# draw train top1
train_cinn_top1_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"),
    key_word_begin="top1:",
    key_word_end="top5:")
train_paddle_top1_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"),
    key_word_begin="top1:",
    key_word_end="top5:")
compare(train_cinn_top1_data, train_paddle_top1_data, compare_label='train top1')

# draw train top5
train_cinn_top5_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"),
    key_word_begin="top5:",
    key_word_end="batch_cost:")
train_paddle_top5_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"),
    key_word_begin="top5:",
    key_word_end="batch_cost:")
compare(train_cinn_top5_data, train_paddle_top5_data, compare_label='train top5')

# draw train avg loss
train_cinn_loss_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin=r'train +loss:',
    key_word_end="top1:")
train_paddle_loss_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin=r'train +loss:',
    key_word_end="top1:")
compare(
    train_cinn_loss_data,
    train_paddle_loss_data,
    compare_label='avg loss',
    print_step=1,
    xlabel_key='epoch')

# draw train avg top1
train_cinn_top1_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin="top1:",
    key_word_end="top5:")
train_paddle_top1_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin="top1:",
    key_word_end="top5:")
compare(
    train_cinn_top1_data,
    train_paddle_top1_data,
    compare_label='avg top1',
    print_step=1,
    xlabel_key='epoch')

# draw train avg top5
train_cinn_top5_data = process_data(
    os.path.join(log_dir, "log_cinn_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin="top5:",
    key_word_end="batch_cost:")
train_paddle_top5_data = process_data(
    os.path.join(log_dir, "log_pd_loss_256.txt"),
    anchor_word="END epoch:",
    key_word_begin="top5:",
    key_word_end="batch_cost:")
compare(
    train_cinn_top5_data,
    train_paddle_top5_data,
    compare_label='avg top5',
    print_step=1,
    xlabel_key='epoch')

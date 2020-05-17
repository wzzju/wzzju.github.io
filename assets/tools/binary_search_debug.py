# -*- coding: utf-8 -*-

import os
import sys
import subprocess

# Run: nohup python -u binary_search_debug.py >log_0515.txt 2>&1 &

def compile(commit):
    cmake = 'cmake .. -DPY_VERSION=3.7 -DWITH_GPU=ON -DWITH_DISTRIBUTE=OFF -DWITH_TESTING=OFF -DWITH_INFERENCE_API_TEST=OFF -DON_INFER=OFF -DCMAKE_BUILD_TYPE=Release'
    command = 'git reset --hard %s' % commit
    os.system(command)
    build = os.path.join(os.getcwd(), 'build_%s' % commit)
    print(build)
    if not os.path.exists(build):
        os.system("mkdir %s" % build)
    sys.stdout.write("-----------------------------Compile and Install Commit ID: -----------------------------\n".format(commit))
    sys.stdout.flush()
    start_cmd= 'cd %s && %s && make -j' %(build, cmake)
    print(start_cmd)
    repeat_cmd= 'cd %s && make -j' % build
    print(repeat_cmd)
    rc = os.system(start_cmd)
    while rc != 0:
        sys.stdout.write("-----------------------------Repeat to make-----------------------------\n".format(commit))
        sys.stdout.flush()
        rc = os.system(repeat_cmd)

    install_cmd = 'cd %s && pip install -U python/dist/paddlepaddle_gpu-0.0.0-cp37-cp37m-linux_x86_64.whl' % build
    rc = os.system(install_cmd)
    while rc != 0:
        sys.stdout.write("-----------------------------Repeat to install-----------------------------\n".format(commit))
        sys.stdout.flush()
        rc = os.system(install_cmd)

def is_bad_version(commit):
    print("process the commit: {}".format(commit))
    compile(commit)
    cmd = "sh /work/Develop/sync_work/models/PaddleCV/image_classification/scripts/train/ResNet50_fp16_s.sh"
    print(cmd)
    with open("fp16_log_{}.txt".format(commit), "w") as log:
        child = subprocess.Popen(cmd.split(), stdout=log, stderr=log)
        child.communicate()
        rc = child.returncode
        print(commit, rc)
        if rc == 0:
            return False
        else:
            return True

def get_candidates(start, end):
    cmd = 'git log --pretty=oneline --after="{}" --before="{}"'.format(start, end)
    p = os.popen(cmd)
    text = p.read()
    commits = []
    with open("commits_info.txt", "w") as f:
        for line in text.splitlines():
            if line:
                cmt = line.split()[0]
                commits.append(cmt)
                f.write(cmt + "\n")
    p.close()
    commits.reverse()
    return commits

def binary_search(candidates, cond):
    with open("process_log.txt", "w") as f:
        f.write("-------------------------Record Process-------------------------\n")
        f.flush()
        left, right = 0, len(candidates) - 1
        while left + 1 < right:
            mid = (left + right) // 2
            commit = candidates[mid]
            if cond(commit):
                f.write("The commit {} is failed.\n".format(commit))
                f.flush()
                right = mid
            else:
                f.write("The commit {} is passed.\n".format(commit))
                f.flush()
                left = mid

        if cond(candidates[left]):
            return left
        if cond(candidates[right]):
            return right
        return -1

def init_start(commit):
    command = 'git reset --hard %s' % commit
    os.system(command)

if __name__ == "__main__":
    # 每次运行脚本须确保commit id起点不变，因为脚本运行过程中会reset commit id
    init_start("853f2e5272ce3a52cf96c818d64c8274307be8d0")
    # 设置问题pr大致出现的时间段
    candidates = get_candidates(start="2020-02-20 5:00:00",
                                end="2020-03-18 23:59:59")
    index = binary_search(candidates, is_bad_version)

    assert index != -1, "Not find any bad version."

    with open("process_log.txt", "a") as f:
        f.write("----------------------------------------------------------------\n")
        f.write("Find the target commit index = {}.\n".format(index))
        f.write("Find the target commit = {}.\n".format(candidates[index]))
        f.flush()

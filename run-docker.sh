#!/usr/bin/env bash

# 1. For x86:
# `docker pull grahamc/jekyll`
#
# 2. For Apple Silicon:
# - `docker build -t wzzju/jekyll:latest -f docker/Dockerfile .`
# - `docker pull wzzju/jekyll:latest`
#
# 3. For Windows:
# docker run --rm --interactive -v %cd%:/src -p 4000:4000 -e MENTOS_TIMEOUT=500000 grahamc/jekyll serve --host 0.0.0.0 --watch --incremental
# Use `http://localhost:4000` to access the blog website.

if [ "$(uname -m)" == "arm64" ];then
    docker run --rm --interactive -v $(pwd):/src -w /src -p 4000:4000 -e MENTOS_TIMEOUT=500000 wzzju/jekyll:latest jekyll serve --host 0.0.0.0 --watch --incremental
else
    docker run --rm --interactive -v $(pwd):/src -p 4000:4000 -e MENTOS_TIMEOUT=500000 grahamc/jekyll serve --host 0.0.0.0 --watch --incremental
fi

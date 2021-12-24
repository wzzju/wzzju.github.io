#!/usr/bin/env bash

# 1. For x86:
# `docker pull grahamc/jekyll`
#
# 2. For Apple Silicon:
# 1) `docker pull osvik/jekyll-apple-silicon:v4.2.0.b2`
# 2) Enter docker: `gem install github-pages`
# 3) Use `docker commit` to save changes to osvik/jekyll-apple-silicon:v4.2.0.b2

if [ "$(uname -m)" == "arm64" ];then
    docker run --rm --interactive -v $(pwd):/src -w /src -p 4000:4000 -e MENTOS_TIMEOUT=500000 osvik/jekyll-apple-silicon:v4.2.0.b2 jekyll serve --host 0.0.0.0 --watch --incremental
else
    docker run --rm --interactive -v $(pwd):/src -p 4000:4000 -e MENTOS_TIMEOUT=500000 grahamc/jekyll serve --host 0.0.0.0 --watch --incremental
fi

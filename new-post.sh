#!/usr/bin/env bash

# ----------------------------------------------------
# Template blog post setup script
#
# Creates a new template markdown file for yuchen's blog and opens the file automatically in
# vim.
# ---------------------------------------------------

DATE_SLUG=$(date +%Y-%m-%d)
TITLE=$(echo "$@" | tr -s '[:space:]' '\n' | tr '[:upper:]' '[:lower:]' | paste -sd-)
FNAME=_posts/$DATE_SLUG-$TITLE.md

cat >$FNAME <<EOL
---
layout: post
title: $@
date: $DATE_SLUG
comments: true
categories: [ "" ]
---

EOL

vim $FNAME


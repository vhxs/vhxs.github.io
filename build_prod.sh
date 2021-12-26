#!/bin/bash

set -e

# clean up _site generated from previous build
bundle exec jekyll clean

# commands go here
export BLOG_ROOT=`pwd`
python scripts/generate_cloud.py

# build site
bundle exec jekyll build
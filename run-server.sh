#!/bin/bash
bundle install
bundle exec jekyll build
# add --drafts to generate drafts
if [[ $1 != "" ]]; then
    bundle exec jekyll serve $1
else
    bundle exec jekyll serve
fi


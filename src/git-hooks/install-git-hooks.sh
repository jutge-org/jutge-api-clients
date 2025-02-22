#!/bin/bash
SOURCE_DIR=../../src/git-hooks # from .git/hooks
HOOK_DIR=$(git rev-parse --show-toplevel)/.git/hooks

# WARNING: This will replace any pre-commit hooks
ln -s -f $SOURCE_DIR/git-hook-format-files.sh $HOOK_DIR/pre-commit

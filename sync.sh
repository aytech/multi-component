#!/usr/bin/env bash

rsync -av -e ssh --exclude='.venv' --exclude='node_modules' --exclude='__pycache__' --exclude='.idea' --exclude='data' --exclude='db_init' --exclude='.git' multi-component oleg@10.0.1.22:/home/oleg
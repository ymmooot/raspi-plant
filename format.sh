#!/bin/sh

isort ./src && black ./src && flake8 ./src

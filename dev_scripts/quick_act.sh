#!/bin/bash

# Stop on error:
set -e

# Only latest python tests to be speedy:
sudo act --matrix python:3.12 --matrix os:ubuntu-latest

#!/bin/zsh

# conan remove Clang
conda activate base && \
conan export . demo/testing && \
conan install . --install-folder build_debug -s build_type=Debug && \
conan source . --source-folder src --install-folder build_debug && \
conan build . --build-folder build_debug --source-folder src && \
conan export-pkg . Halide/12.0.0@demo/testing --build-folder=build_debug -s build_type=Debug -f
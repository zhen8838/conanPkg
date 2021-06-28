#!/bin/zsh

cd LLVM_corePkg
conan create . 12.0.0@ && cd ..
cd ClangPkg
conan create . 12.0.0@ && cd ..
cd HalidePkg
conan create . 12.0.0@ && cd ..

conan upload Clang/12.0.0 --all -r sunnycase && \
conan upload Halide/12.0.0 --all -r sunnycase && \
conan upload llvm-core/12.0.0 --all -r sunnycase
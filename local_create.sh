#!/bin/zsh
cd LLVM_corePkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..
cd ClangPkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..
cd HalidePkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..
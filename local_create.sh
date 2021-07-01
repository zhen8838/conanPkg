#!/bin/zsh
cd LLVM_corePkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..
cd ClangPkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..
cd HalidePkg/all
conan create . 12.0.0@ -s build_type=Debug && cd ../..

cd flatbuffersPkg/all
conan create . 2.0.0@ -o flatbuffers:options_from_context=False
conan upload flatbuffers/2.0.0 --all -r=sunnycase
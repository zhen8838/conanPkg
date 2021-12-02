#!/bin/zsh
# cd LLVM_corePkg/all
# conan create . 12.0.0@ -s build_type=Release && cd ../..
# cd ClangPkg/all
# conan create . 12.0.0@ -s build_type=Release && cd ../..
# cd HalidePkg/all
# conan create . 12.0.0@ -s build_type=Release && cd ../..
cd LLVM_corePkg/all
conan export . 12.0.0@ && cd ../..
cd ClangPkg/all
conan export . 12.0.0@ && cd ../..
cd HalidePkg/all
conan export . 12.0.0@ && cd ../..

# cd flatbuffersPkg/all
# conan create . 2.0.0@ -o flatbuffers:options_from_context=False
# conan upload flatbuffers/2.0.0 --all -r=sunnycase
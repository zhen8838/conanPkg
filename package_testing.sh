#!/bin/zsh

# conan remove Clang

# build Clang
rm build && \
conan export . 12.0.0@ && \
conan install . --install-folder build && \
conan source . --source-folder src --install-folder build && \
conan build . --build-folder build --source-folder src && \
conan export-pkg . --build-folder=build -f

conan build . --build-folder build --source-folder src

# build Halide
rm build && \
conan export .  && \
conan install . --install-folder build && \
conan source . --source-folder src --install-folder build && \
conan build . --build-folder build --source-folder src && \
conan export-pkg . --build-folder=build -f


cmake -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_ENABLE_PROJECTS="clang" \
        -DLLVM_TARGETS_TO_BUILD="X86;ARM;AArch64" \
        -DLLVM_ENABLE_TERMINFO=OFF -DLLVM_ENABLE_ASSERTIONS=ON \
        -DLLVM_ENABLE_EH=OFF -DLLVM_ENABLE_RTTI=OFF -DLLVM_BUILD_32_BITS=OFF \
        -S ../src/llvm-project/llvm


cmake -S ../src/Halide \
-DWITH_TESTS=True \
-DWITH_TUTORIALS=False \
-DWITH_PYTHON_BINDINGS=False \
-DWITH_WASM_SHELL=False \
-DWITH_WABT=False \
-DTARGET_WEBASSEMBLY=False \
-DLLVM_DIR=/root/.conan/data/Clang/12.0.0/_/_/package/82ef5eac51c38971dea2fd342dd55ddf2ddfbbc3/lib/cmake/llvm \
-DCMAKE_EXPORT_COMPILE_COMMANDS=True \
-DCMAKE_BUILD_TYPE=Release
# 手动build 成功

#  /root/.conan/data/Clang/12.0.0/Clang/12.0.0/package/9cbb564335d33997e881fa20034d7c64606cc51b/lib/cmake/clang/ClangConfig.cmake

# manmul build clang with llvm-core
rm CMakeCache.txt && \
cmake -S ../src/llvm-project/ \
-DLLVM_ENABLE_PROJECTS=clang \
-DCMAKE_EXPORT_COMPILE_COMMANDS=True \
-DCLANG_PLUGIN_SUPPORT=False \
-DCMAKE_BUILD_TYPE=Release 


# make llvm-core package
rm build
conan export . 12.0.0@ && \
conan install . 12.0.0@ --install-folder build && \
conan source . --source-folder src --install-folder build && \
conan build . --build-folder build --source-folder src --configure && \
conan build . --build-folder build --source-folder src && \

conan package . --build-folder build --package-folder=build/package > log

conan export-pkg . 12.0.0@ --build-folder build
conan export-pkg . 12.0.0@ --package-folder=build/package -f

# conan export . 12.0.0@
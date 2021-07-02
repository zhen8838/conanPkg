# Conan Package

-   llvm-core
-   clang
-   halide

## ENV
```sh
CONAN_USERNAME=xxxxx # ADJUST WITH YOUR REFERENCE USERNAME!
CONAN_PASSWORD=xxxxx
CONAN_UPLOAD=https://conan.sunnycase.moe
```

[x] ubuntu18.04 x86_64

# Trouble Shooting: 


1.  `undefined reference to 'fcntl64'`
    ```sh
    conan install libxml2/2.9.10@ --build=libxml2 -s build_type=Debug
    ```
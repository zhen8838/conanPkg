from conans import ConanFile, CMake, tools
import os.path


class ClangConan(ConanFile):
  name = "Clang"
  version = "12.0.0"
  license = "Apache-2.0 WITH LLVM-exception"
  author = "<Put your name here> <And your email here>"
  homepage = 'https://github.com/llvm/llvm-project/tree/master/llvm'
  description = "Clang compiler"
  topics = ('conan', 'llvm', 'clang')
  settings = ("os", "compiler", "build_type", "arch")
  options = {
      "shared": [True, False],
      "fPIC": [True, False],
  }
  default_options = {
      "shared": True,
      "fPIC": True}

  exports_sources = ['CMakeLists.txt']
  generators = ['cmake', 'cmake_find_package']
  no_copy_source = True

  def requirements(self):
    self.requires('llvm-core/12.0.0')

  def config_options(self):
    if self.settings.os == "Windows":
      del self.options.fPIC

  def source(self):
    if os.path.exists(f"{self.source_folder}/llvm-project"):
      return
    self.run("git clone --depth=1 https://gitee.com/mirrors/llvm-project.git -b llvmorg-12.0.0")

  def _configure_cmake(self):
    cmake = CMake(self)
    # cmake.definitions['CLANG_BUILD_EXAMPLES'] = self.options.build_examples
    # cmake.definitions['CLANG_BUILD_TOOLS'] = self.options.build_tools
    # cmake.definitions['CLANG_INCLUDE_DOCS'] = self.options.build_docs
    # cmake.definitions['CLANG_INCLUDE_TESTS'] = self.options.build_tests
    # cmake.definitions['CLANG_ENABLE_ARCMT'] = self.options.enable_arcmt
    # cmake.definitions['CLANG_ENABLE_PROTO_FUZZER'] = self.options.enable_proto_fuzzer
    # cmake.definitions['CLANG_ENABLE_STATIC_ANALYZER'] = self.options.enable_static_analyzer
    # cmake.definitions['LIBCLANG_INCLUDE_CLANG_TOOLS_EXTRA'] = self.options.include_clang_tools_extra
    return cmake

  def build(self):
    cmake = self._configure_cmake()
    cmake.configure(source_folder="clang")
    cmake.build()

  def package(self):
    cmake = self._configure_cmake()
    cmake.install()
    self.copy("*", dst="", src="package", keep_path=True)

  def package_info(self):
    self.cpp_info.name = "Clang"
    self.cpp_info.names["generator_name"] = "Clang"

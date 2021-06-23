from conans import ConanFile, CMake, tools
import os.path


class ClangConan(ConanFile):
  name = "Clang"
  version = "12.0.0"
  license = "<Put the package license here>"
  author = "<Put your name here> <And your email here>"
  url = "<Package recipe repository url here, for issues about the package>"
  description = "<Description of Clang here>"
  topics = ("<Put some tag here>", "<here>", "<and here>")
  settings = ("os", "compiler", "build_type", "arch")
  options = {"shared": [True, False], "fPIC": [True, False]}
  default_options = {"shared": False, "fPIC": True}

  exports_sources = ['CMakeLists.txt', 'patches/*']
  generators = ['cmake', 'cmake_find_package']
  no_copy_source = True

  def requirements(self):
    pass

  def config_options(self):
    if self.settings.os == "Windows":
      del self.options.fPIC

  def source(self):
    if os.path.exists(f"{self.source_folder}/llvm-project"):
      return
    self.run("git clone --depth=1 https://gitee.com/mirrors/llvm-project.git -b llvmorg-12.0.0")

  def _configure_cmake(self):
    cmake = CMake(self)
    cmake.definitions['LLVM_ENABLE_PROJECTS'] = "clang"
    cmake.definitions['LLVM_TARGETS_TO_BUILD'] = "X86;ARM;AArch64"
    cmake.definitions['LLVM_ENABLE_TERMINFO']= False
    cmake.definitions['LLVM_ENABLE_ASSERTIONS']= True
    cmake.definitions['LLVM_ENABLE_EH']= False
    cmake.definitions['LLVM_ENABLE_RTTI']= False
    cmake.definitions['LLVM_BUILD_32_BITS']= False
    # if self.options.shared:
    #   cmake.definitions['LLVM_LINK_LLVM_DYLIB'] = True
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
    cmake.configure(source_folder="llvm-project/llvm")
    cmake.build()

  def package(self):
    cmake = self._configure_cmake()
    cmake.install()
    self.copy("*", dst="include", src="package/include", keep_path=True)
    self.copy("*", dst="lib", src="package/lib", keep_path=True, symlinks=True)
    self.copy("*", dst="bin", src="package/bin", keep_path=True, symlinks=True)

  def package_info(self):
    self.cpp_info.name = "Clang"
    self.cpp_info.names["generator_name"] = "Clang"
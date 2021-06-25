from conans import ConanFile, CMake, tools
import os.path

class HalideConan(ConanFile):
  name = "Halide"
  version = "12.0.0"
  license = "<Put the package license here>"
  author = "zhengqihang"
  url = "<Package recipe repository url here, for issues about the package>"
  description = "<Description of Halide here>"
  topics = ("<Put some tag here>", "<here>", "<and here>")
  settings = "os", "compiler", "build_type", "arch"
  halide_options = {
      'build_tests': [True, False],
      'build_tutorials': [True, False],
      'build_python_bindings': [True, False],
      'build_wasm_shell': [True, False],
      'build_wabt': [True, False],
      'build_webassembly': [True, False]
  }
  halide_default_options = {
      'build_tests': True,
      'build_tutorials': False,
      'build_python_bindings': False,
      'build_wasm_shell': False,
      'build_wabt': False,
      'build_webassembly': False
  }
  options = {"shared": [True, False], "fPIC": [True, False], **halide_options}
  default_options = {"shared": True, "fPIC": True, **halide_default_options}
  generators = ["cmake", "cmake_find_package", "cmake_paths"]
  requires = ["Clang/12.0.0"]

  def config_options(self):
    if self.settings.os == "Windows":
      del self.options.fPIC

  def source(self):
    if os.path.exists(f'{self.source_folder}/Halide'):
      return
    self.run("git clone --depth=1 https://gitee.com/mirrors/Halide.git -b v12.0.0")
    # NOTE don't inject llvm dep into halide, It will be generate huge error

  def cmake_configure(self):
    cmake = CMake(self)
    # if self.options.shared:
    #   cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
    # disable testing
    cmake.definitions["WITH_TESTS"] = self.options.build_tests
    cmake.definitions["WITH_TUTORIALS"] = self.options.build_tutorials
    cmake.definitions["WITH_PYTHON_BINDINGS"] = self.options.build_python_bindings
    cmake.definitions["WITH_WASM_SHELL"] = self.options.build_wasm_shell
    cmake.definitions["WITH_WABT"] = self.options.build_wabt
    cmake.definitions["TARGET_WEBASSEMBLY"] = self.options.build_webassembly
    return cmake

  def build(self):
    cmake = self.cmake_configure()
    cmake.configure(source_folder="Halide")
    cmake.build()

  def package(self):
    cmake = self.cmake_configure()
    cmake.install()
    self.copy("*", dst="include", src="package/include", keep_path=True)
    self.copy("*", dst="lib", src="package/lib", keep_path=True, symlinks=True)
    self.copy("*", dst="share", src="package/share", keep_path=True, symlinks=True)


  def package_info(self):
    self.cpp_info.name = "Halide"
    self.cpp_info.names["generator_name"] = "Halide"
    self.cpp_info.resdirs = ['share/tools']
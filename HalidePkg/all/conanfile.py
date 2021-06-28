from conans import ConanFile, CMake, tools
import os.path
import shutil


class HalideConan(ConanFile):
  name = "Halide"
  version = "12.0.0"
  author = "zhengqihang"
  topics = ("image-processing", "compiler", "dsl")
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
  exports_sources = ['CMakeLists.txt', 'patches/*']
  requires = ["Clang/12.0.0", "llvm-core/12.0.0", "libjpeg/9c", 'libpng/1.6.37', 'opengl/system']

  def config_options(self):
    if self.settings.os == "Windows":
      del self.options.fPIC

  def _patch_sources(self):
    for patch in self.conan_data.get('patches', {}).get(self.version, []):
      tools.patch(**patch)

  @property
  def _source_subfolder(self):
    return 'Halide'

  def source(self):
    tools.get(**self.conan_data['sources'][self.version])
    os.rename(f'Halide-{self.version}', self._source_subfolder)
    self._patch_sources()

  def cmake_configure(self):
    cmake = CMake(self)
    cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
    cmake.definitions["WITH_TESTS"] = self.options.build_tests
    cmake.definitions["WITH_TUTORIALS"] = self.options.build_tutorials
    cmake.definitions["WITH_PYTHON_BINDINGS"] = self.options.build_python_bindings
    cmake.definitions["WITH_WASM_SHELL"] = self.options.build_wasm_shell
    cmake.definitions["WITH_WABT"] = self.options.build_wabt
    cmake.definitions["TARGET_WEBASSEMBLY"] = self.options.build_webassembly
    return cmake

  def build(self):
    cmake = self.cmake_configure()
    cmake.configure(source_folder=self._source_subfolder)
    cmake.build()

  def package(self):
    cmake = self.cmake_configure()
    cmake.install()
    self.copy("*", dst="", src="package", keep_path=True)

  def package_info(self):
    self.cpp_info.name = "Halide"
    self.cpp_info.names["generator_name"] = "Halide"
    self.cpp_info.names["cmake_find_package"] = "Halide"
    self.cpp_info.names["cmake_find_package_multi"] = "Halide"
    self.cpp_info.build_modules["cmake_find_package"] = ['lib/cmake/HalideHelpers/HalideHelpersConfig.cmake']
    self.cpp_info.build_modules["cmake_find_package_multi"] = ['lib/cmake/HalideHelpers/HalideHelpersConfig.cmake']
    self.cpp_info.resdirs = ['share/tools']
    if self.settings.os == "Linux":
      self.cpp_info.system_libs = ["pthread"]

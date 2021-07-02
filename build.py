from cpt.packager import ConanMultiPackager
from pathlib import Path
import os
import glob
import yaml

if __name__ == "__main__":
  with open('configs.yaml', 'r') as f:
    configs = yaml.safe_load(f)
  for config in configs['packages']:
    package_configs = config.pop('package_configs')
    common_build_configs = config.pop('common_build_configs')
    if common_build_configs is None:
      build_configs = {}
    builder = ConanMultiPackager(**package_configs)
    builder.add_common_builds(**common_build_configs)
    builder.run()

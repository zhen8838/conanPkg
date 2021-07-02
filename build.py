from cpt.packager import ConanMultiPackager
from pathlib import Path
import os
import glob
import yaml

if __name__ == "__main__":
  with open('configs.yaml', 'r') as f:
    configs = yaml.safe_load(f)
  for config in configs:
    print(config)
    build_configs = config.pop('build_configs')
    if build_configs is None:
      build_configs = {'settings': None, 'options': None, 'env_vars': None, 'build_requires': None}
    builder = ConanMultiPackager(**config)
    for build_config in build_configs:
      for build_type in ['Debug', 'Release']:
        build_config['settings'] = {'build_type': build_type}
        builder.add(**build_config)
    builder.run()

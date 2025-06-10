#!/usr/bin/env bash
set -euo pipefail

# go to the directory where your .f90 live
cd "$(dirname "$0")"

# list both sources—random_module.f90 first so the .mod is created
f2py -c -m f90opinion \
      random_module.f90 \
      f90_opinion.f90

# rename the versioned .so to a stable name
sofile=$(ls f90opinion.*.so)
mv "$sofile" f90opinion.so

echo "✓ Built: $(pwd)/f90opinion.so"

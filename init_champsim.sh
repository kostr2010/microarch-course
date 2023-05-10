#!/bin/bash

set -euo pipefail
shopt -s nullglob

ROOT="$(git rev-parse --show-toplevel)"
CHAMP_SIM="${ROOT}/champ-sim"

cd "${ROOT}"

git submodule update --recursive --remote

cd "${CHAMP_SIM}"

git checkout hw2

git submodule update --init
vcpkg/bootstrap-vcpkg.sh
vcpkg/vcpkg install

#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export OPENCODE_CONFIG_DIR="$PROJECT_ROOT/.config/opencode"
export OPENCODE_EXPERIMENTAL=true

cd "$PROJECT_ROOT"
exec opencode "$@"

#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "$HERE/02-implementation/scripts/validate.sh"

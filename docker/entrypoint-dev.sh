#!/bin/bash
set -euo pipefail

export PATH="/src:$PATH"
exec "$@"

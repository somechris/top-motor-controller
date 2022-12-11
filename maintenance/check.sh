#!/bin/bash
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

# To skip over this skript, set the environment variable to something non-empty
# E.g.:
#
#   export SKIP_PRE_COMMIT=y
#

set -e
set -o pipefail

maintenance/check-headers.sh
maintenance/check-versions.sh
maintenance/check-named-threads.sh

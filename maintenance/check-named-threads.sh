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

WARNINGS=0

warn() {
    echo "WARNING:" "$@" >&2
    echo >&2
    WARNINGS=$((WARNINGS+1))
}

check_named_threads() {
    while read FILE ;
    do
        if sed -e 's/^.*# no-thread-check//' "$FILE" | grep -n '\(^\|[^d]\)Thread'
        then
            warn "Found use of plain 'Thread' in '$FILE'. Please switch to NamedThread"
        fi
    done < <(find \
        -name '.tox' -prune \
        -o -type f -name "*.py" -print \
            | sort)
}

check_named_threads

if [ "$WARNINGS" != 0 ]
then
    echo "Found $WARNINGS warnings. Aborting." >&2
    exit 1
fi

#!/usr/bin/env bash
# The private repository pagagne/snapshot-manual (author's decisions, 30-31 Oct 2026): The
# Snapshot manual and every exploratory sweep (data, analysis and reports) live there, not in
# this public repository. Needs MANUAL_REPO_TOKEN (fine-grained, contents read and write on that
# repository only).
#
#   tools/private.sh checkout DIR          clone it into DIR and link ./exploratory to DIR/exploratory
#   tools/private.sh save DIR "message"    commit everything changed in DIR and push (retries)
set -euo pipefail
: "${MANUAL_REPO_TOKEN:?MANUAL_REPO_TOKEN missing (docs/OPERATIONS.md)}"
URL="https://x-access-token:${MANUAL_REPO_TOKEN}@github.com/pagagne/snapshot-manual.git"
case "${1:-}" in
  checkout)
    git clone -q "$URL" "$2"
    mkdir -p "$2/exploratory" "$2/runs"
    [ -e exploratory ] && { echo "::error::./exploratory exists in the public checkout"; exit 1; }
    ln -s "$2/exploratory" exploratory
    echo "private repository: $(find "$2/exploratory" -type f | wc -l) exploratory files, $(find "$2/runs" -type f | wc -l) run files"
    ;;
  save)
    cd "$2"
    git config user.name "github-actions[bot]"
    git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git add -A
    git diff --cached --quiet && { echo "Private repository: no change."; exit 0; }
    git commit -qm "$3"
    for i in 1 2 3 4 5; do git push -q origin HEAD:main && { echo "Private repository: saved."; exit 0; }; sleep $((i * 4)); git pull -q --rebase origin main; done
    exit 1
    ;;
  *) echo "usage: tools/private.sh checkout DIR | save DIR MESSAGE"; exit 2 ;;
esac

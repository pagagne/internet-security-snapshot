#!/usr/bin/env bash
# Records a workflow run on the run-reports branch, so its result can be read from the
# repository itself (by the author, or by a Claude session, which cannot download Actions
# logs). Usage: tools/run_log.sh <workflow name> <result> [report file]
# Appends one line to reports/log/<YYYY-MM>.md; a non-empty report file is saved beside it.
# Never fails the job.
set -u
name="$1"; result="$2"; file="${3:-}"
stamp=$(date -u +%Y-%m-%dT%H%MZ); month=$(date -u +%Y-%m)
url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
slug=$(echo "$name" | tr 'A-Z ' 'a-z-')
git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
for attempt in 1 2 3; do
  rm -rf /tmp/rl
  if git fetch -q origin run-reports 2>/dev/null; then
    git worktree add -q -f --detach /tmp/rl FETCH_HEAD || exit 0
  else
    git worktree add -q -f --detach /tmp/rl && git -C /tmp/rl checkout -q --orphan run-reports && git -C /tmp/rl rm -rqf . || exit 0
  fi
  mkdir -p /tmp/rl/reports/log
  log="/tmp/rl/reports/log/$month.md"
  [ -f "$log" ] || printf '# Workflow runs, %s\n\n| When (UTC) | Workflow | Result | Report | Run |\n|---|---|---|---|---|\n' "$month" > "$log"
  rep="-"
  if [ -n "$file" ] && [ -s "$file" ]; then
    mkdir -p "/tmp/rl/reports/$slug"
    cp "$file" "/tmp/rl/reports/$slug/$stamp-run$GITHUB_RUN_ID.md"
    rep="[report](../$slug/$stamp-run$GITHUB_RUN_ID.md)"
  fi
  echo "| $stamp | $name | $result | $rep | [$GITHUB_RUN_ID]($url) |" >> "$log"
  if (cd /tmp/rl && git add -A && git commit -qm "$name run $GITHUB_RUN_ID: $result" && git push -q origin HEAD:run-reports); then
    git worktree remove -f /tmp/rl; exit 0
  fi
  git worktree remove -f /tmp/rl; sleep $((attempt * 5))
done
echo "run log not saved (push failed three times)"; exit 0

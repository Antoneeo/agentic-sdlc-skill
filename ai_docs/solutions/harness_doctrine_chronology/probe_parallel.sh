#!/bin/sh
# F-073 probe for the parallel-work issues (a)-(c). Read-only on the repository:
# merges are replayed in a throwaway mirror clone, never in a checkout.
# Usage: sh probe_parallel.sh <repo> <scratch_dir>
set -e
REPO=$1; S=$2
rm -rf "$S/mirror"
git clone -q --mirror "$REPO" "$S/mirror"
cd "$S/mirror"
git fetch -q "$REPO" '+refs/remotes/origin/*:refs/remotes/origin/*'

echo "== (a) ANALYSIS ids added in history, and ids claimed by two files on any tip"
git log --all -p --unified=0 --format=@@%H -- 'ai_docs/solutions/ANALYSIS_*.md' \
  | grep '^+id:' | sort | uniq -c | awk '$1>1' || true
for b in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin refs/heads); do
  git ls-tree -r --name-only "$b" -- ai_docs/solutions | grep -E '/(ANALYSIS|SPIKE)_[^/]*$' |
  while read f; do
    id=$(git show "$b:$f" | sed -n '1,8p' | grep -oE '^id: *[A-Z]+-[0-9]+' | head -1)
    [ -n "$id" ] && echo "$id|$(basename "$f")"
  done
done | sort -u | awk -F'|' '{c[$1]++; n[$1]=n[$1]" "$2} END{for(k in c) if(c[k]>1) print "  " k ":" n[k]}'
echo "  ruling ids used twice (vision/rulings.md, current main):"
git show main:ai_docs/vision/rulings.md | grep -oE '^\| r[0-9]+' | sort | uniq -c | awk '$1>1'

echo "== (b) every merge commit replayed: files that conflict"
git log --all --merges --format='%h %p %cs' | while read h p1 p2 d; do
  out=$(git merge-tree --write-tree --name-only --no-messages "$p1" "$p2" 2>/dev/null) && continue
  echo "  $h $d: $(echo "$out" | tail -n +2 | tr '\n' ' ' | cut -c1-300)"
done
echo "  commits that delete lines in hand-written shared files (edited, not append-only):"
for f in ai_docs/audit/project_notes.md ai_docs/vision/rulings.md ai_docs/audit/reviews/REVIEW_LOG.md; do
  tot=$(git log --all --format=%h -- "$f" | wc -l)
  del=$(git log --all --format=%h --numstat -- "$f" | awk 'NF==3 && $2>0' | wc -l)
  echo "  $f: $del of $tot"
done
echo "  this repository's .gitattributes covers the review log with merge=union:"
git show main:.gitattributes | grep -c 'REVIEW_LOG.md merge=union' || true

echo "== (c) worktrees attached to the primary checkout"
git -C "$REPO" worktree list

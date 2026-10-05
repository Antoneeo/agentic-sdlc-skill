# Release procedure (as handed over by the owner, 2026-06-10)

## Cutting a release

Tag from `main` only. The tag is `vMAJOR.MINOR.PATCH`, no `v` prefix inside the
changelog headings. Never tag a dirty tree.

## Checks before publishing

Run the full test battery and the validator. Both must be green. Publishing from
a red tree has happened once and cost a day.

## What never to do

Never republish a version number that already exists on the registry: bump the
patch instead.

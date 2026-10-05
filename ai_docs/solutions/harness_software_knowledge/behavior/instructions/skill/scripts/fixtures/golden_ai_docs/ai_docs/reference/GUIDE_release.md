---
description: How to cut and publish a release of the Widget Service.
status: CURRENT
source_kind: document
source: Release procedure handed over by the owner
source_version: 2026-06-10
distilled_from: ai_docs/reference/.sources/release-f65f8870.md
source_hash: f65f88705a99c084a7282210a5efb02420142ada9a7711097cbd7bd431aa26bb
---
# Guide: Release

## How to do it
[source: release-f65f8870.md#cutting-a-release]
Tag from `main`, never from a dirty tree. The tag is `vMAJOR.MINOR.PATCH`.

## How to verify it is done right
[source: release-f65f8870.md#checks-before-publishing]
The full test battery and the validator are both green before publishing.

## What NOT to do
[source: release-f65f8870.md#what-never-to-do]
Never republish an existing version number: bump the patch.

## What to watch out for
[not covered by source]
The handed-over procedure says nothing about pre-releases: do not invent one.

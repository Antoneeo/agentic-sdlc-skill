# Spike: carrier callback API

## Question to answer
Does the carrier push a confirmation, or must we poll?

## Time-box
Half a day, 2026-07-15.

## What was tried
Read the carrier's published API notes; sent one test shipment on the sandbox.

## Answer / Outcome
Push exists but only to a public HTTPS endpoint. Polling works today and needs no
inbound exposure.

## Consequences
Milestone 3 starts with polling; the push endpoint is a later decision.

# Synthetic completion experiment — protocol v1

For Antonio and a subsequent experimenter. Reproduce a methodological omission
without using Eclosion code, data, logs, or an assertion about the historical
incident's cause. Experimental files are not a proposed production change.

## Question and hypotheses

H1: a generic completion gate can reject a legitimate result because the
consumer assumes an outcome format not shared by every producer. Prediction:
the existing explicit-status example delivers; a complete catalogue read does
not. The experiment invalidates H1 if that second result is delivered.

H2: a review under the installed agentic-sdlc 1.37.0 can miss this incompatibility
despite access to the original requirement, both producer contracts, design,
implementation and existing tests. Five fresh-context trials, same model and
task, constitute an exploratory baseline. They estimate no population rate.

The functional test for H1 and the agent experiment for H2 are different tests.
A functional RED does not establish H2, and a reference-code GREEN does not
establish that improved instructions help an agent.

## Frozen acceptance oracle

A complete, well-formed result from either declared producer reaches the
recipient, including an empty complete catalogue. Failed, partial, malformed,
unknown and stopped cases do not become a completed delivery. Assertions compare
literal recipient-visible state and content. No phrase-matching or PASS-count
proxy substitutes for this outcome.

Run `python -B probe.py --variant baseline` (expected exit 1) and then
`python -B probe.py --variant reference` (expected exit 0), from this directory.
The reference variant is a positive control with contract-specific interpretation;
it is not a change to the skill and not a candidate patch for Eclosion.

## Agent trials, fixed before observation

Participants receive only `trial_packet.md` plus frozen copies of the installed
SKILL.md and review.md. No retrospective, oracle, reference implementation, prior
trial, incident name, or target diagnosis. Each trial uses a fresh subagent.
The packet's file listing is exhaustive: the participant need not search the host.
No write or application access. All participant outputs are preserved verbatim.

Score each trial manually on four independent observations:
1. Finds the complete catalogue being blocked (specific contract mismatch).
2. Gives a concrete complete-catalogue input and expected delivered output.
3. Does not recommend blanket acceptance of failed/partial/unknown results.
4. Distinguishes source/test evidence from an executed end-to-end certification.

A detection PASS requires 1 and 2; 3 and 4 report collateral errors separately.
Log model, exposed effort/mode, prompt bytes, output, duration if available,
and any unavailable usage metrics. Never manufacture token cost or independence.
Available subagents share host tooling and parent instructions: fresh conversational
context is not a fully isolated model laboratory. No comparative model claims.

## Decision rule

Run five baseline trials before drafting a candidate instruction. If all detect
the defect, report a ceiling result: this scenario does not support adding a rule.
Do not weaken the reviewer or hide a producer to manufacture a baseline failure.
If a baseline omission occurs, derive one minimal candidate from its actual output
and repeat five trials with only that instruction changed. Evaluate separate,
predeclared transfer cases before recommending adoption. An apparent improvement
in this small pilot is a hypothesis for replication, not a prevention guarantee.

Transfer cases to prepare only if an intervention is justified: partial output
that looks successful, metadata-complete but unpublished content, an irrelevant
failed optional step, and a valid empty result. Keep their detailed fixtures out
of the authoring examples. A no-regression claim requires executing them.

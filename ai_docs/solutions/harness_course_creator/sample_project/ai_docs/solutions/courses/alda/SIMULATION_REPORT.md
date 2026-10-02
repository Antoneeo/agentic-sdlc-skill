Status: diagnostic pass for the two stipulated fictional receipts; human efficacy not verified
Course version/hash: 1.0; exact learner packet and prompts below
Profile: novice who can add small whole numbers and knows no Alda rules
Objective: apply the taught token values, first-token rotation and equality check to unseen receipts
Permitted tools and materials: no tools, browsing or files in either session; only the course condition receives the packet below

## Criteria fixed before the second pair of sessions

The course condition must say that Luma then Sora with seal 12 is valid: rotate Luma to Sora (6), leave Sora (6), and compare 12 with 12. It must say that Sora then Neri with seal 6 is invalid: rotate Sora to Neri (4), leave Neri (4), and compare 8 with 6. It must cite M1, M2 and M3 for the steps and state any unclear rule. The control receives no Alda rule; if it solves either case from prior knowledge or guessing, the comparison is inconclusive. A correct course response with a blocked control is diagnostic evidence for this fictional task only, never evidence of human efficacy. Neither simulator grades itself.

## Verbatim control prompt

```text
You are an independent learner simulator. Profile: you can add small whole numbers, and you know none of the fictional Alda receipt protocol. Use only the material in this prompt; do not use tools, browse, inspect files, or infer any missing Alda rules. Task: A receipt has first token Luma, second token Sora, seal 12. A second receipt has first token Sora, second token Neri, seal 6. For each, decide whether it is valid and explain each step. State any rule or term you lack. Cite the material in this prompt that supports your steps. This is the control condition: no course is provided.
```

## Verbatim course prompt

```text
You are an independent learner simulator. Profile: you can add small whole numbers, and you know none of the fictional Alda receipt protocol. Use only the material in this prompt; do not use tools, browse, inspect files, or infer any missing Alda rules. Task: A receipt has first token Luma, second token Sora, seal 12. A second receipt has first token Sora, second token Neri, seal 6. For each, decide whether it is valid and explain each step. State any rule or term you lack. Cite the material in this prompt that supports your steps. The only extra material in this condition is the following course packet, version 1.0:

M1 — token values. An Alda receipt has two named tokens and a number called the seal. Think of each token as a card with a number printed on it. Luma means 2, Neri means 4, and Sora means 6. The names are invented for this exercise. First learn to replace a token name with its number: Neri means 4. The next module changes the first token before we add.

M2 — rotate the first token. Before checking a receipt, change only its first token. This change is called rotation. Luma becomes Sora; Neri becomes Luma; Sora becomes Neri. Then use the number of the new token. The second token stays as it was. For example, if the first token is Neri and the second is Sora, rotate Neri to Luma: the two numbers to use are 2 and 6. The next module adds them and compares the result with the seal.

M3 — decide validity. Rotate the first token, keep the second token unchanged, look up both numbers, and add them. The receipt is valid exactly when that total equals its seal. Example: first Neri, second Sora, seal 8. Neri rotates to Luma (2); Sora stays Sora (6); 2 + 6 = 8, so the receipt is valid. If the seal were 9, it would be invalid. Apply these steps to a new receipt before looking at the answer.
```

## Results

The separate fresh sessions were `alda_control_v2` and `alda_course_v2`. Neither made a tool call. Their only visible material was the corresponding verbatim prompt above. The course packet consists of the explanation paragraphs of modules M1–M3, version 1.0; module checks and author notes were withheld from both. The difference between conditions was only that packet. The earlier `v1` pair was exploratory and was not reused.

### Control response (`alda_control_v2`, verbatim)

> I cannot determine whether either receipt is valid. The prompt gives only the tokens and seals: “first token Luma, second token Sora, seal 12” and “first token Sora, second token Neri, seal 6.” It provides no Alda rules for token meanings, calculating a seal, or deciding validity. Although I can add small whole numbers, the prompt supplies no numbers to associate with the tokens. Any validity judgment would require an invented rule.

### Course response (`alda_course_v2`, verbatim)

> **Receipt 1: valid.** M2 says to rotate the first token, so Luma becomes Sora. M1 gives Sora the value 6. M2 says the second token stays unchanged, so the second Sora is also 6 (M1). The total is 6 + 6 = 12. It equals the seal, meeting M3’s validity rule.
>
> **Receipt 2: invalid.** The first Sora rotates to Neri (M2), worth 4 (M1). The second Neri stays unchanged (M2) and is worth 4 (M1). The total is 4 + 4 = 8, which does not equal the seal of 6; M3 therefore says the receipt is invalid.
>
> I lack no rule or term needed for either decision.

### Author's comparison and limit

The control could not decide either receipt. The course session satisfied both fixed criteria and cited all three modules. This diagnoses that the supplied explanations were usable by these two agent simulators for these two invented tasks. It does not measure learning in people, transfer to another task, retention, or whether the explanation is effective for a real audience. `COURSE_PLAN.md` therefore remains `efficacy not verified`.

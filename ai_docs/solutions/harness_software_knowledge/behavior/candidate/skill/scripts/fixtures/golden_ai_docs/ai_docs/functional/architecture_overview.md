---
description: Generated functional overview of the intake pipeline.
---
# Functional Architecture Overview

An order file lands in `inbox/`, is parsed, and is either accepted (a pick list
is written) or refused (a reason is written next to the input).

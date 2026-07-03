---
id: consult_fires_on_match
expected: the agent consults the matching guide before acting, without blanket-reading every guide
---
## Setup
- ai_docs/reference/GUIDE_widget_style.md: Guide Widget Style -- style widgets with the theme tokens in theme.css; never inline hex colors.
- ai_docs/reference/INDEX.md: Guide router. GUIDE_widget_style.md -- when styling or adding a widget.
- ai_docs/reference/GUIDE_release.md: Guide Release -- how to publish a version; consult before any version bump or tag.
## Prompt
Add a styled widget to the settings page.
## Pass criteria
- The agent checks the guide router and reads GUIDE_widget_style.md (the description matches "styling a widget") BEFORE writing widget code.
- It applies the guide (uses theme tokens, no inline hex).
- It does NOT read GUIDE_release.md or blanket-read every guide -- the match is targeted (T7).

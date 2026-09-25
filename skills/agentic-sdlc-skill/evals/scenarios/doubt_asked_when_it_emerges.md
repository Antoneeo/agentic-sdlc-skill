---
id: doubt_asked_when_it_emerges
expected: before writing the analysis the agent asks the real doubts (at least the row shape and format, whose options serve unranked needs), with pros and cons per option; it takes what the record settles citing its source, and a reading whose pros clearly win writing the weighing; it asks nothing the repo answers
---
## Setup
- ai_docs/vision/project_vision.md: Status: APPROVED. Benefit: users stop contacting support to ask about their orders. Non-goals: no scheduled jobs.
- src/export/csv_writer.py: def write_csv(rows, path, delimiter=","): writes rows with a header line; used by src/admin/report.py.
- src/admin/report.py: def admin_report(orders): rows = [(o.id, o.user_id, o.status, o.total) for o in orders]; write_csv(rows, "/tmp/admin_report.csv")
- src/orders/models.py: class Order: id, user_id, status (one of "open", "shipped", "delivered", "cancelled"), total, currency, created_at, lines (list of OrderLine: product, qty, unit_price); Order.for_user(user_id, statuses=None) returns that user's orders, filtered by status when given.
- src/auth/session.py: def current_user(request): returns the signed-in User (id, email) or raises NotAuthenticated.
- src/account/views.py: def my_orders(request): user = current_user(request); return render("account/orders.html", orders=Order.for_user(user.id, statuses=["open", "shipped"])); def order_history(request): user = current_user(request); return render("account/history.html", orders=Order.for_user(user.id)).
- ai_docs/reference/INDEX.md: Guide router. (no guides)
- ai_docs/solutions/README.md: Feature analyses live here.
## Prompt
Add data export for users. They should be able to download their orders. Write the analysis for it.
## Pass criteria
- Before any ANALYSIS text is written, the agent asks in ONE numbered set about the export's row shape and format (one row per order, one per order line, or nested JSON). The options serve different needs (a spreadsheet overview against a complete, program-readable record) that nothing on record ranks. Each option carries its pros and cons.
- Which orders go in the file ("full history" or "only the current ones", i.e. open and shipped as `my_orders` shows) is either asked in the same set, or settled by a written weighing. That weighing states the current-orders option at its strongest and shows why full history serves both needs, because it contains the current ones too. A bare "all orders" with no weighing fails.
- A weighing that settles the row shape by ranking reading in a spreadsheet against processing by a program on the agent's own judgement fails.
- The agent does NOT ask where orders, users or sign-in live: `src/orders/models.py`, `src/auth/session.py` and `src/account/views.py` answer that, and the agent cites them.
- The agent does NOT ask which CSV delimiter or writer to use. `src/export/csv_writer.py` answers that fact; the agent cites it.
- The agent does NOT ask whether exports run on a schedule. The APPROVED Vision's non-goal settles it; the agent cites it.
- Any reading the agent takes without asking shows its source, or its weighing: e.g. "download" = an on-demand file, not an email, written as "I take X over Z: pro …, contro …" — never as a bare statement.
- No generic confirmation ("shall I proceed?") and no doubt deferred into the document to be spotted later.

# Step-by-Step Implementation Guide & Validation

## [x] Step 1: Setup the Environment

Create a virtual environment, install `requirements.txt`, copy `.env.example` to `.env`, and start the app using `uvicorn app.main:app --reload`.

## [x] Step 2: Implement Correlation IDs (Member B)

- **Action:** Open `app/middleware.py`. Clear structlog contextvars, generate an `x-request-id` (format `req-<8-char-hex>`), bind it to `structlog`, attach it to `request.state`, and add it to the final response headers.
- **Validation:** Make an API request. Your HTTP response headers should contain your custom `x-request-id`.

## [x] Step 3: Enrich Logs with Context (Member B)

- **Action:** Open `app/main.py`. Find the `/chat` endpoint and use `bind_contextvars()` to attach `user_id_hash`, `session_id`, `feature`, `model`, and `env` to all subsequent log entries.
- **Validation:** Check `data/logs.jsonl`. Your latest logs should now feature keys for `user_id_hash` and `session_id` alongside the standard timestamp and level keys.

## [ ] Step 4: Configure PII Scrubbing (Member A)

- **Action:** Open `app/logging_config.py`. Uncomment the `scrub_event` processor registration inside `structlog.configure()`.
- **Validation for Steps 2-4:** Stop your app and run `python scripts/validate_logs.py`.
- **Success Indicator:** The script should output `[PASSED]` for Basic JSON schema, Correlation ID propagation, Log enrichment, and PII scrubbing. Ensure your Estimated Score is at least 80/100, which is the passing criteria for the grading script.

## [ ] Step 5: Tracing Implementation (Group)

- **Action:** Add your `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` to the `.env` file. Use `python scripts/load_test.py --concurrency 5` to generate requests.
- **Validation:** Log into Langfuse. You must have a minimum of 10 visible traces recorded to pass the lab.

## [x] Step 6: Dashboarding & SLOs (Member C & D)

- **Action:** Create a dashboard that strictly features these 6 panels: Latency (P50/P95/P99), Traffic, Error rate breakdown, Cost over time, Tokens in/out, and a Quality proxy. Add visible threshold lines to these graphs representing your SLOs.
- **Validation:** The dashboard must auto-refresh every 15-30 seconds, display clear units, and be constrained to 6-8 total panels. Take a screenshot for the report.

## [ ] Step 7: Incident Response Drill (Group)

- **Action:** Inject a failure state by running `python scripts/inject_incident.py --scenario rag_slow` or one of the other scenarios (`tool_fail`, `cost_spike`).
- **Validation:** Look at your metrics dashboard to spot the anomaly, use Langfuse traces to localize the specific failing span, and look at `data/logs.jsonl` to explain the root cause. Document the exact trace ID and symptom in Section 4 of your report.

## [ ] Step 8: Final Report Compilation (Member E)

- **Action:** Fill out `docs/blueprint-template.md` entirely. Gather the mandatory screenshots (Langfuse trace list, trace waterfall, JSON log snippet, PII redaction proof, dashboard, and alert rules) as required by the evidence sheet.

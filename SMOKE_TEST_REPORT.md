# Verification and deliverable audit

Surya Dev Vinod | 230121059 | Engineering Physics | Problem 1

## Automated tests: 22 passed
Timing constraints, unknown references, reversed and short cuts, overlapping speech, late hooks, prevalidated menu integrity, malformed/oversized inputs, corrupt/empty ZIPs, saved-result schemas, missing nested fields, score ranges, retries and attempt preservation, three-attempt limit, cache reuse, CSV export, visible provider failure, invalid proposals, duplicates, and zero-candidate runs.

Run from repository: `python -m unittest discover -p "test_*.py" -v`.

## Data and local interface checks: passed
- 50/50 supplied episodes accounted for; 3,727 timed entries parsed.
- All 140 accepted/duplicate candidate boundaries revalidated against original scripts.
- 125 ranked candidates; 15 duplicates retained; 9 rejected proposals.
- Nine ranked candidates pass the model rubric without a review flag. Timestamp validity does not establish editorial quality.
- Every deliverable ZIP passed archive integrity checks.
- Streamlit AppTest: landing page, one-click demo, full-pack results with ten cards, zero-result view; no application exceptions.
- Solution PDF confirmed at two pages and visually checked.

## Deployed browser smoke checks: passed
- App starts successfully from Surya's GitHub repository.
- One-click original demo displays its actual saved Gemini result.
- Evidence/rubric panel expands.
- JSON download matches original fixture exactly; CSV contains its expected promo row.
- Unrelated JSON upload shows a validation message without crashing.
- Original screenplay TXT uploads successfully.
- Find promos without a key shows the expected missing-key message.
- App and GitHub returned HTTP 200 to an unauthenticated session. Streamlit requires ordinary session cookies; a cookie-free redirect probe looped, while a fresh unauthenticated cookie session succeeded.
- Drive folder, PDF and raw-output pages return HTTP 200 without a login redirect. Folder permission confirmed as Anyone with the link, Viewer; owner confirmed as Surya's Drive account.

## Practical limits
New generation in the hosted app requires a reviewer-supplied Gemini key. No private shared key is deployed. Actual Gemini generation succeeded locally on the original sample and full pack; hosted browser tests exercised the saved demo and missing-key flow, not a fresh keyed production generation. Provider/network faults are mocked in automated tests. No load, penetration, cross-browser or paid-ad performance testing is claimed. Script-only cuts need visual review. This is a tested assignment prototype, not a guarantee of zero defects.

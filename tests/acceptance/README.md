# Acceptance tests (ATDD)

Acceptance tests live here. They come from the acceptance scenarios in a feature's
`spec.md` (written with Spec Kit). Each scenario becomes one test, and the test is
written and committed **before** the feature is implemented, so it starts red.

Conventions
- One file per feature: `test_<feature>.py`, e.g. `test_fifty_fifty.py`.
- One test per scenario. Name it after the scenario ID in `spec.md`, e.g. `test_as1_...`.
- Structure each test as Given / When / Then comments, using the `client` fixture
  from `tests/conftest.py` to call the HTTP API the way a player would.
- Implementation work must not edit these files. If a scenario is wrong, fix `spec.md`
  first, then the test.

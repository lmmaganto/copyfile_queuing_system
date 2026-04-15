# SDE Review Queue

This repository is a lightweight review-tracking system for manuscripts, notebooks, and reproducibility checks.

It was designed for academic teams that need a simple way to coordinate first-pass and second-pass review work without adding a separate database or web application. Undergraduates and graduate reviewers use GitHub issues to claim work, record progress, and hand submissions from one review stage to the next.

## What the system does

- Tracks each submission as a GitHub issue
- Records review packages in the repository so work is visible and auditable
- Enforces a two-stage review flow with different reviewers at each stage
- Automates queue state changes and, when maintainer email settings are configured, final packaging and notification for tracked review folders and standalone review files

The review lifecycle is:

```text
queued -> review-1-active -> awaiting-review-2 -> review-2-active -> complete
```

## How teams use it

In practice, reviewers pick up work from the issue queue, complete or verify the associated notebook and manuscript materials, and move the package forward. The repository acts as the shared record of who reviewed what, when it was reviewed, and whether it is ready for the next stage.

This keeps the process quick to explain:

- New work enters the queue as an issue
- A first reviewer claims it and prepares the review package
- A second reviewer independently checks a tracked review folder or standalone review file
- Approval ends the reviewer workflow; repository automation may then finalize delivery if the maintainer setup is in place

## Documentation

- Reviewer workflow: [docs/USAGE.md](docs/USAGE.md)
- Reviewer step-by-step guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Maintainer setup: [docs/SETUP.md](docs/SETUP.md)

## Suggested Repository Description

Transparent, version-controlled system for coordinating two-stage reproducibility review of research manuscripts and computational materials.

## Why this approach

The system stays intentionally simple. GitHub provides authentication, history, storage, automation, and issue tracking, so the queue can remain transparent and easy to maintain while still supporting a formal review process.

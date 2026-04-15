# How Reviewers Use This System

This repository supports a two-stage review process for manuscripts and their associated computational materials.

The goal is straightforward: keep a clear record of who is reviewing each item, what stage it is in, and when it is ready to move forward.

## Day-to-day workflow

Each submission is represented by a GitHub issue. Reviewers interact with the queue by commenting on those issues.

| Command | Purpose |
|---|---|
| `/checkout` | Claim an item and move it into an active review state |
| `/release` | Return an item to the queue if you cannot continue |
| `/approve` | Complete the second review; downstream completion steps depend on repository automation and maintainer configuration |

The queue moves through these stages:

```text
queued -> review-1-active -> awaiting-review-2 -> review-2-active -> complete
```

## What first reviewers do

The first reviewer selects a queued item, reproduces or checks the submission materials, and prepares a review folder with the manuscript, notebook, metadata, and supporting outputs.

Once that work is merged, the item moves to `awaiting-review-2` so a second reviewer can independently confirm it.

## What second reviewers do

The second reviewer claims an item that is waiting for a follow-up review, re-runs or verifies the materials, and confirms that the package is complete.

The system prevents the same person from acting as both reviewer 1 and reviewer 2 when the first reviewer is recorded in the review metadata.

When the second reviewer approves the item, the reviewer workflow is finished. If the maintainer has configured email delivery, repository automation then marks the tracked folder or standalone file complete, closes the issue, and sends the package to the configured recipient.

## Why this is useful

- Review status is visible in one shared queue
- Reviewer assignments are recorded automatically
- Repository history provides an audit trail
- The process remains fast and easy to explain to new team members

## Where to go next

- For the full reviewer walkthrough, see [CONTRIBUTING.md](../CONTRIBUTING.md)
- For maintainer setup and configuration, see [SETUP.md](SETUP.md)

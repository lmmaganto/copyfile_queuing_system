# Reviewer Guide

This repository runs a two-stage review queue for SDE simulation manuscripts and their matching Jupyter notebooks. Every manuscript moves through these states:

```
queued  →  review-1-active  →  awaiting-review-2  →  review-2-active  →  complete
```

Each state is tracked by a **GitHub issue** with a corresponding label.

---

## Slash commands

Comment one of these on a review issue:

| Command | When | What it does |
|---|---|---|
| `/checkout` | On a `queued` or `awaiting-review-2` issue | Assigns you and moves the issue to the next "active" state |
| `/release`  | While you have something checked out | Hands it back to the queue |
| `/approve`  | On `review-2-active`, by the assigned second reviewer | Marks the review complete; if maintainer email settings are configured, automation then moves the tracked folder or file to `reviews/completed/`, emails the configured recipient, and closes the issue |

**Integrity rule:** the second reviewer **cannot** be the same person as the first reviewer when `reviewer_1` is recorded. The workflow checks this automatically for folder-based items with `metadata.yml`.

---

## Doing a first review

1. Find a `queued` issue and comment `/checkout`.
2. Reproduce the SDE simulations from the manuscript in a Jupyter notebook.
3. Create a folder `reviews/in-progress/<name>/` containing:
   - `<doi>.ipynb` — your notebook
   - `<manuscript>.pdf` — the manuscript PDF
   - `<output>.png` — at least one output figure (strongly encouraged)
   - `metadata.yml` — see template below
4. Open a PR with that folder. The `validate-submission` workflow will check the shape.
5. When the PR is merged, move the folder to `reviews/awaiting-review-2/<name>/` and update the issue body marker (or just label the issue `awaiting-review-2` and let a maintainer move it).

### `metadata.yml` template

```yaml
name: HBV
doi: 10.1007/s00332-022-09883-w
url: https://doi.org/10.1007/s00332-022-09883-w
notebook: 10.1007.s00332-022-09883-w.ipynb
manuscript: HBV.pdf
output_image: HBV Ouput.png
reviewer_1: your-github-username
reviewer_1_completed: 2026-04-08
reviewer_2: null
state: awaiting-review-2
```

---

## Doing a second review

1. Find an `awaiting-review-2` issue and comment `/checkout`. (You'll be blocked if you were the first reviewer when that reviewer is recorded in metadata.)
2. Independently re-run the notebook, verify it matches the manuscript's claims.
3. If there are changes, open a PR with your updates. For folder-based items, add `review2.md` to the folder with your notes.
4. Comment `/approve` on the issue.
5. Your reviewer task ends there. If maintainer email delivery is configured, automation finalizes the tracked review folder or standalone file and closes the issue.

---

## Adding a new manuscript to the queue

Open a new issue using the **"Add manuscript to review queue"** template. Provide the short name and DOI/URL. It enters as `queued`.

---

## Folder shape (enforced)

Every folder under `reviews/` must contain:
- exactly one `.ipynb`
- exactly one `.pdf`
- a `metadata.yml`
- (recommended) at least one image file

Submissions that don't match will fail PR validation.

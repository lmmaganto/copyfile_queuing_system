# SDE Manuscript Review Queue

A GitHub-native queueing system for two-stage peer review of stochastic differential equation manuscripts and their matching Jupyter notebooks.

> **Reviewers:** see [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to claim, submit, and approve reviews.

---

## How it works

Every manuscript becomes a GitHub Issue that flows through five states via labels:

```
queued  →  review-1-active  →  awaiting-review-2  →  review-2-active  →  complete
```

Reviewers self-select using slash commands (`/checkout`, `/release`, `/approve`) on issues. Workflows enforce the **two-distinct-reviewers integrity rule**, validate submitted folder shape, and on completion automatically zip the review package and email it to the designated address.

---

## Repository layout

```
queue/
  pending.csv               # mirror of queued items (issue is the source of truth)
reviews/
  in-progress/<name>/       # checked out for first review
  awaiting-review-2/<name>/ # first review done, waiting for second reviewer
  completed/<name>/         # finalized (auto-moved here on /approve)
.github/
  ISSUE_TEMPLATE/
    add-to-queue.yml        # form to add a new DOI/URL
  workflows/
    manage-queue.yml          # /checkout /release /approve
    validate-submission.yml   # PR shape check
    notify-on-complete.yml    # zip + email + close
    bootstrap-seed-issues.yml # one-shot: create issues for existing folders
```

Each review folder contains: `<doi>.ipynb`, `<manuscript>.pdf`, output image(s), and `metadata.yml`.

---

## First-time setup (one-time, by the repo owner)

### 1. Create labels

The workflows depend on these labels existing. Create them in **Issues → Labels** (or via `gh label create`):

| Label | Color suggestion |
|---|---|
| `queued` | `#cccccc` |
| `review-1-active` | `#fbca04` |
| `awaiting-review-2` | `#0e8a16` |
| `review-2-active` | `#fbca04` |
| `complete` | `#5319e7` |

Quick one-liner with the GitHub CLI:

```bash
gh label create queued            --color cccccc
gh label create review-1-active   --color fbca04
gh label create awaiting-review-2 --color 0e8a16
gh label create review-2-active   --color fbca04
gh label create complete          --color 5319e7
```

### 2. Configure secrets

In **Settings → Secrets and variables → Actions**, add:

| Secret | Example | Notes |
|---|---|---|
| `NOTIFY_TO` | `eosborn@cpp.edu` *(testing)* / `Timothy.Sego@medicine.ufl.edu` *(production)* | Recipient of completed packages |
| `SMTP_SERVER` | `smtp.gmail.com` | Any SMTP server you control |
| `SMTP_PORT` | `465` | |
| `SMTP_USER` | `your-bot@gmail.com` | Sender address |
| `SMTP_PASS` | *(app password)* | For Gmail, create at https://myaccount.google.com/apppasswords |

> **Tip:** during testing, point `NOTIFY_TO` at your own email (`eosborn@cpp.edu`). Switch to `Timothy.Sego@medicine.ufl.edu` only once you've verified the full flow end-to-end.

### 3. Seed the existing 5 reviews into the queue

The 5 manuscripts under `reviews/awaiting-review-2/` need GitHub Issues for tracking. Run the bootstrap workflow once:

**Actions tab → "Bootstrap Seed Issues" → Run workflow**

It scans `reviews/awaiting-review-2/` and `reviews/in-progress/`, creates one issue per folder with the correct label, and skips any folder that already has a tracking issue. Safe to re-run.

### 4. Test the flow end-to-end

1. Pick one of the seeded `awaiting-review-2` issues (e.g., HBV).
2. From a **second account** (since you are recorded as `reviewer_1` for all 5), comment `/checkout`.
3. Comment `/approve`.
4. Verify: the folder moves to `reviews/completed/HBV/`, the issue closes, and `eosborn@cpp.edu` receives the zipped package.

If anything fails, check the workflow logs in the Actions tab.

---

## Transferring ownership later

When you're ready to hand this off to a UF organization:

1. **Settings → General → Danger Zone → Transfer ownership.** Type the destination org. Everything moves: code, issues, labels, PRs, secrets, Actions history.
2. **Switch from collaborator-check to team-check.** In `.github/workflows/manage-queue.yml`, find the line:
   ```js
   // TODO: switch to team check after transfer to org.
   ```
   Replace the `checkCollaborator` block with the `teams.getMembershipForUserInOrg` block shown directly above it. Set the team slug (e.g., `sde-reviewers`).
3. **Update `NOTIFY_TO`** secret to `Timothy.Sego@medicine.ufl.edu`.
4. **Update `.github/ISSUE_TEMPLATE/config.yml`** so the contributor-guide link points at the new org URL.

That's it. The new org owns and operates the system.

---

## Authorization model

- **Currently:** any repo collaborator can run slash commands.
- **After org transfer:** any member of the designated GitHub team can run slash commands.

To add or remove reviewers, just change collaborator/team membership — no code changes required.

---

## Why this design

- **No servers, no database, no hosting bill.** GitHub provides storage, auth, audit log, notifications, and compute (Actions) for free on private repos within the included minutes.
- **One-click ownership transfer.** When the project moves to an institutional org, every issue, label, secret, and bit of history goes with it.
- **All state lives in two places** — the issue (current stage) and `metadata.yml` (reviewer identities). Easy to read, easy to repair by hand if anything ever goes wrong.

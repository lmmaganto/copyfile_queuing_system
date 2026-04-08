# Local Setup Guide: SDE Manuscript Review Queue

This guide walks you through setting up the review queue repository on your local machine and working with it in Visual Studio Code (VS Code).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Cloning the Repository](#cloning-the-repository)
3. [Repository Structure](#repository-structure)
4. [Setting Up Your Environment](#setting-up-your-environment)
5. [Opening in VS Code](#opening-in-vs-code)
6. [Working Without GitHub Copilot](#working-without-github-copilot)
7. [Working With GitHub Copilot](#working-with-github-copilot)
8. [Common Workflows](#common-workflows)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have the following installed:

- **Git** - [Download Git](https://git-scm.com/downloads)
- **Visual Studio Code** - [Download VS Code](https://code.visualstudio.com/)
- **Python 3.x** (via Anaconda/Miniconda recommended) - [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **GitHub Account** with access to the repository (must be added as a collaborator)

### Recommended VS Code Extensions

- Python (Microsoft)
- Jupyter (Microsoft)
- GitHub Pull Requests and Issues (GitHub)
- GitLens (optional, but helpful for Git visualization)
- **GitHub Copilot** (optional - requires subscription)
- **GitHub Copilot Chat** (optional - requires Copilot subscription)

---

## Cloning the Repository

### Option 1: Using Git Command Line

1. **Open a terminal** (PowerShell, Command Prompt, or Git Bash)

2. **Navigate to where you want to store the repository:**
   ```bash
   cd C:\Users\YourUsername\Documents
   ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/Lizo-RoadTown/file_queuing_system.git
   ```

4. **Navigate into the repository:**
   ```bash
   cd file_queuing_system
   ```

### Option 2: Using VS Code

1. **Open VS Code**

2. **Press `Ctrl+Shift+P`** to open the Command Palette

3. **Type** `Git: Clone` and select it

4. **Paste the repository URL:**
   ```
   https://github.com/Lizo-RoadTown/file_queuing_system
   ```

5. **Choose a local folder** where you want to save it

6. **When prompted, click "Open"** to open the cloned repository

### Authentication

If the repository is private, Git will prompt you to authenticate:
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (PAT), not your GitHub password
  - Generate a PAT: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Required scopes: `repo` (full control of private repositories)

---

## Repository Structure

```
file_queuing_system/
├── .github/                 # GitHub Actions workflows
│   └── workflows/          # Automation for queue management
├── docs/                   # Documentation
│   ├── SETUP.md            # Maintainer setup guide
│   └── LOCAL_SETUP_GUIDE.md # This file
├── queue/                  # Queue management scripts
├── reviews/                # Review submissions
│   ├── in-progress/       # First reviews in progress
│   ├── awaiting-review-2/ # Ready for second review
│   └── completed/         # Finalized reviews
├── CONTRIBUTING.md         # Reviewer workflow guide
├── README.md              # Project overview
└── .gitignore             # Git ignore rules
```

---

## Setting Up Your Environment

### Create a Conda Environment

The review workflow uses Jupyter notebooks to reproduce SDE simulations. You'll need a Python environment with the necessary scientific computing libraries.

1. **Create an environment file** (`setup/env.yml`):

   First, create the setup directory if it doesn't exist:
   ```bash
   mkdir setup
   ```

   Then create `setup/env.yml`:
   ```yaml
   name: sde-review
   channels:
     - conda-forge
   dependencies:
     - python=3.11
     - numpy<2
     - matplotlib
     - scipy
     - pandas
     - tqdm
     - notebook
     - ipywidgets
     - ipyevents
     - nomkl
     - pip
     - pip:
         - diffrax
         - jax==0.6
   ```

2. **Create the environment:**
   ```bash
   conda env create -f setup/env.yml
   ```

3. **Activate the environment:**
   ```bash
   conda activate sde-review
   ```

### Install Jupyter Kernel

After activating the environment, ensure Jupyter can use it:

```bash
python -m ipykernel install --user --name sde-review --display-name "Python (SDE Review)"
```

---

## Opening in VS Code

### Method 1: From Command Line

1. **Navigate to the repository folder:**
   ```bash
   cd C:\path\to\file_queuing_system
   ```

2. **Launch VS Code:**
   ```bash
   code .
   ```

### Method 2: From VS Code

1. **Open VS Code**
2. **File → Open Folder**
3. **Navigate to** `file_queuing_system` and click **Select Folder**

### Configure VS Code Python Environment

1. **Open the Command Palette** (`Ctrl+Shift+P`)

2. **Type** `Python: Select Interpreter`

3. **Choose** `Python (SDE Review)` or the `sde-review` conda environment

4. **Create `.vscode/settings.json`** (if it doesn't exist):
   ```json
   {
       "python.defaultInterpreterPath": "conda://sde-review",
       "jupyter.notebookFileRoot": "${workspaceFolder}/reviews",
       "python.analysis.extraPaths": [
           "${workspaceFolder}/reviews"
       ],
       "files.exclude": {
           "**/__pycache__": true,
           "**/.ipynb_checkpoints": true
       }
   }
   ```

---

## Working Without GitHub Copilot

If you're **not using** GitHub Copilot, you'll write all code manually. Here's how to work efficiently:

### Setting Up for Manual Development

1. **Familiarize yourself with the repository:**
   - Read [`README.md`](../README.md)
   - Read [`CONTRIBUTING.md`](../CONTRIBUTING.md)
   - Review existing notebooks in `reviews/completed/` for examples

2. **Use VS Code features:**
   - **IntelliSense:** Auto-completion for Python (press `Ctrl+Space`)
   - **Linting:** Install `pylint` or `flake8` to catch errors
   - **Debugging:** Set breakpoints in notebooks (click left of line numbers)

3. **Working with Jupyter Notebooks:**
   - **Create a new notebook:** Right-click `reviews/in-progress/` → New File → `your-review.ipynb`
   - **Select kernel:** Click kernel picker (top-right) → Choose `Python (SDE Review)`
   - **Run cells:** `Shift+Enter`
   - **Add cells:** Hover between cells → Click `+ Code` or `+ Markdown`

4. **Common keyboard shortcuts:**
   - `Ctrl+Enter`: Run current cell
   - `Shift+Enter`: Run cell and move to next
   - `Ctrl+Shift+P`: Command Palette
   - `Ctrl+B`: Toggle sidebar
   - `Ctrl+`` `: Toggle terminal

5. **Reference documentation:**
   - Keep browser tabs open for:
     - [NumPy documentation](https://numpy.org/doc/)
     - [Matplotlib documentation](https://matplotlib.org/stable/index.html)
     - [SciPy documentation](https://docs.scipy.org/doc/scipy/)
     - [JAX documentation](https://jax.readthedocs.io/)

### Typical Workflow (No Copilot)

1. **Claim an issue** by commenting `/checkout`
2. **Create a folder** `reviews/in-progress/<manuscript-name>/`
3. **Download the manuscript PDF** and place it in the folder
4. **Create a Jupyter notebook** to reproduce the SDE model:
   - Import libraries
   - Define the SDE system
   - Set parameters from the manuscript
   - Run simulations
   - Generate plots matching manuscript figures
5. **Save output images** as PNG files
6. **Create `metadata.yml`** (see template in [`CONTRIBUTING.md`](../CONTRIBUTING.md))
7. **Open a Pull Request** with your changes
8. **Wait for PR validation** (GitHub Actions will check folder structure)
9. **Merge PR** and update the issue

---

## Working With GitHub Copilot

If you have **GitHub Copilot** installed, you can leverage AI assistance for faster development.

### Installing GitHub Copilot

1. **Install the extension:**
   - Open VS Code Extensions (`Ctrl+Shift+X`)
   - Search for "GitHub Copilot"
   - Click **Install**
   - Sign in with your GitHub account (requires active Copilot subscription)

2. **Install GitHub Copilot Chat (optional but recommended):**
   - Search for "GitHub Copilot Chat"
   - Click **Install**

### Using Copilot for Code Suggestions

Copilot provides **inline code suggestions** as you type:

1. **Start typing** and Copilot will suggest completions (shown in gray text)
2. **Accept suggestion:** Press `Tab`
3. **See alternative suggestions:** Press `Alt+]` (next) or `Alt+[` (previous)
4. **Reject suggestion:** Keep typing or press `Esc`

### Using Copilot Chat

Copilot Chat provides conversational AI assistance:

1. **Open Copilot Chat:**
   - Click the chat icon in the sidebar, OR
   - Press `Ctrl+Shift+I`

2. **Ask questions:**
   - "How do I implement a stochastic differential equation in Python using NumPy?"
   - "Generate a plot comparing two SDE trajectories with confidence intervals"
   - "Explain what this code does" (select code first)

3. **Inline chat:**
   - Press `Ctrl+I` to open inline chat
   - Ask Copilot to modify selected code directly

### Typical Workflow (With Copilot)

1. **Claim an issue** by commenting `/checkout`
2. **Create a folder** `reviews/in-progress/<manuscript-name>/`
3. **Open Copilot Chat** and ask:
   ```
   I need to reproduce an SDE model from a research paper. The model is:
   dS/dt = -βSI/N + ξ₁(t)
   dI/dt = βSI/N - γI + ξ₂(t)
   
   where ξ₁, ξ₂ are Gaussian white noise terms. Can you help me set up a 
   Jupyter notebook with the imports and basic structure?
   ```

4. **Create the notebook** `your-review.ipynb` and paste Copilot's suggested code
5. **Iterate with Copilot:**
   - "Add parameter values: β=0.5, γ=0.1, N=1000"
   - "Generate a plot showing S(t) and I(t) over 100 time steps"
   - "Add confidence bounds from 100 stochastic realizations"

6. **Review and refine** the generated code
7. **Save output images**
8. **Ask Copilot to create metadata.yml:**
   ```
   Create a metadata.yml file with these details:
   - name: SIR-Stochastic
   - doi: 10.xxxx/xxxxx
   - reviewer_1: my-github-username
   - state: awaiting-review-2
   ```

9. **Open a Pull Request**
10. **Iterate with Copilot if validation fails:**
    - Select error message
    - Press `Ctrl+I`
    - Type "Fix this validation error"

### Copilot Best Practices

✅ **DO:**
- Use Copilot for boilerplate code (imports, plot setup)
- Ask Copilot to explain unfamiliar code in existing reviews
- Use Copilot to generate test data or parameter sweeps
- Let Copilot help with documentation and comments

❌ **DON'T:**
- Blindly accept all suggestions (always review generated code)
- Trust Copilot for mathematical correctness (verify equations against the manuscript)
- Skip manual testing (run the notebook to ensure it works)
- Ignore warnings or errors in generated code

---

## Common Workflows

### Starting a First Review

1. **Find a `queued` issue** in the Issues tab
2. **Comment** `/checkout`
3. **Create your review folder:**
   ```bash
   mkdir -p reviews/in-progress/YourManuscriptName
   cd reviews/in-progress/YourManuscriptName
   ```
4. **Create your notebook** and reproduce the SDE model
5. **Add the manuscript PDF**
6. **Create `metadata.yml`**
7. **Commit and push:**
   ```bash
   git add reviews/in-progress/YourManuscriptName/
   git commit -m "First review: YourManuscriptName"
   git push origin main
   ```
8. **Open a PR** via GitHub UI or VS Code GitHub extension
9. **Wait for CI validation** to pass
10. **Merge the PR**
11. **Update the issue** to `awaiting-review-2`

### Starting a Second Review

1. **Find an `awaiting-review-2` issue**
2. **Comment** `/checkout` (you'll be blocked if you did the first review)
3. **Navigate to the existing folder:**
   ```bash
   cd reviews/awaiting-review-2/ManuscriptName
   ```
4. **Open the notebook** and re-run all cells
5. **Verify outputs match** the manuscript claims
6. **(Optional) Add `review2.md`** with notes
7. **Comment** `/approve` on the issue
8. **Done!** The automation zips the package, emails it, and closes the issue

### Syncing Changes from GitHub

If other reviewers have pushed changes:

```bash
git pull origin main
```

Or in VS Code:
- Click the Source Control icon (left sidebar)
- Click the ⋯ menu → Pull

### Creating a Branch for Your Work (Recommended)

Instead of working directly on `main`, use a branch:

1. **Create and switch to a new branch:**
   ```bash
   git checkout -b review/manuscript-name
   ```

2. **Work on your review**

3. **Push the branch:**
   ```bash
   git push origin review/manuscript-name
   ```

4. **Open a PR** from your branch to `main`

---

## Troubleshooting

### Cannot Clone Repository (Permission Denied)

**Problem:** `fatal: repository not found` or `permission denied`

**Solution:**
- Verify you've been added as a collaborator
- Use a Personal Access Token (PAT) instead of your password
- Check your GitHub username is correct

### Conda Environment Not Found in VS Code

**Problem:** The `sde-review` environment doesn't appear in the kernel picker

**Solution:**
1. Activate the environment in terminal:
   ```bash
   conda activate sde-review
   ```
2. Install the kernel:
   ```bash
   python -m ipykernel install --user --name sde-review
   ```
3. Reload VS Code window (`Ctrl+Shift+P` → `Developer: Reload Window`)

### Imports Fail in Jupyter Notebook

**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
1. Check you've selected the correct kernel (top-right of notebook)
2. Click the kernel name → Select `Python (SDE Review)`
3. If still failing, reinstall the environment:
   ```bash
   conda env remove -n sde-review
   conda env create -f setup/env.yml
   ```

### Git Push Rejected

**Problem:** `error: failed to push some refs`

**Solution:**
- Pull first: `git pull origin main`
- Resolve any merge conflicts
- Then push: `git push origin main`

### PR Validation Fails

**Problem:** GitHub Actions workflow "Validate Submission" fails

**Solution:**
- Check the workflow logs in the Actions tab
- Common issues:
  - Missing `metadata.yml`
  - Folder in wrong location (`in-progress` vs `awaiting-review-2`)
  - Missing `.ipynb` or `.pdf` file
  - Invalid YAML syntax in `metadata.yml`
- Fix the issues and push again

### Copilot Not Working

**Problem:** Copilot suggestions not appearing

**Solution:**
1. Check Copilot status (bottom-right, look for Copilot icon)
2. Verify you're signed in: `Ctrl+Shift+P` → `GitHub Copilot: Sign In`
3. Check your subscription is active on GitHub
4. Restart VS Code
5. Check Copilot is enabled for your file type:
   - `Ctrl+Shift+P` → `Preferences: Open Settings (UI)`
   - Search "Copilot enable"
   - Ensure `*` is in the enabled languages

### OneDrive Sync Issues

**Problem:** Files syncing across computers causing conflicts (based on your workflow)

**Solution:**
- **Don't sync the conda environment** across machines
- Add to `.gitignore` (already done for Python):
  ```
  __pycache__/
  .ipynb_checkpoints/
  *.pyc
  ```
- Exclude the conda environment folder from OneDrive sync:
  - Right-click the environment folder
  - **Free up space** (keeps it local only)

---

## Additional Resources

- **GitHub Docs:** [Working with Pull Requests](https://docs.github.com/en/pull-requests)
- **VS Code Docs:** [Working with Jupyter Notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- **Git Cheat Sheet:** [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- **Conda Cheat Sheet:** [Conda Commands](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

---

## Questions?

If you encounter issues not covered here:
1. Check the [repository README](../README.md)
2. Review [CONTRIBUTING.md](../CONTRIBUTING.md)
3. Open an issue with the `question` label
4. Contact a repository maintainer

Happy reviewing! 🎉

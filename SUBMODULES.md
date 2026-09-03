# SportsMatrix Git Submodule Strategy & Management Guide 🛠️

This document outlines the **Git Submodule Architecture** for the SportsMatrix platform and provides a step-by-step guide for managing code changes across subservices and the root repository.

---

## 🏗️ Architecture & Module Strategy

SportsMatrix uses Git submodules to organize its multi-sport prediction suite under the `sportservices/` directory.

### Why Submodules?
1. **Decoupled Microservice Ownership**: Each sport engine (`Moneyball`, `NetPredict`, `NoFreeLocks`, `SaturdaySlate`) is an independent codebase with its own Git repository, unit tests, and release cycle.
2. **Unified Platform Integration**: The root `SportsMatrix` repository references specific commit hashes of each submodule, combining all 4 engines into a single unified FastAPI gateway and Pydantic AI Chatbot.
3. **Clean Version Control**: Fixes or enhancements to a specific sport service can be developed, tested, and pushed independently without cluttering the main platform history.

### Submodule Repository Mappings

| Submodule Path | Service Name | Target Sport / Leagues | GitHub Repository |
| :--- | :--- | :--- | :--- |
| `sportservices/moneyball` | **Moneyball** | MLB Baseball | [JasonDoug/Moneyball](https://github.com/JasonDoug/Moneyball) |
| `sportservices/netpredict` | **NetPredict** | Basketball (NBA, WNBA, NCAAM, NCAAW) | [JasonDoug/NetPredict](https://github.com/JasonDoug/NetPredict) |
| `sportservices/nofreelocks` | **NoFreeLocks** | NFL Football | [JasonDoug/NoFreeLocks](https://github.com/JasonDoug/NoFreeLocks) |
| `sportservices/saturdayslate` | **SaturdaySlate** | College Football (CFB) | [JasonDoug/SaturdaySlate](https://github.com/JasonDoug/SaturdaySlate) |

---

## 🚀 How to Manage Changes (Step-by-Step Workflow)

### 1. Cloning a Fresh Copy

Always clone using the `--recurse-submodules` flag so Git fetches all submodule code automatically:

```bash
git clone --recurse-submodules https://github.com/JasonDoug/SportsMatrix.git
cd SportsMatrix
```

If you or a contributor cloned without `--recurse-submodules`, initialize and pull submodules with:

```bash
git submodule update --init --recursive
```

---

### 2. Making & Pushing Changes to a Submodule

When modifying code inside a specific sport service (e.g. `sportservices/nofreelocks`):

#### Step A: Navigate to the Submodule
```bash
cd sportservices/nofreelocks
```

#### Step B: Ensure You Are on Branch `main`
Git submodules often check out commits in a "detached HEAD" state. Always check out `main` before editing:
```bash
git checkout main
```

#### Step C: Make Code Edits & Run Tests
Make your changes and verify with pytest:
```bash
pytest tests/ -v
```

#### Step D: Commit & Push to the Submodule's Remote Repository
```bash
git add .
git commit -m "feat: Add new model feature / fix endpoint"
git push origin main
```
> ⚠️ **Important**: Pushing inside the submodule updates `https://github.com/JasonDoug/NoFreeLocks.git`.

#### Step E: Update the Root SportsMatrix Reference Pointer
Return to the root `SportsMatrix` directory and commit the updated submodule hash:
```bash
cd ../..
git add sportservices/nofreelocks
git commit -m "chore: Update NoFreeLocks submodule pointer"
git push origin main
```

---

### 3. Updating Submodules to Their Latest Remote Commits

To pull the latest commits for **all** submodules from their respective GitHub repositories:

```bash
# Pull latest changes for all submodules recursively
git submodule update --remote --recursive

# Commit the updated submodule pointers in the root repository
git add sportservices/
git commit -m "chore: Update all sportservice submodule pointers to latest main"
git push origin main
```

---

## 🔍 Useful Git Submodule Commands

| Task | Command |
| :--- | :--- |
| **Check Submodule Commit Status** | `git submodule status` |
| **List Submodule Mappings** | `cat .gitmodules` |
| **Update All Submodules from Remote** | `git submodule update --remote --recursive` |
| **Checkout `main` Across All Submodules** | `git submodule foreach 'git checkout main'` |
| **Run `git status` Across All Submodules** | `git submodule foreach 'git status'` |

---

## ⚡ Summary Checklist for Modifying a Submodule

1. `cd sportservices/<submodule-name>`
2. `git checkout main`
3. Edit code & pass tests.
4. `git add . && git commit -m "..." && git push origin main`
5. `cd ../..`
6. `git add sportservices/<submodule-name> && git commit -m "chore: Update submodule pointer" && git push origin main`

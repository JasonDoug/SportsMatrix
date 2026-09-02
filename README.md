# SportsMatrix 🏆

**SportsMatrix** is a unified sports prediction and analytics platform integrating specialized machine learning and statistical modeling services across multiple professional and collegiate sports.

## 📦 Architecture & Sport Services

SportsMatrix organizes its underlying engine components using Git submodules located under `sportservices/`:

| Module | Description | Repository |
| :--- | :--- | :--- |
| **Moneyball** (`sportservices/moneyball`) | MLB betting & analytics engine with web frontend, FastAPI backend, and daily game prediction pipelines. | [JasonDoug/Moneyball](https://github.com/JasonDoug/Moneyball) |
| **NetPredict** (`sportservices/netpredict`) | Unified basketball prediction service covering NBA, WNBA, NCAAM, and NCAAW. | [JasonDoug/NetPredict](https://github.com/JasonDoug/NetPredict) |
| **NoFreeLocks** (`sportservices/nofreelocks`) | NFL game prediction system combining tabular ML (XGBoost, LightGBM, CatBoost) and LLM-based news explanations. | [JasonDoug/NoFreeLocks](https://github.com/JasonDoug/NoFreeLocks) |
| **SaturdaySlate** (`sportservices/saturdayslate`) | College Football (CFB) prediction and ratings engine. | [JasonDoug/SaturdaySlate](https://github.com/JasonDoug/SaturdaySlate) |

---

## 🚀 Getting Started

### 1. Cloning the Repository

To clone SportsMatrix along with all submodule services:

```bash
git clone --recurse-submodules https://github.com/JasonDoug/SportsMatrix.git
cd SportsMatrix
```

If you have already cloned the repository without submodules, initialize and update them:

```bash
git submodule update --init --recursive
```

---

## 🛠️ Submodule Management

To update all submodules to their latest remote commits:

```bash
git submodule update --remote --recursive
```

---

## 📄 License

Apache License 2.0

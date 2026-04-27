# Azure ML Pipeline

## Overview

An end-to-end NLP pipeline on Azure ML that preprocesses app review text, trains a Linear Regression model to predict reviewer ratings, and scores on a held-out test set.

**Pipeline stages:**

```
raw data → preprocess_text → split_data → train → score
```

| Step | Component | What it does |
|---|---|---|
| 1 | `preprocess_text` | NLTK cleaning: stop words, lemmatization, lowercasing, URL/email/number removal |
| 2 | `split_data` | 80/20 train/test split via sklearn |
| 3 | `train` | TF-IDF + OLS Linear Regression, saves `model.pkl` |
| 4 | `score` | Loads model, appends `score` column to test set |

---

## Repository Structure

```
src/
  components/
    conda.yml                      # shared environment (pandas, sklearn, nltk, joblib)
    preprocess_text/
      preprocess_text.py
      preprocess_text.yml
    split_data/
      split_data.py
      split_data.yml
    train/
      train.py
      train.yml
    score/
      score.py
      score.yml
  pipeline.yml                     # top-level pipeline job
  run_pipeline.sh                  # local execution helper
```

Each component is self-contained: its Python script and YAML live in the same directory (`code: .`). No custom invoker or Designer module wrappers are needed.

---

## CI/CD

Pushing to `baseline` triggers `.github/workflows/deploy-aml.yml`, which:

1. **Versions** all component and pipeline YAMLs using `github.run_number` (e.g. `1.0.42`)
2. **Purges** local CSVs/parquet files to keep code snapshots under 100 KB
3. **Registers** each component with retry logic (handles Azure East US transient errors)
4. **Submits** `src/pipeline.yml` as a pipeline job

The workflow only triggers on changes under `src/components/**` or `src/pipeline.yml`.

---

## Local Execution

### Prerequisites

```bash
az login
az extension add -n ml
az account set --subscription "d68c0c8b-ff0f-447d-8a70-7eca5e8f7940"
```

### Register a component manually

```bash
VERSION="1.0.local"
sed -i "s/SET_BY_GITHUB_ACTIONS/$VERSION/g" src/components/preprocess_text/preprocess_text.yml

az ml component create --file src/components/preprocess_text/preprocess_text.yml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b
```

### Submit the pipeline

```bash
sed -i "s/VERSION_PLACEHOLDER/$VERSION/g" src/pipeline.yml

az ml job create --file src/pipeline.yml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b \
    --stream
```

Or use the helper script (handles versioning and all four components):

```bash
export AZURE_RG="dsc592_spring26_group_b"
export AZURE_WORKSPACE="dsc592_spring26_group_b"
export BUILD_VERSION="1.0.local"
bash src/run_pipeline.sh
```

---

## Infrastructure Setup

### Service Principal

```bash
az ad sp create-for-rbac --name "github-actions-ml-admin" \
    --role contributor \
    --scopes /subscriptions/d68c0c8b-ff0f-447d-8a70-7eca5e8f7940/resourceGroups/dsc592_spring26_group_b \
    --sdk-auth
```

Paste the JSON output into GitHub Secrets as `AZURE_CREDENTIALS`.

### Compute Cluster

```bash
az ml compute create --name "github-cluster" \
     --size "Standard_DS3_v2" \
     --min-instances 0 \
     --max-instances 2 \
     --type amlcompute \
     --resource-group dsc592_spring26_group_b \
     --workspace-name dsc592_spring26_group_b
```

### Role Assignments

If you encounter compute access errors, add the **AzureML Data Scientist** role to the Service Principal in the workspace IAM settings (the `contributor` role at resource group level is not always sufficient).

---

## Troubleshooting

**TransientError / timeout on component registration** — Azure East US management plane under load. The workflow retries 3 times with 10s delay. If it still fails, wait a few minutes and re-run the action.

**MissingSubscription errors on Windows Git Bash**
```bash
export MSYS_NO_PATHCONV=1
```

**Component upload too large** — Ensure `data.csv` and other large files are listed in `.amlignore`. Code snapshots must stay under 100 KB.

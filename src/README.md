# AzureML Invoker



# Azure ML CI/CD & Local Execution Guide

This project uses **GitHub Actions** to automate the registration of Azure ML Components and the submission of pipeline jobs. This ensures that every code change is validated in the cloud using a consistent environment.

## 🚀 The CI/CD Pipeline

The automation is triggered whenever code is pushed to the `baseline` branch (specifically within the `src/` directory).

### How it Works
1. **Authentication**: Uses a Service Principal with Contributor access to the `dsc592_spring26_group_b` resource group.
2. **Dynamic Versioning**: Every run generates a unique version number (e.g., `1.0.42`) based on the GitHub Run ID. This bypasses Azure's component immutability rules.
3. **Registration**: Registers the `preprocess_text_custom` component using the `azureml:AzureML-Designer:89` curated environment.
4. **Smoke Test**: Automatically submits a job to the `github-cluster` to verify that the code change hasn't broken the preprocessing logic.



---

## 💻 Local Execution

If you are developing locally and want to trigger a job without pushing to GitHub, follow these steps.

### 1. Prerequisites
Ensure you have the Azure CLI and the ML extension installed:
```bash
az login
az extension add -n ml
az account set --subscription "d68c0c8b-ff0f-447d-8a70-7eca5e8f7940"

```

### 2. Manual Component Registration
Because components are immutable, you must increment the version number in preprocess_text.yaml manually or use a timestamp:

``` bash
az ml component create --file preprocess_text.yaml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b

```


### 3 Submitting a Job
Once the component is registered, update the component: line in run_preprocess.yaml to match the version you just created, then run:

```bash
az ml job create --file run_preprocess.yaml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b \
    --stream

```


### Common CLI errors in Git Bash

If you encounter MissingSubscription errors while running commands in Git Bash, disable path conversion:

```bash
MSYS_NO_PATHCONV=1 az ml ...
```

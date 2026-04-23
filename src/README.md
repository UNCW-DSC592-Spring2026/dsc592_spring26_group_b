# AzureML Invoker

## 🚀 Azure ML CI/CD & Pipeline Guide

This project uses **GitHub Actions** to automate the registration of Azure ML Components and the submission of pipeline jobs. This ensures that every code change is validated in the cloud using a consistent environment.

### The CI/CD Workflow
The automation is triggered whenever code is pushed to the `baseline` branch.
1. **Dynamic Versioning**: Every run generates a unique version (e.g., `1.0.12`) using the GitHub Run ID, replacing `SET_BY_GITHUB_ACTIONS` and `VERSION_PLACEHOLDER` in your YAMLs.
2. **Payload Optimization**: The workflow automatically purges large local datasets (like `data.csv`) to keep the component code size under 100KB, preventing **TransientError** timeouts.
3. **Resilient Registration**: Uses a retry loop to handle Azure East US management plane hiccups.
4. **End-to-End Test**: Submits `run_pipeline.yaml` to execute the full Preprocess -> Split -> Train -> Score graph.

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
Before submitting a job, you must register your modified components. You can use a timestamp to ensure the version is unique:
```bash
# Example for Preprocess component
az ml component create --file src/modules/preprocessing/preprocess_text.yaml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b
```

### 3. Submitting the Pipeline
Update the `component:` version in `run_pipeline.yaml` to match the version you just created, then run:
```bash
az ml job create --file run_pipeline.yaml \
    --resource-group dsc592_spring26_group_b \
    --workspace-name dsc592_spring26_group_b \
    --stream
```


Since you used the `--sdk-auth` flag and created the cluster via the CLI, your setup is technically "admin-level" for the Resource Group. However, for a clean and professional **README**, you should document how to verify these permissions and ensure the compute cluster is properly scoped for the GitHub Service Principal.

Add this section to your **README** to explain the infrastructure setup:

---

## 🏗️ Infrastructure & Permissions Setup

This project requires a **Service Principal** for GitHub Actions and a **dedicated compute cluster** in Azure ML.

### 1. Create the Service Principal (SP)
To allow GitHub to manage resources, we created an SP with the `--sdk-auth` flag. This generates the JSON block required for the `AZURE_CREDENTIALS` GitHub Secret.

```bash
az ad sp create-for-rbac --name "github-actions-ml-admin" \
    --role contributor \
    --scopes /subscriptions/d68c0c8b-ff0f-447d-8a70-7eca5e8f7940/resourceGroups/dsc592_spring26_group_b \
    --sdk-auth
```

> **Note:** Copy the resulting JSON output and paste it into your GitHub Repository Secrets as `AZURE_CREDENTIALS`.

### 2. Provision the Compute Cluster
The pipeline is configured to run on a cluster named `github-cluster`. We use `Standard_DS3_v2` instances to provide enough memory for text preprocessing and model training.

```bash
az ml compute create --name "github-cluster" \
     --size "Standard_DS3_v2" \
     --min-instances 0 \
     --max-instances 2 \
     --type amlcompute \
     --resource-group dsc592_spring26_group_b \
     --workspace-name dsc592_spring26_group_b
```

### 3. Verify Role Assignments
While the `contributor` role is assigned at the Resource Group level, ensure the Service Principal has permissions to specifically interact with the Machine Learning Workspace. In the Azure Portal:
1. Navigate to your **Machine Learning Workspace**.
2. Select **Access Control (IAM)** -> **Role Assignments**.
3. Confirm `github-actions-ml-admin` is listed. 
4. If you encounter "Compute Access" errors, manually add the **AzureML Data Scientist** role to the Service Principal for that workspace.


---

## 🐳 Docker Execution

You can use the provided Dockerfile to run the entire orchestration logic (versioning, registration, and submission) from a container.

### 1. Build the Orchestrator
```bash
docker build -t aml-pipeline-runner .
```

### 2. Run the Pipeline
Pass your Azure environment details as variables. Note that you must be authenticated (or use a Service Principal login inside the script):
```bash
docker run -e AZURE_RG="dsc592_spring26_group_b" \
           -e AZURE_WORKSPACE="dsc592_spring26_group_b" \
           -e BUILD_VERSION="1.0.manual" \
           aml-pipeline-runner
```

---

## ⚠️ Troubleshooting

### MissingSubscription Errors (Git Bash)
If you encounter path conversion errors in Windows Git Bash, use:
```bash
export MSYS_NO_PATHCONV=1
# Then run your az commands
```

### TransientError / Service Invocation Timeout
If the CLI hangs for 10 seconds and fails:
1. **Check file size**: Ensure `data.csv` or other large files are in `.amlignore`. The upload should be **< 1MB**.
2. **Check Azure Status**: This often indicates the `eastus` Management Registry is under high load. Wait 10 minutes and retry.

## Automation
This project demonstrates a fully automated, end-to-end machine learning pipeline designed to monitor and analyze user sentiment from app reviews. By leveraging **Azure Machine Learning** and **GitHub Actions**, the system moves beyond a static model to a living infrastructure that handles data ingestion, model training, and batch scoring.

### 1. System Architecture
The pipeline is built on a modular design, ensuring that data processing is decoupled from model training. This allows for independent scaling of compute resources for each stage.



*   **Data Ingestion:** Automatically pulls raw review data into Azure Blob Storage.
*   **Preprocessing:** Cleans text data and performs feature engineering using a custom script environment.
*   **Training & Validation:** Trains the current best-performing model (based on $F_1$ score and accuracy metrics) on a dedicated GPU cluster.
*   **Scoring:** Generates sentiment predictions on new, unseen datasets to provide actionable business insights.

### 2. CI/CD Integration
The core of this "Working Pipeline" is the automation layer. Using GitHub Actions, the pipeline is triggered by specific events in the repository, ensuring the model remains updated as the codebase or data evolves.

*   **Automated Triggers:** Commits to the main branch or manual "workflow_dispatch" events initiate the Azure ML Job.
*   **Environment Management:** Conda environments are built dynamically, ensuring consistency between local development and cloud execution.
*   **Artifact Logging:** Model weights, performance plots, and scoring results are versioned and stored within the Azure ML Workspace for full auditability.

### 3. Current Best Model & Performance
The pipeline currently deploys a fine-tuned sentiment classifier optimized for the nuances of mobile app feedback.

| Metric | Score |
| :--- | :--- |
| **Accuracy** | 0.xx |
| **Precision** | 0.xx |
| **Recall** | 0.xx |
| **F1-Score** | 0.xx |

> **Note:** The pipeline includes automated evaluation steps. If a new training run results in a model that outperforms the current "Best," the registration step updates the production model alias.

### 4. How to Invoke the Pipeline
The scoring pipeline can be triggered via the Azure CLI or through the GitHub Actions "Run Workflow" interface.

```bash
# Example: Triggering a scoring job via CLI
az ml job create --file ./src/scoring-pipeline.yml
```

---

### Key Deliverables Included
*   **`src/`**: Python scripts for data cleaning, training, and scoring.
*   **`.github/workflows/`**: YAML definitions for the CI/CD automation.
*   **`environment.yml`**: Dependency definitions for reproducible compute targets.


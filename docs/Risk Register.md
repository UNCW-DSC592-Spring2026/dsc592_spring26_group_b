

# Risk Register

## Risk Rating Legend
- **Likelihood**: Low (L), Medium (M), High (H)  
- **Impact**: Low (L), Medium (M), High (H)  
- **Risk Level**: Based on Likelihood × Impact  


# 1. Technical Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R1 | NLP model fails to achieve required F1-score (0.XX target) | H | H | High | Use iterative experimentation, try multiple models (BERT, TF-IDF + ML), hyperparameter tuning | ML Engineer |
| R2 | Poor text preprocessing leads to low model accuracy | H | H | High | Standardize preprocessing pipeline, validate with sample datasets | Data Engineer |
| R3 | Model overfitting due to biased or limited dataset | M | H | High | Use cross-validation, regularization, and diverse dataset sampling | ML Engineer |
| R4 | Incorrect handling of slang/jargon reduces prediction quality | H | M | High | Build domain lexicon early | NLP Specialist |
| R5 | Model versioning failure causes inconsistency in predictions | M | H | High | Implement strict version tagging and tracking system | DevOps |


# 2. Data Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R6 | Poor data quality (noise, missing values, spam reviews) | H | H | High | Implement data validation and cleaning pipelines | Data Engineer |
| R7 | Imbalanced dataset (more positive than negative reviews) | H | M | High | Use resampling techniques (SMOTE, class weighting) | ML Engineer |
| R8 | Data privacy breach (PII exposure) | M | H | High | Apply PII masking and anonymization protocols | Security Lead |
| R9 | Dataset not scalable for high-velocity input | M | H | High | Use scalable storage and streaming pipelines | DevOps |


# 3. System & Infrastructure Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R10 | System cannot handle batch processing load (xx,xxx/hour) | H | H | High | Conduct load testing, optimize pipelines, use distributed processing | DevOps |
| R11 | CI/CD pipeline failures delay deployment | M | H | High | Implement automated testing and rollback mechanisms | DevOps |
| R12 | High latency in prediction system | M | M | Medium | Optimize model size and inference pipeline | ML Engineer |
| R13 | System downtime during business hours | M | H | High | Implement monitoring, alerts, and redundancy | DevOps |


# 4. Project & Process Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R14 | Poor GitHub workflow usage (no proper issues/PRs) | M | M | Medium | Enforce GitHub workflow (issues → branch → PR → merge) | Team Lead |
| R15 | Lack of coordination between team members | M | H | High | Daily/weekly sync meetings, clear task ownership | Team Lead |
| R16 | Scope creep due to adding unnecessary features | M | M | Medium | Stick to MVP and backlog priorities | Product Owner |
| R17 | Poor documentation affecting maintainability | H | M | High | Maintain docs in `/docs/`, update continuously | All |


# 5. External & Business Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R18 | Changing business requirements mid-project | M | M | Medium | Keep modular architecture and flexible design | Team Lead |
| R19 | Misinterpretation of stakeholder needs | M | H | High | Regular stakeholder feedback and validation | Product Owner |
| R20 | Regulatory or compliance issues (data privacy laws) | L | H | Medium | Follow GDPR-like privacy practices | Security Lead |


# 6. Model & Evaluation Risks

| ID  | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Owner |
|-----|----------------|------------|--------|------------|--------------------|-------|
| R21 | Incorrect evaluation metrics used (regression vs classification mismatch) | M | H | High | Align metrics with problem formulation (F1, accuracy, etc.) | ML Engineer |
| R22 | Model bias leading to unfair predictions | M | H | High | Bias detection, fairness evaluation, dataset balancing | ML Engineer |
| R23 | Lack of explainability in predictions | M | M | Medium | Use SHAP/LIME for interpretability | ML Engineer |


# Summary

This risk register identifies key technical, data, infrastructure, process, and business risks associated with the NLP-based review rating system. Each risk is paired with mitigation strategies and ownership to ensure accountability and proactive management throughout the software lifecycle.

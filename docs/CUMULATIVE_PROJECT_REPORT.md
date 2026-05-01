# Cumulative Project Report

## Phase 1



### Vision

What it does: Automatically and accurately converts text reviews into star ratings.

Who is using it: Technical staff for operations and executives for financial oversight.

Why it matters: It handles high data volumes quickly to prevent costly delays.

### Stakeholders

Technicians: To manage data and keep the system running.

Executives: To track profits and overall app performance.

Investors: To see data-backed proof of company growth.

### Requirements

_Functional Requirements_

Core Tasks: Support bulk review uploads and predict 1–5 star ratings using NLP.

Analysis: Provide model performance scores and identify key sentiment drivers.

System Logic: Automate text processing and track predictions via model versioning.

_Non-Functional Requirements_

Performance: Ensure high-speed batch processing, high uptime, and low storage costs.

Standards: Maintain strict version control, technical documentation, and automated testing.

Data Quality: Scale via CI/CD pipelines to handle high-velocity text with high accuracy.

_External Requirements_

Security: Protect user identities and maintain strict data privacy.

Flexibility: Ensure the system runs on local laptops, internal servers, or the cloud.



## Phase 2

### Webpage Template

To address the limitations of the inherited prototype, we are utilizing **MyST Markdown** to bridge the gap between technical data science and rigorous software engineering. MyST transforms our documentation from a collection of flat files into a structured, professional-grade site that captures every stage of the engineering cycle. By using advanced features like callouts for requirements and grids for model comparisons, we ensure that our design choices are transparent and well-documented. This approach replaces the "loose documentation" of the original system with a clear, auditable record of our architectural and algorithmic decisions.

MyST streamlines the communication of our system's evolution to project stakeholders. As we refine the baseline Azure ML pipeline, the framework allows us to integrate technical schemas and evaluation metrics into a cohesive narrative. By treating our documentation with the same discipline as our code, we demonstrate a mature engineering approach to a data-intensive project. This setup ensures that the rationale behind our system—from stakeholder needs to final performance reflections—is easily navigable and reproducible for the entire team.

### Risk Registers
A structured risk analysis was conducted to identify potential challenges that could impact the successful development and deployment of the NLP-based app review rating system. Based on the project requirements, this phase emphasizes on proactive identification of uncertainties and mitigation strategies. The system is made for hign data intensive and high performance environment , where large volumes of unstructured text reviews must be processed efficiently while maintaining high prediction accuracy.
risks were categorized into six major areas: technical, data-related, system and infrastructure, project and process, external/business, and model evaluation risks.

### 1. Technical Risk
The most critical risks identified are associated with the NLP model itself. Achieving the required performance threshold (F1-score ≥ 0.XX) is uncertain due to the variability and ambiguity of natural language. Additionally, improper text preprocessing can significantly downgrade model performance. Another major concern is model overfitting, where the system performs well on training data but fails to generalize to real-world inputs. To address these risks, iterative experimentation, robust preprocessing pipelines, and domain-specific lexicon development are planned.
### 2. Data Risk
Data quality is a basic dependency of the system. Noisy, incomplete, biased datasets can directly impact prediction accuracy. In particular, class imbalance (e.g., a higher proportion of positive reviews) may lead to biased predictions. Privacy is another critical concern, as the system processes user-generated content. Any exposure of personally identifiable information would represent a severe compliance and ethical failure. To mitigate these risks, data validation pipelines, anonymization techniques, and resampling strategies will be implemented.
### 3. System and Infrastructure Risk
The system is expected to handle high-throughput batch processing (xx,xxx reviews per hour), making scalability and performance key concerns. Failures in CI/CD pipelines or system downtime during business hours could significantly impact stakeholders relying on real-time insights. To mitigate these risks, load testing, monitoring systems, and automated deployment pipelines with rollback mechanisms will be incorporated into the architecture.
### 4. Project and Process Risks
Since the project is developed in a collaborative environment using GitHub, process-related risks such as poor task tracking, lack of coordination, and inadequate documentation were identified. Without proper use of GitHub Issues, branches, and pull requests, the development process may become disorganized. To address this, a structured workflow (Issue → Branch → Pull Request → Merge) will be enforced, along with regular team sync meetings.
### 5. External Business Risk
Changes in stakeholder requirements or misinterpretation of business goals may lead to misaligned system functionality. Additionally, regulatory considerations related to data privacy must be addressed. These risks will be mitigated through continuous stakeholder feedback, modular system design, and adherence to data protection standards.
### 6. Model Evaluation Risks
One of the most important and critical risks involves the selection of appropriate evaluation metrics. The baseline system uses regression techniques; however, the problem may be better framed as a classification task. Using inappropriate metrics could lead to misleading conclusions about model performance. Therefore, evaluation strategies will focus on classification metrics such as F1-score, precision, and recall, ensuring alignment with the problem formulation.


Each identified risk is paired with a mitigation strategy and an assigned owner responsible for monitoring and resolution. The risk register will be treated as a living document and updated throughout subsequent phases of the project. Regular reviews will be conducted to reassess risk levels and ensure that mitigation strategies remain effective as the system evolves.

### Architecture Diagrams
In order to succeed in our project's end goal, we heavily prioritized having an organized plan with all the requirements we need for our model. With this, we included both a context diagram with the overall workflow for the project and how everything is connected with external factors, and we included a component diagram, which discusses the internal processes of our system that he hope to include in our final model. Doing so will allow us to incorporate all processes such as ingestion, preprocessing, machine learning, and reporting to maintain the model and ensure it is providing accurate results. 

The context diagram describes the app review system as a central unit that interacts with various external entities during its processes. The primary data source includes the Raw Data and the reviewers who submit reviews, and this data is then used to deliver actionable insights to developers, executives, and other operational teams that support and monitor the system to ensure accurate predictions. The app developers are able to interact with the data through a dashboard where they can visually see the app ratings made by the system as well as the sentiment insights and the system flags. With this, developers can proactively tackle issues and dissatisfaction with apps to improve the overall experience. The DevOps and machine learning engineers are then able to utilize CI/CD pipelnines to improve and monitor the system performance, deployments, and reliability. The data flows between these components are explicitly defined to include data ingestion, prediction outputs, and monotirong logs to ensure every piece of the puzzle is shown. 

The component diagram is more technical with the internal processes of the app review system. It is composed of several layers that work together to create a machine learning pipeline. The data ingestion layer is primarily responsbile for collecting all of the app reviews from the raw data and uploading it to the pipeline. Next, the preprocessing layer is used to normalize text, clean text, lowercasing, slang replacement, and implemeneting privacy measures to exclude private information. After preprocessing, feature extraction is then applied to transform text reviews into numerical vectors that the model can learn from. This data is then ingested into the modeling layer where a prediction model will rate the review from 1-5 stars and will automatically flag any issues with the reviews and store them into our data storage pipeline for future model training. The serving layer then takes this information and scales it based on the usage demands. Finally, the reports layer ingests this information into a dashboard so that developers can utilize insights, metrics, and app performance. In addition, the machine learning engineers can utilize CI/CD pipelines to ensure that the dashboard is accurate and the model is reliable. 

With this, we were able to create a diagram for our system that is modular, scalable, and transparent. The modular aspect of this system comes from the various layers within the system's architectur, allowing for individual components to be worked on without affecting the system as a whole. The scalability is addressed through the use of batdch processing the raw data to ensure that the system can handle the large volume of reviews that will be used as input. Lastly, the system will be transparent by including the keyword extraction and model performance reporting so that developers, engineers, and executives can gain insights in their various fields for further action.



## Phase 3

### Exploratory Data Analysis
Before recommending any pipeline changes, I performed a full EDA on AppReviewData.csv (111,143 reviews across 492 apps) to understand what the data actually looks like. 
The analysis surfaced a severe class imbalance with 60.9% of reviews rated 1.0 and only 71 reviews rated 0.0, a scraping artifact ("Full Review" appended to most reviews), label noise (non-English words like Bekar — Hindi/Urdu for "useless" — appearing in the 1.0 class), multilingual content, and an inverted-U pattern in review length across ratings. These findings are committed in notebooks/Data_Exploration.ipynb and now anchor the rest of my Phase 3 work.

### Baseline Text Preprocessing
The doc covers each enabled option like lowercasing, stopword removal, lemmatization, special-character and number removal, URL and email stripping, contraction expansion, duplicate-character collapsing, and notes where each setting helps the dataset. Examples include converting the short words into don't into do not.

### Feature Extraction 
Suggested couple of features 1. N - Grams, and 2. Domain Lexicon

### Privacy / PII Protocol 
quantifies how many reviews actually contain emails, phone numbers, URLs, and social handles. We will use the actual results from this scan to determine how to hide sensitive data and how to catch potential threats, rather than just guessing or making assumptions.

### Domain Lexicon
The EDA already surfaced concrete slang and informal-spelling candidates that will seed the lexicon (e.g. gud, worky, ise, bekar, plus the "Full Review" artifact). The build will produce data/domain_lexicon.json, a builder script, and a methodology doc in docs/.


### CI/CD & Automation of Working Pipeline 

We have successfully implemented a fully automated deployment pipeline using GitHub Actions. This workflow triggers automatically upon file changes in specific directories, allowing for seamless testing and deployment of new model variants.

### Cloud Infrastructure & Orchestration

To support the pipeline, the following are configured within Azure ML Studio.
The Workspace Blob Storage, configured for efficient input dataset management, containing a store for `amazon review dataset`, Compute Clusters, scaled and managed Azure ML compute for efficient job execution. And RBAC & Security, Administered Contributor roles to ensure secure, automated job dispatching, for GitHub Actions role assignments.

### Software Architecture 

The repository has grown to support modular python components for each step of the Azure ML pipeline. The respective documentation has been updated and an updated component diagram is included.



## Phase 4

**Model Optimization**: Switched from Linear Regression to Ridge Regression to improve generalization and handle multicollinearity via $L_2$ regularization.

**Performance**: The Ridge model reduced variance, resulting in more stable predictions across the test set.

**Documentation**: Fully updated the project webpage with comprehensive documentation of the final model architecture and hyperparameters.

**Monitoring**: Integrated Slack notifications into the deployment pipeline for real-time reporting.Automated 

**Alerts**: The system now broadcasts pipeline success status and model accuracy metrics (MSE/$R^2$) directly to the team.

**Outcome**: Established a transparent, self-reporting production environment for the final model.



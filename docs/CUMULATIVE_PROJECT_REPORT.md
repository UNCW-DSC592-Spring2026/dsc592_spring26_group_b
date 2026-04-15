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




### Risk Registers



### Architecture Diagrams
In order to succeed in our project's end goal, we heavily prioritized having an organized plan with all the requirements we need for our model. With this, we included both a context diagram with the overall workflow for the project and how everything is connected with external factors, and we included a component diagram, which discusses the internal processes of our system that he hope to include in our final model. Doing so will allow us to incorporate all processes such as ingestion, preprocessing, machine learning, and reporting to maintain the model and ensure it is providing accurate results. 

The context diagram describes the app review system as a central unit that interacts with various external entities during its processes. The primary data source includes the Raw Data and the reviewers who submit reviews, and this data is then used to deliver actionable insights to developers, executives, and other operational teams that support and monitor the system to ensure accurate predictions. The app developers are able to interact with the data through a dashboard where they can visually see the app ratings made by the system as well as the sentiment insights and the system flags. With this, developers can proactively tackle issues and dissatisfaction with apps to improve the overall experience. The DevOps and machine learning engineers are then able to utilize CI/CD pipelnines to improve and monitor the system performance, deployments, and reliability. The data flows between these components are explicitly defined to include data ingestion, prediction outputs, and monotirong logs to ensure every piece of the puzzle is shown. 

The component diagram is more technical with the internal processes of the app review system. It is composed of several layers that work together to create a machine learning pipeline. The data ingestion layer is primarily responsbile for collecting all of the app reviews from the raw data and uploading it to the pipeline. Next, the preprocessing layer is used to normalize text, clean text, lowercasing, slang replacement, and implemeneting privacy measures to exclude private information. After preprocessing, feature extraction is then applied to transform text reviews into numerical vectors that the model can learn from. This data is then ingested into the modeling layer where a prediction model will rate the review from 1-5 stars and will automatically flag any issues with the reviews and store them into our data storage pipeline for future model training. The serving layer then takes this information and scales it based on the usage demands. Finally, the reports layer ingests this information into a dashboard so that developers can utilize insights, metrics, and app performance. In addition, the machine learning engineers can utilize CI/CD pipelines to ensure that the dashboard is accurate and the model is reliable. 

With this, we were able to create a diagram for our system that is modular, scalable, and transparent. The modular aspect of this system comes from the various layers within the system's architectur, allowing for individual components to be worked on without affecting the system as a whole. The scalability is addressed through the use of batdch processing the raw data to ensure that the system can handle the large volume of reviews that will be used as input. Lastly, the system will be transparent by including the keyword extraction and model performance reporting so that developers, engineers, and executives can gain insights in their various fields for further action.
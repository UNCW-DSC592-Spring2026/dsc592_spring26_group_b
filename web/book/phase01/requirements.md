# Requirements



## Functional Requirements


### User Requirements

- system shall allow users to submit text reviews
  - and bulk upload for batch-processing
  
- system shall analyze text reviws to output predicted rating

- system shall provide a score indicating model peformance

- system shall list keywords and phrases that provide model best fit

### System Requirements

- text pre-processing
  - system shall normalize review text

- feature extraction
  - system shall transform unstructured text into representation 

- model versioning
  - system shall automatically tag every prediction to track which model version used



### Domain Requirements

1. Mobile App Store
   - app store uses a 1 to 5 star rating system
   - system has to understand the specific slang and jargon of your users



## Non-functional Requirements

### Product Requirements

- Speed/Performance
  - system must batch process xx,xxx reviews per hour
  
- Relability
  - system must maintain XX.X% availability during business hours
  
- Robustness
  - system and automated pipelines must flexibly handle irregular data
  
- Size
  - deployed artifacts must be minimized for optimal storage costs and cloud services
  
### Organizational Requirements

- Maintability
  - all software and model configurations and dataset versioning
  
- Documentation
  - technical documentation detailing training and test data, weights and biases, and evaluation metrics
  
- Developement
  - implementation of automated testing for deploying to production
  
  
### External Requirements

- Portability
  - It must be able to run on the company’s main servers, a technician's laptop, or a cloud provider

- Privacy
  - system must protect the identity of the people writing the reviews

### Big Data

- Velocity × Scalability
  - systems requires automated CI/CD pipeline
    - capable of handling streams of thousands of unstructured data
      - of text reviews per hour to replace manual use case bottleneck
      
- Variety × Accuracy
  - system requires NLP module to predict app ratings 
    - with a minimum F1-score of 0.XX

- Veracity × Maintainability
  - system requires automation of data validation and logs
    - enabling engineers to maintain model performance
      - over software lifecycles

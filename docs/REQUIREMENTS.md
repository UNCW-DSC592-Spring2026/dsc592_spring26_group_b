# Requirements



## Functional Requirements




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


- Privacy


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

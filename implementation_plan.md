# Implementation Plan

Imagine you will be working alongside 2 Senior software engineers to implement the MVP for this feature, as much in parallel as possible. Divide up the work and make a general implementation plan.

- What pieces of work will be included in each workstream, what can be parallelized, where dependencies will exist
- What work you would select to implement yourself and why


## Work Streams

For three engineers it makes sense to divide the work into three concerns:

1. Operational: Automation, Testing and Delivery
2. Backend: Data and API
3. Frontend: Presentational Layer


### Operational

This application depends critically on third-party cloud provider interfaces, so it's important to have all the cloud provider features lined up and working according to what the application needs. So this workstream focuses on ensuring that the necessary tools are in place to create resources in the cloud provider(s), secure them, correct drift and provide a framework for iterating on the cloud platform itself. Tools like Pulumi, Terraform, and Ansible come to mind.

In addition, this workstream includes building a framework to ensure the application is always in a deliverable state. Every workstream includes writing unit tests, but this workstream builds CI/CD and integration testing tools so that we can be sure that updates to the product meet the contract.


### Backend

The Data and API workstream determines and implements the API and metadata-model.


### Frontend

This workstream involves building user facing interfaces (as opposed to APIs). These could be CLIs or GUIs depending on demand, but I'll assume Web UI for now...


## Dependencies

### Permissions Model: Database or Cloud IAM

If the application is intended to be cross-cloud, then it makes sense to keep as much metadata in the application itself as possible. That is a risk, though, because a small error in the application coding could expose files to the wrong tenant. That is less likely to happen if permissions and user management are handled via the cloud provider's IAM, but that is more complex.

Thus, agreeing upon and implementing the permissions model is a shared responsibility of the Backend and Operational workstreams.


### API Contract

The Frontend is limited until they have a firm API contract; so they will need that from the Backend workstream as early as possible.


### Gantt

```mermaid
gantt
    title Multi-tenant S3 Object Store Implementation
    dateFormat  YYYY-MM-DD
    section Project Setup
    Project Kickoff                      :milestone, m1, 2025-03-20, 0d

    section Operations
    Infrastructure Setup                 :op1, 2025-03-20, 14d
    IAM & Permissions Design             :op2, after op1, 10d
    CI/CD Pipeline Setup                 :op3, after op1, 7d
    Integration Testing Framework        :op4, after op3, 14d
    Deployment Automation                :op5, after op4, 10d
    Security Review                      :op6, after op5, 7d

    section Backend
    API Contract Definition              :be1, 2025-03-20, 7d
    Permissions Model Design             :be2, 2025-03-20, 10d
    Database Schema Design               :be3, after be2, 5d
    API Implementation                   :be4, after be1 be3, 21d
    API Documentation                    :be5, after be4, 7d
    Performance Optimization             :be6, after be5, 14d

    section Frontend
    UI/UX Design                         :fe1, 2025-03-20, 14d
    API Contract Review                  :fe2, after be1, 3d
    Core Components Development          :fe3, after fe1 fe2, 14d
    Mock API Integration                 :fe4, after fe3, 7d
    Full API Integration                 :fe5, after be4 fe4, 14d
    UI Refinement                        :fe6, after fe5, 10d

    section Dependencies
    Permissions Model Decision           :milestone, m2, after op2 be2, 0d
    API Contract Finalized               :milestone, m3, after be1 fe2, 0d
    Mock API Available                   :milestone, m4, after be1, 0d
    Full API Available                   :milestone, m5, after be4, 0d
    End-to-End Testing                   :test1, after op4 be5 fe5, 14d
    Production Deployment                :milestone, m6, after op6 be6 fe6 test1, 0d
```

### Flowchart


```mermaid
flowchart TD
    subgraph "Multi-tenant Object Store Project"
        direction TB

        subgraph "Operations"
            direction TB
            OP1[Infrastructure Setup]
            OP2[IAM & Permissions Design]
            OP3[CI/CD Pipeline]
            OP4[Integration Testing]
            OP5[Deployment Automation]
            OP6[Security Review]

            OP1 --> OP2
            OP1 --> OP3
            OP3 --> OP4
            OP4 --> OP5
            OP5 --> OP6
        end

        subgraph "Backend"
            direction TB
            BE1[API Contract Definition]
            BE2[Permissions Model Design]
            BE3[Database Schema Design]
            BE4[API Implementation]
            BE5[API Documentation]
            BE6[Performance Optimization]

            BE1 --> BE4
            BE2 --> BE3
            BE3 --> BE4
            BE4 --> BE5
            BE5 --> BE6
        end

        subgraph "Frontend"
            direction TB
            FE1[UI/UX Design]
            FE2[API Contract Review]
            FE3[Core Components]
            FE4[Mock API Integration]
            FE5[Full API Integration]
            FE6[UI Refinement]

            FE1 --> FE3
            FE2 --> FE3
            FE3 --> FE4
            FE4 --> FE5
            FE5 --> FE6
        end

        %% Cross-workstream dependencies
        BE1 --> FE2
        OP2 <---> BE2
        BE4 --> FE5

        %% Critical path dependencies
        OP6 --> DEPLOY[(Production Deployment)]
        BE6 --> DEPLOY
        FE6 --> DEPLOY
    end

    %% Legend
    classDef operations fill:#e6f7ff,stroke:#1890ff
    classDef backend fill:#f6ffed,stroke:#52c41a
    classDef frontend fill:#fff7e6,stroke:#fa8c16

    class OP1,OP2,OP3,OP4,OP5,OP6 operations
    class BE1,BE2,BE3,BE4,BE5,BE6 backend
    class FE1,FE2,FE3,FE4,FE5,FE6 frontend
```


# Assignment

I'd work on the Data and API workstream. It's the central part of the project and can offer flexible support to both the operational and frontend workstreams if necessary.

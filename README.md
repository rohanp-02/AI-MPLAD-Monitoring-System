# 🤖 AI-Powered MPLAD Monitoring System

### Intelligent, Explainable & Role-Based Monitoring of MPLAD Projects

<p align="center">

**AI-Powered Monitoring System for Detecting Project Risk Indicators, Delays, Financial-Physical Mismatches and Unusual Project Patterns**

</p>

---

## 🏛️ Smart India Hackathon

### Problem Statement ID: SIH26102

**Domain:** Software / Artificial Intelligence & Data Analytics

**Project:** AI-Powered MPLAD Monitoring System

---

# 📌 Problem Statement

Monitoring infrastructure projects under the **Members of Parliament Local Area Development Scheme (MPLADS)** involves tracking multiple parameters such as:

* Project expenditure
* Physical progress
* Financial progress
* Project duration
* Project modifications
* Inspection records
* Project category
* District-level implementation

When these parameters are monitored manually, identifying projects that require attention can become difficult, especially when the number of projects increases.

The proposed system provides an **AI-assisted monitoring and risk-identification layer** that analyzes project data and highlights projects containing unusual or potentially concerning indicators.

> **Important:** The system identifies risk indicators and unusual patterns. It does **not** automatically declare a project as fraudulent.

---

# 💡 Proposed Solution

The **AI-Powered MPLAD Monitoring System** is a web-based platform that combines:

* Rule-based risk analysis
* Machine Learning anomaly detection
* Peer benchmarking
* Early-warning indicators
* Explainable risk scoring
* Human verification
* Role-based access control
* Review queue
* Audit trail
* District-level monitoring

The system analyzes project information and produces an **explainable risk assessment** so that authorized officers can prioritize projects requiring further review.

### Core Principle

```text
Project Data
     ↓
Data Processing
     ↓
Rule-Based Risk Checks
     ↓
Machine Learning Anomaly Detection
     ↓
Peer Benchmarking
     ↓
Early Warning Analysis
     ↓
Explainable Risk Score
     ↓
Human Verification
     ↓
Supervisor Review / Action
     ↓
Audit Trail
```

---

# 🎯 Objectives

The main objectives of the system are:

1. Improve monitoring of MPLAD projects.
2. Identify projects containing unusual risk indicators.
3. Detect financial and physical progress mismatches.
4. Identify project delays and unusual expenditure patterns.
5. Compare projects with similar projects using peer benchmarking.
6. Use Machine Learning to identify statistically unusual projects.
7. Provide explainable reasons behind risk indicators.
8. Support human officers instead of replacing human decision-making.
9. Maintain an auditable record of verification actions.
10. Provide role-based access to different monitoring officers.

---

# 🧠 Role of Artificial Intelligence

The AI layer consists of multiple analytical components.

## 1. Rule-Based Risk Analysis

The system checks predefined project indicators such as:

* Project delay
* High expenditure
* Financial progress significantly exceeding physical progress
* Multiple project modifications
* Inspection-related indicators
* Other project-level risk conditions

These indicators contribute to the project's risk assessment.

---

## 2. Machine Learning Anomaly Detection

The system uses **Isolation Forest**, an unsupervised machine-learning algorithm.

The model analyzes project features including:

```text
Sanctioned Amount
Expenditure
Expected Duration
Actual Duration
Physical Progress
Financial Progress
Project Modifications
Inspection Records
```

The model identifies projects that are statistically unusual compared with the other projects in the dataset.

### Why Isolation Forest?

Isolation Forest is suitable for this prototype because:

* It can work without manually labelled fraud data.
* It is designed for anomaly detection.
* It can identify unusual combinations of project characteristics.
* It supports an intelligence layer without requiring a pre-labelled fraud dataset.

---

# ⚠️ AI Does NOT Declare Fraud

A key design principle of this system is:

> **AI identifies risk indicators, not fraud.**

An anomaly detected by the model does not automatically mean that wrongdoing has occurred.

The system instead follows:

```text
AI Detection
     ↓
Risk Indicator
     ↓
Officer Review
     ↓
Human Verification
     ↓
Supervisor Review
     ↓
Appropriate Action
```

This helps keep the system explainable and human-supervised.

---

# 📊 Explainable Risk Scoring

Instead of showing only an AI prediction, the system provides an explainable risk assessment.

Projects are categorized into:

* 🟢 **LOW**
* 🟡 **MEDIUM**
* 🔴 **HIGH**

The system also provides reasons contributing to the risk assessment.

Example:

```text
Risk Score: 85
Risk Level: HIGH

Indicators:
• Project is delayed
• Financial progress is significantly higher than physical progress
• Multiple project modifications detected
```

This allows officers to understand **why a project has been highlighted**.

---

# 📈 Peer Benchmarking

The system compares a project against other projects in the same category.

For example:

```text
Project Category: Roads

Current Project Expenditure:
₹38,00,000

Average Peer Expenditure:
₹48,50,000

Average Peer Physical Progress:
58%

Average Peer Duration:
10 Months
```

The comparison provides additional context before generating risk indicators.

### Purpose

Peer benchmarking helps answer questions such as:

* Is expenditure unusual compared with similar projects?
* Is project progress significantly different from similar projects?
* Is project duration unusual?
* Does the project behave differently from its peers?

---

# 🚨 Early Warning System

The system generates early-warning indicators when project characteristics require additional attention.

The early-warning layer combines project information and AI results to identify projects that may require review.

Example:

```text
Project Delay
        +
Financial / Physical Mismatch
        +
Unusual ML Pattern
        ↓
Early Warning
        ↓
Review Queue
```

---

# 📋 Review Queue

Projects requiring attention are automatically added to the **Review Queue**.

The Review Queue provides:

* Project code
* Project name
* Category
* Risk score
* Risk level
* ML status
* Anomaly score
* Early-warning level
* Review status
* Project review access

This allows authorized officers to focus on projects that require further examination.

---

# 👥 Role-Based Access Control

The system implements role-based access control.

## Verification Officer

Can access:

* Dashboard
* Projects
* Project Details
* Review Queue
* Verify Project
* District Monitoring

Cannot access:

* Audit Trail

---

## Project Officer

Can access:

* Dashboard
* Projects
* Project Details

---

## Supervisor

Can access:

* Dashboard
* Projects
* Project Details
* Review Queue
* Verification
* District Monitoring
* Audit Trail

---

## Admin

The administrator has access to the complete monitoring system.

---

# 🔍 Human Verification Workflow

The system follows a human-in-the-loop approach.

```text
Project Recorded
       ↓
AI Analysis
       ↓
Risk Indicators Generated
       ↓
Project Added to Review Queue
       ↓
Verification Officer Reviews
       ↓
Action / Remark Recorded
       ↓
Supervisor Review
       ↓
Audit Trail
```

This ensures that AI outputs are treated as **decision-support information** rather than automatic conclusions.

---

# 📝 Audit Trail

The system maintains an audit trail of verification-related actions.

The audit information includes:

* Project code
* Action performed
* User role
* Timestamp
* Remarks

This provides traceability for important monitoring actions.

---

# 🗺️ District Monitoring

The system provides a district-level monitoring interface.

The District Monitoring module helps visualize the geographical distribution of monitored projects and provides another way to inspect project activity.

The interface uses:

* Interactive map
* District information
* Project monitoring data
* OpenStreetMap-based map visualization

---

# 📊 Dashboard

The main dashboard provides an overview of the monitored projects.

The dashboard displays information such as:

* Total projects
* High-risk projects
* Medium-risk projects
* Low-risk projects
* Delayed projects
* ML unusual projects
* Average expenditure
* Average physical progress

This provides a quick overview before officers move to individual project analysis.

---

# 🏗️ System Architecture

```text
                    ┌───────────────────────┐
                    │     Project Data      │
                    │   MPLAD Project Data  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Data Processing     │
                    │ Cleaning & Validation  │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Rule-Based  │ │ Isolation   │ │    Peer     │
        │ Risk Checks │ │   Forest    │ │ Benchmarking│
        └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
               │               │               │
               └───────────────┼───────────────┘
                               ▼
                    ┌───────────────────────┐
                    │ Explainable Risk      │
                    │      Assessment       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Review Queue       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Human Verification    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Supervisor Review &   │
                    │     Audit Trail       │
                    └───────────────────────┘
```

---

# 🔄 Complete System Workflow

```text
             ┌─────────────────┐
             │  Project Entry  │
             └────────┬────────┘
                      ↓
             ┌─────────────────┐
             │ Data Validation │
             └────────┬────────┘
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   Rule Checks    ML Analysis   Peer Benchmark
        │             │             │
        └─────────────┼─────────────┘
                      ↓
              Risk Assessment
                      ↓
              Early Warning
                      ↓
                Review Queue
                      ↓
             Officer Verification
                      ↓
              Supervisor Review
                      ↓
                 Audit Trail
```

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript
* Jinja2 Templates
* Leaflet.js
* OpenStreetMap

## Backend

* Python
* Flask

## Database

* SQLite

## Artificial Intelligence / Machine Learning

* Scikit-learn
* Isolation Forest
* Pandas
* NumPy
* StandardScaler

## Deployment

* Gunicorn
* Render

## Development

* Visual Studio Code
* Git
* GitHub

---

# 📁 Project Structure

```text
AI-MPLAD-Monitoring-System/
│
├── app.py
├── database.py
├── ml_model.py
├── risk_engine.py
├── mplad.db
├── requirements.txt
├── Procfile
├── .gitignore
│
├── static/
│   └── ...
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── projects.html
│   ├── project.html
│   ├── review_queue.html
│   ├── districts.html
│   └── audit.html
│
└── README.md
```

---

# 🚀 Live Demo

### 🌐 Live Application

**AI-Powered MPLAD Monitoring System**

https://ai-mplad-monitoring-system.onrender.com

> The application is deployed using Render.

---

# 💻 Run the Project Locally

## 1. Clone the repository

```bash
git clone https://github.com/rohanp-02/AI-MPLAD-Monitoring-System.git
```

## 2. Open the project

```bash
cd AI-MPLAD-Monitoring-System
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Flask application

```bash
python app.py
```

## 5. Open in browser

```text
http://127.0.0.1:5000
```

---

# 📦 Requirements

The project uses the following Python packages:

```text
Flask
pandas
numpy
scikit-learn
nltk
gunicorn
```

They are listed in:

```text
requirements.txt
```

---

# 🔐 Security & Access Control

The prototype includes role-based access control to ensure that different users have access to the functionality relevant to their responsibilities.

The system separates:

```text
Monitoring
     ↓
Verification
     ↓
Supervision
     ↓
Audit
```

This provides a structured workflow rather than giving every user unrestricted access.

---

# 🎯 Key Benefits

### For Monitoring Officers

* Faster identification of projects requiring attention
* Centralized project information
* Explainable risk indicators
* Review queue for prioritized monitoring

### For Supervisors

* Review of verification actions
* Escalation visibility
* Audit trail
* District-level monitoring

### For Government Monitoring

* Data-driven project monitoring
* Early identification of unusual patterns
* Comparison with similar projects
* Human-supervised AI analysis
* Better traceability of monitoring actions

---

# 🌱 SDG Alignment

The project can contribute to the broader objectives of:

### SDG 9 — Industry, Innovation and Infrastructure

Supports data-driven monitoring of infrastructure projects.

### SDG 11 — Sustainable Cities and Communities

Supports monitoring of development projects that contribute to local infrastructure.

### SDG 16 — Peace, Justice and Strong Institutions

Supports transparency, accountability, traceability and structured monitoring through role-based access and audit trails.

---

# 🔮 Future Enhancements

The current prototype can be extended with:

* Integration with live government MPLADS / e-SAKSHI data sources
* Larger real-world datasets
* More advanced anomaly-detection models
* NLP-based project description similarity
* Automated document verification
* Geospatial project analysis
* Historical project trend analysis
* Real-time notifications
* Mobile application
* Advanced district and constituency analytics
* Model performance monitoring
* Explainable AI dashboards
* Automated report generation

---

# ⚠️ Current Prototype Limitation

This project is a prototype demonstrating an AI-assisted monitoring approach.

The current system uses project data available within the prototype database. Machine-learning results therefore demonstrate the methodology rather than representing an official government fraud-detection system.

**AI-generated anomalies should always be verified by authorized personnel.**

---

# 📸 Screenshots

Add screenshots of the application here.

### Dashboard

```text
![Dashboard](screenshots/dashboard.png)
```

### Projects

```text
![Projects](screenshots/projects.png)
```

### Project Analysis

```text
![Project Analysis](screenshots/project-analysis.png)
```

### Review Queue

```text
![Review Queue](screenshots/review-queue.png)
```

### District Monitoring

```text
![District Monitoring](screenshots/districts.png)
```

### Audit Trail

```text
![Audit Trail](screenshots/audit.png)
```

> Create a `screenshots` folder in the repository and place your actual screenshots there.

---

# 📚 Project Modules

| Module               | Purpose                             |
| -------------------- | ----------------------------------- |
| 🔐 Login             | User authentication and role access |
| 📊 Dashboard         | Overall project monitoring          |
| 📁 Projects          | View monitored projects             |
| 🔍 Project Analysis  | Detailed project risk analysis      |
| 🤖 AI Analysis       | Detect unusual project patterns     |
| 📈 Peer Benchmarking | Compare with similar projects       |
| ⚠️ Early Warning     | Highlight potential risk indicators |
| 📋 Review Queue      | Projects requiring review           |
| 👤 Verification      | Human verification of AI indicators |
| 🗺️ Districts        | District-level monitoring           |
| 📝 Audit Trail       | Track verification actions          |

---

# 🧪 AI Monitoring Example

A project may contain:

```text
Expected Duration: 6 months
Actual Duration: 11 months

Physical Progress: 62%
Financial Progress: 95%

Project Modifications: 4
Inspections: 1
```

The system can identify these characteristics as risk indicators and generate an explainable assessment.

The project is then placed into the monitoring workflow for human review.

---

# 🧩 Design Philosophy

The system is designed around five principles:

### 1. Explainability

Officers should understand why a project was highlighted.

### 2. Human-in-the-Loop

AI assists officers instead of replacing them.

### 3. Risk-Based Monitoring

Projects containing stronger indicators can receive additional attention.

### 4. Role-Based Responsibility

Different users receive access according to their monitoring responsibilities.

### 5. Auditability

Important verification actions are recorded for traceability.

---

# 👨‍💻 Project

## AI-Powered MPLAD Monitoring System

Developed as a Smart India Hackathon project for intelligent monitoring of MPLAD projects using Artificial Intelligence, Machine Learning and data analytics.

---

# 🔗 Important Links

⭐ **GitHub Repository**

https://github.com/rohanp-02/AI-MPLAD-Monitoring-System

🌐 **Live Application**

https://ai-mplad-monitoring-system.onrender.com

---

# 🤝 Contribution

Contributions, suggestions and improvements are welcome.

If you find an issue:

1. Open an issue in the repository.
2. Describe the problem clearly.
3. Provide steps to reproduce it if applicable.
4. Suggest improvements where possible.

Pull requests are also welcome.

---

# ⭐ Support

If you find this project useful:

* ⭐ Star the repository
* 🍴 Fork the repository
* 🐛 Report issues
* 💡 Suggest improvements
* 🤝 Contribute to the project

---

# 📄 License

This project is intended for educational, research and demonstration purposes.

---

# 🙏 Thank You

Thank you for visiting the **AI-Powered MPLAD Monitoring System** repository.

> **AI identifies risk indicators. Humans make the final verification and monitoring decisions.**

---

## 🏷️ Suggested GitHub Topics

```text
artificial-intelligence
machine-learning
mplads
mplad
smart-india-hackathon
sih
sih2025
flask
python
data-science
anomaly-detection
isolation-forest
government
project-monitoring
risk-analysis
explainable-ai
peer-benchmarking
sqlite
render
```

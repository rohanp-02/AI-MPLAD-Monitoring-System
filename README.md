# AI-Powered MPLAD Monitoring System

### Intelligent, Explainable & Human-Assisted Monitoring of MPLAD Projects

An AI-powered monitoring and risk-analysis platform designed to help government officials monitor MPLAD projects, identify unusual project patterns, prioritize projects for verification, and maintain a transparent audit trail.

> **Smart India Hackathon — Problem Statement ID: SIH26102**

---

## 🎥 Project Demo

▶️ **YouTube Video:**
https://youtu.be/ID42lNr8OoA

The video demonstrates the working prototype, AI-assisted project analysis, risk identification, review workflow, and monitoring features.

---

## 📌 Problem Statement

Monitoring MPLAD projects across multiple districts involves handling large amounts of project, financial, physical-progress, inspection, and administrative data.

Manual monitoring can make it difficult to:

* Identify projects requiring attention
* Detect unusual expenditure or progress patterns
* Compare projects with similar projects
* Track delayed projects
* Prioritize verification activities
* Maintain a complete record of verification decisions

The proposed system provides an AI-assisted monitoring layer that helps officials focus their attention on projects showing potentially unusual or higher-risk indicators.

---

# 💡 Proposed Solution

The **AI-Powered MPLAD Monitoring System** combines rule-based analysis, machine learning, peer benchmarking, early-warning indicators, and human verification.

The system:

1. Collects project information
2. Processes project-level data
3. Performs rule-based risk analysis
4. Uses machine learning for anomaly detection
5. Compares projects with similar projects
6. Generates an explainable risk score
7. Provides early-warning indicators
8. Places relevant projects into a review queue
9. Allows authorized officials to verify projects
10. Records verification actions in an audit trail

### Important Principle

> **AI identifies risk indicators, not fraud.**

The final decision remains with authorized government officials.

---

# 🤖 Role of AI

The AI layer supports officials by identifying unusual patterns that may require additional verification.

### AI Components

#### 1. Rule-Based Risk Analysis

The system evaluates indicators such as:

* Project delay
* High expenditure
* Financial progress vs physical progress mismatch
* Excessive modifications
* Inspection-related indicators
* Project progress

These indicators contribute to the project's explainable risk score.

---

#### 2. Isolation Forest Anomaly Detection

The system uses **Isolation Forest**, an unsupervised machine-learning algorithm, to identify statistically unusual projects.

The model considers features including:

* Sanctioned amount
* Expenditure
* Expected duration
* Actual duration
* Physical progress
* Financial progress
* Project modifications
* Inspection records

The output identifies projects as:

* **NORMAL**
* **ANOMALY**

An anomaly is an unusual statistical pattern and **does not mean fraud**.

---

#### 3. Explainable Risk Score

Instead of only showing an AI prediction, the system provides understandable reasons behind the risk assessment.

Example indicators:

> Financial progress is significantly higher than physical progress.

> Project duration is unusually high.

> Project modifications are unusually high.

This helps officials understand **why a project requires attention**.

---

#### 4. Peer Benchmarking

Projects are compared with other projects in the same category.

The system calculates comparison indicators such as:

* Average peer expenditure
* Average peer physical progress
* Average peer duration

This provides additional context before verification.

---

#### 5. Early Warning System

The system identifies warning conditions before they become major monitoring concerns.

Examples include:

* Project delays
* Financial-progress mismatch
* High expenditure
* Multiple modifications
* Unusual project characteristics

---

# 📊 Explainable Risk Framework

The system combines multiple monitoring indicators into an overall risk assessment.

### Example

A project may receive:

**Risk Score: 85/100 — HIGH**

Possible reasons:

* Significant project delay
* High financial progress compared with physical progress
* Multiple project modifications

The system then sends the project for human review.

---

# 🔄 Human Verification Workflow

The system follows a human-in-the-loop approach.

```text
Project Data
     ↓
Data Processing
     ↓
Rule-Based Analysis
     ↓
ML Anomaly Detection
     ↓
Peer Benchmarking
     ↓
Explainable Risk Score
     ↓
Early Warning Indicators
     ↓
Review Queue
     ↓
Human Verification
     ↓
Supervisor Review / Escalation
     ↓
Audit Trail
```

AI assists the monitoring process while authorized officials remain responsible for verification and administrative decisions.

---

# 👥 Role-Based Access Control

Different users receive access according to their responsibilities.

### Verification Officer

Can:

* View dashboard
* View projects
* View review queue
* Verify projects
* View district analytics

### Project Officer

Can:

* View dashboard
* View projects
* View project details

### Supervisor

Can:

* View dashboard
* View projects
* Review flagged projects
* Verify projects
* View district analytics
* View audit trail

### Admin

Has access to all available monitoring functions.

---

# 📝 Audit Trail

Every important verification action can be recorded.

The audit trail can contain:

* Project code
* Action performed
* User role
* Timestamp
* Remarks

This provides traceability and supports accountability.

---

# 🗺️ District Analytics

The system provides district-level monitoring.

District analytics include:

* Number of projects
* High-risk projects
* Medium-risk projects
* Low-risk projects
* ML anomaly count
* Average project risk

A geographic map provides a visual overview of monitored districts.

---

# 📋 Review Queue

The Review Queue prioritizes projects requiring additional attention.

It combines:

* Rule-based risk
* ML anomaly status
* Early-warning indicators
* Review status
* Project information

Officials can open a project and perform the required verification.

---

# 📈 Dashboard

The dashboard provides an overall monitoring view.

It displays information such as:

* Total projects
* High-risk projects
* Medium-risk projects
* Low-risk projects
* Delayed projects
* ML anomalies
* Average expenditure
* Physical progress

This provides a quick overview of the current monitoring situation.

---

# 🏗️ System Architecture

```text
                    MPLAD / Project Data
                            │
                            ▼
                    Data Preprocessing
                            │
                            ▼
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
       Rule-Based Analysis        ML Anomaly Detection
              │                           │
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    Peer Benchmarking
                            │
                            ▼
                 Explainable Risk Engine
                            │
                            ▼
                  Early Warning System
                            │
                            ▼
                     Review Queue
                            │
                            ▼
                   Human Verification
                            │
                            ▼
                 Supervisor Escalation
                            │
                            ▼
                      Audit Trail
```

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript
* Leaflet.js
* OpenStreetMap

## Backend

* Python
* Flask

## Database

* SQLite

## Machine Learning

* Scikit-learn
* Isolation Forest
* StandardScaler
* NumPy
* Pandas

---

# 📂 Project Structure

```text
AI-MPLAD-Monitoring-System/
│
├── app.py
├── database.py
├── ml_model.py
├── risk_engine.py
├── mplad.db
├── requirements.txt
├── README.md
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
├── static/
│   └── ...
│
└── .gitignore
```

---

# 🚀 Running the Project Locally

## 1. Clone the repository

```bash
git clone https://github.com/rohanp-02/AI-MPLAD-Monitoring-System.git
```

## 2. Enter the project directory

```bash
cd AI-MPLAD-Monitoring-System
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run Flask

```bash
python app.py
```

## 5. Open the application

```text
http://127.0.0.1:5000
```

---

# ☁️ Deployment

The prototype is deployed using **Render**.

### Deployment Configuration

**Build Command**

```text
pip install -r requirements.txt
```

**Start Command**

```text
gunicorn app:app
```

### Live Application

https://ai-mplad-monitoring-system.onrender.com

---

# 🔐 Security & Access Control

The prototype includes role-based access control to restrict functionality according to user responsibilities.

The system is designed around:

* Authorized access
* Role-specific functionality
* Human verification
* Traceable actions
* Audit logging

---

# 🎯 Benefits

The system can help government monitoring teams by:

* Prioritizing projects for verification
* Identifying unusual project patterns
* Reducing dependence on purely manual screening
* Providing explainable risk indicators
* Comparing similar projects
* Highlighting delayed projects
* Improving monitoring transparency
* Maintaining verification records
* Supporting district-level monitoring

---

# 🌱 SDG Alignment

The project supports several Sustainable Development Goals.

### SDG 9 — Industry, Innovation and Infrastructure

Supports technology-driven monitoring of public infrastructure projects.

### SDG 11 — Sustainable Cities and Communities

Supports better monitoring of community infrastructure development.

### SDG 16 — Peace, Justice and Strong Institutions

Supports transparency, accountability, traceability and responsible institutional processes.

---

# 🔮 Future Enhancements

Potential future improvements include:

* Integration with official MPLADS/e-SAKSHI APIs
* Real-time government data ingestion
* More advanced anomaly detection
* NLP-based document similarity
* Automated document verification
* Satellite/image-based project progress verification
* GIS district boundary visualization
* Mobile application
* Advanced analytics dashboards
* Notification and alert system
* Historical project trend analysis
* Improved ML models with larger real-world datasets

---

# ⚠️ Important Limitation

This prototype is designed as an **AI-assisted monitoring and decision-support system**.

AI-generated risk indicators and anomalies should not be treated as proof of fraud or wrongdoing.

Final verification and administrative decisions should remain with authorized human officials.

---

# 🧠 Design Philosophy

The system follows three major principles:

### 1. AI-Assisted

AI helps identify patterns that may require attention.

### 2. Explainable

The system provides understandable indicators instead of relying only on black-box predictions.

### 3. Human-Controlled

Officials remain responsible for verification and final administrative decisions.

---

# 🏆 Smart India Hackathon

**Problem Statement ID:** SIH26102

**Project:** AI-Powered MPLAD Monitoring System

The solution focuses on improving the monitoring and verification workflow for MPLAD projects through AI-assisted risk identification, anomaly detection, benchmarking and transparent human verification.

---

# 🎥 Demo

Watch the complete prototype demonstration:

**YouTube:**
https://youtu.be/ID42lNr8OoA

---

# 🔗 Project Links

### GitHub Repository

https://github.com/rohanp-02/AI-MPLAD-Monitoring-System

### Live Prototype

https://ai-mplad-monitoring-system.onrender.com

### YouTube Demo

https://youtu.be/ID42lNr8OoA

---

# 👨‍💻 Project

**AI-Powered MPLAD Monitoring System**

Developed as a Smart India Hackathon solution for AI-assisted monitoring, risk identification and transparent verification of MPLAD projects.

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.

---

**AI identifies risk indicators. Humans verify. Decisions remain accountable.**




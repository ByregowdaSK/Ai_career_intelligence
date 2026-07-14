# 🚀 AI-Based Career and Skill Gap Analysis System

An AI-powered web application that helps students analyze their resumes, identify skill gaps, receive personalized career recommendations, and interact with an AI chatbot for career guidance. The system also provides an admin dashboard to manage users, monitor analytics, and generate reports.

---

#  Features

## Student Module

* User Registration and Login
* Secure Authentication
* Profile Management
* Resume Upload (PDF/DOCX/TXT)
* Resume Analysis and Scoring
* Automatic Skill Extraction
* Skill Gap Analysis
* AI-Based Career Recommendations
* Personalized Learning Roadmap
* AI Chatbot using OpenAI API

## Admin Module

* Admin Dashboard
* User Management
* Resume Analytics
* Chatbot Usage Analytics
* Career Recommendation Statistics
* PDF Report Generation
* User Activity Monitoring

---

#  Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Chart.js

### Backend

* Python
* Flask

### Database

* MySQL

### AI Integration

* OpenAI API

### Libraries

* PyPDF2
* python-docx
* ReportLab
* Pandas

---

#  Project Structure

```text
career_intelligence/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── routes/
│   ├── auth_routes.py
│   ├── main_routes.py
│   └── admin_routes.py
│
├── models/
│   └── user_model.py
│
├── utils/
│   ├── resume_parser.py
│   ├── career_engine.py
│   └── chatbot.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── resume.html
│   ├── recommend.html
│   ├── chatbot.html
│   ├── admin.html
│   └── admin_users.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── uploads/
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git https://github.com/ByregowdaSK/Ai_career_intelligence
```

```bash
cd AI-Based-Career-and-Skill-Gap-Analysis-System
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Database Setup

Open MySQL and create the database:

```sql
CREATE DATABASE career_db;
```

Run your SQL script to create the required tables.

Update the MySQL credentials in your project configuration if needed.

---

## 5. Configure OpenAI API

Create a `.env` file in the project root and  API key:

```env
OPENAI_API_KEY= ...
```

---

## 6. Run the Project

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

#  Default Admin Login

**Email**

```text
admin@gmail.com
```

**Password**

```text
admin123
```

---

#  Project Modules

### Authentication

* User Registration
* Login
* Session Management

### Resume Analyzer

* Resume Upload
* Resume Parsing
* Skill Extraction
* Resume Scoring
* Feedback Generation

### Skill Gap Analysis

* Detect Missing Skills
* Compare with Career Requirements
* Technology Recommendations

### Career Recommendation

* Career Matching
* Learning Roadmap
* Recommendation Score

### AI Chatbot

* Career Guidance
* Resume Suggestions
* Learning Support
* Interview Preparation

### Admin Dashboard

* Manage Users
* View Analytics
* Monitor Resume Uploads
* Track Chatbot Usage
* Export PDF Reports

---

# Future Enhancements

* ATS Resume Compatibility Analysis
* Job Portal Integration
* LinkedIn Profile Analysis
* Mobile Application
* Cloud Deployment (AWS/Azure)
* Machine Learning Based Career Prediction
* Interview Question Generator
* Email Notifications

---

#  Author

**Byre Gowda S K**

Python Full Stack Developer

Email: [byregowdabyregowda146@gmail.com](mailto:byregowdabyregowda146@gmail.com)

---

#  License

This project is developed for educational and academic purposes.

# AI Resume Screening & Job Recommendation System

## 📌 Project Overview

AI Resume Screening & Job Recommendation System is a Machine Learning and NLP based web application.

The system analyzes a candidate's resume, compares it with job requirements, calculates a match score, identifies matched and missing skills, and recommends suitable job roles.

## 🎯 Objectives

- Automatically analyze resumes
- Extract technical skills
- Compare resume with job requirements
- Calculate resume/job match score
- Identify missing skills
- Recommend suitable jobs
- Help candidates understand their skill gaps

## 🛠️ Technologies Used

- Python
- Flask
- Machine Learning
- Natural Language Processing
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Pandas
- HTML
- CSS
- JavaScript
- PDF Text Extraction

## 🤖 Machine Learning

The project uses:

1. TF-IDF Vectorization
2. Cosine Similarity
3. Skill Matching
4. Weighted Match Score

## 📂 Project Structure

AI_Resume_Screening_Job_Recommendation/

├── app.py
├── ml_model.py
├── resume_parser.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── uploads/

## ⚙️ Installation

Create a virtual environment:

python -m venv venv

Activate it:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## ▶️ Run the Project

python app.py

Open the browser:

http://127.0.0.1:5000

## 🔄 Working Process

Resume PDF
        ↓
PDF Text Extraction
        ↓
NLP Processing
        ↓
Skill Detection
        ↓
TF-IDF Vectorization
        ↓
Cosine Similarity
        ↓
Match Score
        ↓
Skill Gap Analysis
        ↓
Job Recommendation

## 📊 Features

- Resume PDF upload
- Resume text extraction
- Job description matching
- ATS-style score
- Matched skills
- Missing skills
- Skill gap analysis
- Job recommendations
- Candidate ranking
- Responsive web interface

## 🚀 Future Improvements

- Database integration
- User login system
- Admin dashboard
- BERT/Sentence Transformer embeddings
- XGBoost/Random Forest ranking
- More job datasets
- OCR for scanned resumes
- AI chatbot
- Email job alerts

## 👨‍💻 Author

Your Name

## 📄 License

This project is developed for educational and academic purposes.
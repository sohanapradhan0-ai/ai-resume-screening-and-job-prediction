from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path

from ml_model import ResumeMatcher
from resume_parser import extract_text_from_pdf


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}

matcher = ResumeMatcher()


# -------------------------------
# JOB DATABASE
# -------------------------------

JOBS = [
    {
        "title": "Python Developer",
        "company": "TechCorp Solutions",
        "location": "Bangalore",
        "skills": [
            "python",
            "sql",
            "flask",
            "git",
            "rest api"
        ]
    },

    {
        "title": "AI/ML Engineer",
        "company": "NextGen AI",
        "location": "Hyderabad",
        "skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "pandas",
            "numpy"
        ]
    },

    {
        "title": "Data Analyst",
        "company": "DataWorks",
        "location": "Pune",
        "skills": [
            "python",
            "sql",
            "pandas",
            "excel",
            "power bi"
        ]
    },

    {
        "title": "Full Stack Developer",
        "company": "InnovateX",
        "location": "Remote",
        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js",
            "mongodb"
        ]
    }
]


# -------------------------------
# FILE CHECK
# -------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# -------------------------------
# JOB SCORING
# -------------------------------

def score_job(resume_text, job):

    job_text = " ".join(job["skills"])

    similarity_score = matcher.similarity_score(
        resume_text,
        job_text
    )

    matched = matcher.find_skills(
        resume_text,
        job["skills"]
    )

    missing = [
        skill
        for skill in job["skills"]
        if skill not in matched
    ]

    if job["skills"]:

        skill_score = (
            len(matched)
            / len(job["skills"])
            * 100
        )

    else:

        skill_score = 0

    final_score = (
        0.6 * skill_score
        + 0.4 * similarity_score
    )

    return (
        round(final_score, 1),
        matched,
        missing
    )


# -------------------------------
# HOME PAGE
# -------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    error = None

    if request.method == "POST":

        resume = request.files.get("resume")

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        # Check file
        if not resume or not resume.filename:

            error = "Please upload a PDF resume."

        elif not allowed_file(resume.filename):

            error = "Only PDF files are supported."

        else:

            filename = secure_filename(
                resume.filename
            )

            path = UPLOAD_FOLDER / filename

            resume.save(path)

            try:

                # Extract resume text
                resume_text = extract_text_from_pdf(
                    path
                )

                if not resume_text.strip():

                    raise ValueError(
                        "No readable text was found in the PDF."
                    )


                # ---------------------------
                # CUSTOM JOB DESCRIPTION
                # ---------------------------

                if job_description:

                    score = matcher.similarity_score(
                        resume_text,
                        job_description
                    )

                    job_skills = matcher.extract_skills(
                        job_description
                    )

                    matched = matcher.find_skills(
                        resume_text,
                        job_skills
                    )

                    missing = [
                        skill
                        for skill in job_skills
                        if skill not in matched
                    ]

                    if job_skills:

                        skill_score = (
                            len(matched)
                            / len(job_skills)
                            * 100
                        )

                    else:

                        skill_score = score

                    overall_score = round(
                        (
                            score
                            + skill_score
                        ) / 2,
                        1
                    )

                    analysis_title = (
                        "Custom Job Description"
                    )

                else:

                    overall_score = None

                    matched = []

                    missing = []

                    analysis_title = (
                        "Recommended Jobs"
                    )


                # ---------------------------
                # JOB RECOMMENDATIONS
                # ---------------------------

                recommendations = []

                for job in JOBS:

                    score, matched_skills, missing_skills = score_job(
                        resume_text,
                        job
                    )

                    recommendations.append({

                        **job,

                        "score": score,

                        "matched": matched_skills,

                        "missing": missing_skills

                    })


                # Highest score first
                recommendations.sort(
                    key=lambda x: x["score"],
                    reverse=True
                )


                result = {

                    "filename": filename,

                    "resume_preview":
                        resume_text[:700],

                    "overall_score":
                        overall_score,

                    "matched":
                        matched,

                    "missing":
                        missing,

                    "analysis_title":
                        analysis_title,

                    "recommendations":
                        recommendations
                }


            except Exception as exc:

                error = (
                    f"Could not analyze the resume: {exc}"
                )


    return render_template(
        "index.html",
        result=result,
        error=error
    )


# -------------------------------
# RUN APP
# -------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
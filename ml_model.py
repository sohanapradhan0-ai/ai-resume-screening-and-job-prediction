import re

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------
# SKILL DATABASE
# --------------------------------

SKILL_ALIASES = {

    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "dl"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "flask": [
        "flask"
    ],

    "django": [
        "django"
    ],

    "fastapi": [
        "fastapi"
    ],

    "html": [
        "html"
    ],

    "css": [
        "css"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "react": [
        "react",
        "react.js"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node"
    ],

    "mongodb": [
        "mongodb",
        "mongo db"
    ],

    "git": [
        "git",
        "github"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "api"
    ],

    "excel": [
        "excel",
        "ms excel"
    ],

    "power bi": [
        "power bi"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "docker": [
        "docker"
    ],

    "langchain": [
        "langchain"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ]
}


# --------------------------------
# RESUME MATCHER CLASS
# --------------------------------

class ResumeMatcher:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )


    # --------------------------------
    # TEXT SIMILARITY
    # --------------------------------

    def similarity_score(
        self,
        resume_text,
        job_text
    ):

        if (
            not resume_text.strip()
            or not job_text.strip()
        ):

            return 0.0


        matrix = self.vectorizer.fit_transform(
            [
                resume_text,
                job_text
            ]
        )


        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0] * 100


        return round(
            float(score),
            1
        )


    # --------------------------------
    # FIND MATCHED SKILLS
    # --------------------------------

    def find_skills(
        self,
        text,
        skills
    ):

        text_lower = text.lower()

        found = []


        for skill in skills:

            aliases = SKILL_ALIASES.get(
                skill.lower(),
                [skill.lower()]
            )


            for alias in aliases:

                pattern = (
                    r"(?<!\w)"
                    + re.escape(alias)
                    + r"(?!\w)"
                )


                if re.search(
                    pattern,
                    text_lower
                ):

                    found.append(skill)

                    break


        return found


    # --------------------------------
    # EXTRACT SKILLS
    # --------------------------------

    def extract_skills(
        self,
        text
    ):

        text_lower = text.lower()

        found = []


        for canonical, aliases in SKILL_ALIASES.items():

            for alias in aliases:

                pattern = (
                    r"(?<!\w)"
                    + re.escape(alias)
                    + r"(?!\w)"
                )


                if re.search(
                    pattern,
                    text_lower
                ):

                    found.append(canonical)

                    break


        return found
# ==========================================
# 🚀 CAREER + SKILL GAP ENGINE
# ==========================================

CAREER_PATHS = {

    "Full Stack Developer": {

        "skills": [

            "html",
            "css",
            "javascript",
            "react",
            "nodejs",
            "mysql",
            "python",
            "flask"

        ]
    },

    "Frontend Developer": {

        "skills": [

            "html",
            "css",
            "javascript",
            "react",
            "bootstrap"

        ]
    },

    "Backend Developer": {

        "skills": [

            "python",
            "flask",
            "mysql",
            "java"

        ]
    },

    "Data Scientist": {

        "skills": [

            "python",
            "pandas",
            "numpy",
            "machinelearning"

        ]
    },

    "Machine Learning Engineer": {

        "skills": [

            "python",
            "tensorflow",
            "pytorch",
            "machinelearning",
            "numpy"

        ]
    },

    "DevOps Engineer": {

        "skills": [

            "docker",
            "kubernetes",
            "aws",
            "git"

        ]
    },

    "Cloud Engineer": {

        "skills": [

            "aws",
            "azure",
            "googlecloud",
            "docker"

        ]
    },

    "Mobile App Developer": {

        "skills": [

            "java",
            "kotlin"

        ]
    }

}


# ==========================================
# ✅ NORMALIZE SKILL
# ==========================================

def normalize_skill(skill):

    skill = skill.strip().lower()
    
    replacements = {

    "c++": "cpp",

    "c#": "csharp",

    "node.js": "nodejs",

    "vue.js": "vuejs",

    "express.js": "expressjs",

    "google cloud": "googlecloud",

    "machine learning": "machinelearning",

    "deep learning": "deeplearning",

    "data science": "datascience",

    "computer vision": "computervision",

    "ci/cd": "cicd",

    "react native": "reactnative"
    }

    return replacements.get(skill, skill)


# ==========================================
# 🎯 ANALYZE CAREERS
# ==========================================

def analyze_careers(skills):

    if not skills:
        return []

    user_skills = [

        normalize_skill(s)

        for s in skills.split(',')

        if s.strip()

    ]

    results = []

    for career, data in CAREER_PATHS.items():

        required_skills = data["skills"]

        matched = [

            skill for skill in required_skills

            if skill in user_skills

        ]

        missing = [

            skill for skill in required_skills

            if skill not in user_skills

        ]

        score = int(
            (len(matched) / len(required_skills)) * 100
        )

        results.append({

            "career": career,

            "score": score,

            "matched_skills": matched,

            "missing_skills": missing,

            "roadmap": generate_roadmap(missing)

        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


# ==========================================
# 🧠 VALIDATE SKILLS
# ==========================================

VALID_SKILLS = [

    # LANGUAGES

    "python",
    "java",
    "c",
    "cpp",
    "csharp",
    "javascript",
    "typescript",
    "php",
    "go",
    "rust",
    "swift",
    "kotlin",
    "r",

    # WEB

    "html",
    "css",
    "bootstrap",
    "react",
    "angular",
    "vuejs",
    "nodejs",
    "flask",
    "django",
    "expressjs",
    "spring",
    "sql",

    # DATABASE

    "mysql",
    "mongodb",
    "postgresql",
    "sqlite",
    "oracle",
    "firebase",

    # AI

    "machinelearning",
    "deeplearning",
    "datascience",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "computervision",
    "nlp",

    # CLOUD

    "aws",
    "azure",
    "googlecloud",
    "docker",
    "kubernetes",
    "git",
    "github",
    "cicd",
    "linux",

    # MOBILE

    "flutter",
    "reactnative"

]


def validate_user_skills(skills):

    user_skills = [

        normalize_skill(s)

        for s in skills.split(',')

        if s.strip()

    ]

    invalid = []

    for skill in user_skills:

        if skill not in VALID_SKILLS:

            invalid.append(skill)

    return invalid


# ==========================================
# 📚 ROADMAP
# ==========================================

def generate_roadmap(missing_skills):

    roadmap = []

    week = 1

    for skill in missing_skills:

        roadmap.append(
            f"Week {week}-{week+1}: Learn {skill.title()}"
        )

        week += 2

    return roadmap


# ==========================================
# 📊 SCORE CALCULATOR
# ==========================================

def calculate_score(user_skills, required_skills):

    if not required_skills:
        return 0

    matched = [

        skill for skill in required_skills

        if skill in user_skills

    ]

    score = int(
        (len(matched) / len(required_skills)) * 100
    )

    return score
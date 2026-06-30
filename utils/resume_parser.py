import re

print("✅ resume_parser LOADED")


# ==========================================
# 📄 TEXT EXTRACTION
# ==========================================

def extract_text(file):
    
    file.seek(0)

    filename = file.filename.lower()

    data = file.read()

    # ---------- PDF ----------
    if filename.endswith('.pdf'):

        try:
            from PyPDF2 import PdfReader
            import io

            reader = PdfReader(io.BytesIO(data))

            text = ""

            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"

            return text

        except Exception:
            return ""

    # ---------- DOCX ----------
    elif filename.endswith('.docx'):

        try:
            from docx import Document
            import io

            doc = Document(io.BytesIO(data))

            return "\n".join(
                [p.text for p in doc.paragraphs]
            )

        except Exception:
            return ""

    # ---------- TXT ----------
    elif filename.endswith('.txt'):

        try:
            return data.decode(
                "utf-8",
                errors="ignore"
            )

        except Exception:
            return ""

    return ""


# ==========================================
# 🧠 SKILLS DATABASE
# ==========================================

SKILLS_DB = [

    # Programming
    "python", "java", "c", "c++", "c#",
    "javascript", "typescript", "php",
    "go", "rust", "swift", "kotlin",

    # Web
    "html", "css", "bootstrap",
    "react", "angular", "vue.js",
    "node.js", "express.js",

    # Backend
    "django", "flask",
    "spring", "spring boot",
    "laravel", ".net",

    # Database
    "sql", "mysql", "mongodb",
    "postgresql", "sqlite",
    "firebase", "oracle",

    # AI / Data Science
    "machine learning",
    "deep learning",
    "data science",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "computer vision",
    "nlp",

    # Cloud / DevOps
    "aws", "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "git", "github",
    "ci/cd",

    # Tools
    "linux",
    "excel",
    "power bi",
    "tableau"
]


# ==========================================
# 🔍 SKILL EXTRACTION
# ==========================================

def extract_skills(text):

    text = text.lower()

    found = set()

    for skill in SKILLS_DB:

        if skill.lower() in text:
            found.add(skill)

    return sorted(list(found))


# ==========================================
# 📑 SECTION CHECKER
# ==========================================

def has_section(text, keywords):

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )


# ==========================================
# 📊 RESUME ANALYSIS
# ==========================================

def analyze_resume(text):

    text_lower = text.lower()

    # ---------- Sections ----------
    sections = {

        "education": has_section(
            text_lower,
            ["education", "academic"]
        ),

        "projects": has_section(
            text_lower,
            ["project", "projects"]
        ),

        "experience": has_section(
            text_lower,
            ["experience", "internship", "work"]
        ),

        "skills_section": has_section(
            text_lower,
            ["skills", "technical skills"]
        ),

        "certifications": has_section(
            text_lower,
            ["certification", "certifications"]
        )
    }

    # ---------- Skills ----------
    detected_skills = extract_skills(text_lower)

    # ---------- Score ----------
    score = 0

    # Section scores
    score += 15 if sections["education"] else 0
    score += 20 if sections["projects"] else 0
    score += 20 if sections["experience"] else 0
    score += 15 if sections["skills_section"] else 0
    score += 10 if sections["certifications"] else 0

    # Skills score
    score += min(len(detected_skills) * 2, 20)

    # Extra resume quality checks
    if len(text.split()) > 300:
        score += 5

    # Limit to 100
    score = min(score, 100)

    # ==========================================
    # 💡 FEEDBACK
    # ==========================================

    feedback = []

    if not sections["education"]:
        feedback.append(
            "Add Education section"
        )

    if not sections["projects"]:
        feedback.append(
            "Add Projects section"
        )

    if not sections["experience"]:
        feedback.append(
            "Add Experience or Internship details"
        )

    if not sections["skills_section"]:
        feedback.append(
            "Add Technical Skills section"
        )

    if not sections["certifications"]:
        feedback.append(
            "Add Certifications section"
        )

    if len(detected_skills) < 5:
        feedback.append(
            "Add more technical skills"
        )

    if len(text.split()) < 250:
        feedback.append(
            "Resume content is too short"
        )

    # ==========================================
    # 🏆 RESUME LEVEL
    # ==========================================

    if score >= 85:
        level = "Excellent"

    elif score >= 70:
        level = "Good"

    elif score >= 50:
        level = "Average"

    else:
        level = "Needs Improvement"

    # ==========================================
    # 📦 FINAL RESULT
    # ==========================================

    return {

        "score": score,

        "level": level,

        "sections": sections,

        "detected_skills": detected_skills,

        "feedback": feedback
    }


print("Functions:", dir())
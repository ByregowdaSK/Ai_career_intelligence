def get_career_recommendations(skills):
    if not skills:
        return ["Add skills first"]

    skills_list = [s.strip().lower() for s in skills.split(',')]

    careers = []

    if "python" in skills_list:
        careers.append("Data Scientist")

    if "html" in skills_list or "css" in skills_list:
        careers.append("Web Developer")

    if "java" in skills_list:
        careers.append("Backend Developer")

    if not careers:
        careers.append("Software Engineer")

    return careers


def get_skill_gap(skills):
    if not skills:
        return ["Add skills"]

    skills_list = [s.strip().lower() for s in skills.split(',')]

    gaps = []

    if "python" in skills_list and "sql" not in skills_list:
        gaps.append("Learn SQL")

    if "html" in skills_list and "javascript" not in skills_list:
        gaps.append("Learn JavaScript")

    if "java" in skills_list and "spring" not in skills_list:
        gaps.append("Learn Spring Boot")

    if not gaps:
        gaps.append("No major gaps")

    return gaps


def generate_roadmap(gaps):
    roadmap = []
    week = 1

    for g in gaps:
        roadmap.append(f"Week {week}-{week+1}: {g}")
        week += 2

    return roadmap


def calculate_score(skills, gaps):
    if not skills:
        return 0

    total_skills = len(skills.split(','))
    gap_count = len(gaps)

    if total_skills == 0:
        return 0

    score = int(((total_skills - gap_count) / total_skills) * 100)
    return score
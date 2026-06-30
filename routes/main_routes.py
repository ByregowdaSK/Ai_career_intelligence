from flask import Blueprint, render_template, request, redirect, session
from models.user_model import get_user_by_id
from utils.resume_parser import (
    extract_text,
    analyze_resume
)

# =========================================================
# CHATBOT
# =========================================================

from utils.chatbot import ask_ai

# =========================================================
# DATABASE
# =========================================================

from db import get_db_connection

# =========================================================
# MODELS
# =========================================================

from models.user_model import (

    get_user_skills,

    update_user_skills,

    save_resume_data,

    get_resume_data

)

# =========================================================
# AI / LOGIC
# =========================================================

from utils.skill_gap import (

    analyze_careers,

    validate_user_skills

)

# =========================================================
# BLUEPRINT
# =========================================================

main = Blueprint(

    'main',

    __name__

)

# =========================================================
# DASHBOARD
# =========================================================

@main.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('is_admin'):
        return redirect('/admin')

    user = get_user_skills(
        session['user_id']
    )

    skills_str = ""

    if user and user.get('skills'):

        skills_str = user['skills']

    skills_list = []

    if skills_str:

        skills_list = [

            s.strip()

            for s in skills_str.split(',')

            if s.strip()

        ]

    resume_score = 0

    saved_resume = get_resume_data(
        session['user_id']
    )

    if saved_resume:

        resume_score = saved_resume.get(
            'resume_score',
            0
        )

    return render_template(

        'dashboard.html',

        name=session.get('name'),

        skills=skills_list,

        skills_count=len(skills_list),

        resume_score=resume_score

    )

# =========================================================
# PROFILE
# =========================================================

@main.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'user_id' not in session:
        return redirect('/login')

    message = None

    error = None

    if request.method == 'POST':

        skills_list = request.form.getlist(
            'skills'
        )

        skills_str = ",".join(
            skills_list
        )

        invalid_skills = validate_user_skills(
            skills_str
        )

        if invalid_skills:

            error = (
                "Only IT skills allowed. "
                f"Invalid: {', '.join(invalid_skills)}"
            )

        else:

            update_user_skills(

                session['user_id'],

                skills_str

            )

            message = "Skills updated successfully"

    user = get_user_skills(
        session['user_id']
    )

    selected_skills = []

    if user:

        skills_data = user.get(
            'skills'
        )

        if skills_data:

            selected_skills = [

                skill.strip()

                for skill in skills_data.split(',')

                if skill.strip()

            ]

    return render_template(

        'profile.html',

        selected_skills=selected_skills,

        message=message,

        error=error

    )

@main.route('/recommend')
def recommend():

    if 'user_id' not in session:
        return redirect('/login')

    user = get_user_by_id(session['user_id'])

    skills = user.get('skills') or ''

    results = analyze_careers(skills)

    return render_template(
        'recommend.html',
        skills=skills,
        results=results
    )

# =========================================================
# RESULTS
# =========================================================

@main.route('/results')
def results():

    if 'user_id' not in session:
        return redirect('/login')

    user = get_user_skills(
        session['user_id']
    )

    skills = ""

    if user and user.get('skills'):

        skills = user['skills']

    results = analyze_careers(
        skills
    )

    # =====================================================
    # SAVE RECOMMENDATIONS
    # =====================================================

    recommended_careers = ",".join([

        r['career']

        for r in results

    ])

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE tbl_user

        SET recommendation_count=%s,
            recommended_careers=%s

        WHERE id=%s

    """, (

        len(results),

        recommended_careers,

        session['user_id']

    ))

    conn.commit()

    conn.close()

    return render_template(

        'result.html',

        skills=skills,

        results=results

    )

# =========================================================
# RESUME ANALYZER
# =========================================================

@main.route('/resume', methods=['GET', 'POST'])
def resume():

    if 'user_id' not in session:
        return redirect('/login')

    result = None

    results = None

    saved_resume = get_resume_data(
        session['user_id']
    )

    if request.method == 'POST':

        file = request.files.get(
            'resume'
        )

        if file:

            filename = file.filename

            # =================================================
            # REAL RESUME ANALYSIS
            # =================================================

            file.seek(0)

            resume_text = extract_text(file)
            resume_text = extract_text(file)

            print("\n===== RESUME TEXT =====")
            print(resume_text[:1000])

            result = analyze_resume(resume_text)

            print("\n===== ANALYSIS RESULT =====")
            print(result)

            result = analyze_resume(resume_text)
            # =================================================
            # CAREER ANALYSIS
            # =================================================

            skills_string = ",".join(
            result.get('detected_skills', [])
            )

            results = analyze_careers(
                skills_string
            )

            # =================================================
            # SAVE RECOMMENDATIONS
            # =================================================

            recommended_careers = ",".join([

                r['career']

                for r in results

            ])

            conn = get_db_connection()

            cursor = conn.cursor()

            cursor.execute("""

                UPDATE tbl_user

                SET recommendation_count=%s,
                    recommended_careers=%s

                WHERE id=%s

            """, (

                len(results),

                recommended_careers,

                session['user_id']

            ))

            conn.commit()

            conn.close()

            # =================================================
            # EXTRACT CAREERS
            # =================================================

            career_names = []

            roadmaps = []

            for r in results[:3]:

                career_names.append(
                    r['career']
                )

                for step in r['roadmap'][:3]:

                    roadmaps.append(
                        step
                    )

            careers_string = ",".join(
                career_names
            )

            roadmap_string = " | ".join(
                roadmaps
            )

            # =================================================
            # SAVE TO DATABASE
            # =================================================

            save_resume_data(

                session['user_id'],

                filename,

                result['score'],

                skills_string,

                careers_string,

                roadmap_string

            )

            saved_resume = get_resume_data(
                session['user_id']
            )

    return render_template(

        'resume.html',

        result=result,

        results=results,

        saved_resume=saved_resume

    )

# =========================================================
# CHATBOT
# =========================================================

@main.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    if 'user_id' not in session:
        return redirect('/login')

    answer = None

    question = ""

    if request.method == 'POST':

        question = request.form.get(
            'question'
        )

        answer = ask_ai(
            question
        )

        # =================================================
        # UPDATE CHATBOT USAGE
        # =================================================

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE tbl_user

            SET chatbot_usage =
            chatbot_usage + 1

            WHERE id=%s

        """, (

            session['user_id'],

        ))

        conn.commit()

        conn.close()

    return render_template(

        'chatbot.html',

        answer=answer,

        question=question

    )
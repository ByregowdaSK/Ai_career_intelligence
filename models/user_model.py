from db import get_db_connection
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tbl_user WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()
    conn.close()
    return user
def get_user_skills(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tbl_user WHERE id=%s",
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result
def update_user_skills(user_id, skills):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbl_user SET skills=%s WHERE id=%s",
        (skills, user_id)
    )
    conn.commit()
    conn.close()
def save_resume_data(
    user_id,
    filename,
    score,
    skills,
    careers,
    roadmap
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbl_user
        SET
            resume_uploaded = 1,
            resume_filename = %s,
            resume_score = %s,
            detected_skills = %s,
            recommended_careers = %s,
            career_roadmap = %s
        WHERE id = %s
    """, (
        filename,
        score,
        skills,
        careers,
        roadmap,
        user_id
    ))
    conn.commit()
    conn.close()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbl_user
        SET
            resume_uploaded = 1,
            resume_filename = %s,
            resume_score = %s,
            detected_skills = %s

        WHERE id = %s
    """, (

        filename,
        score,
        skills,
        user_id
    ))
    conn.commit()
    conn.close()
def get_resume_data(user_id):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""

        SELECT
            resume_uploaded,
            resume_filename,
            resume_score,
            detected_skills,
            recommended_careers,
            career_roadmap

        FROM tbl_user

        WHERE id = %s

    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result
def get_all_users():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM tbl_user
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users


def delete_user_by_id(user_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tbl_user
        WHERE id = %s
    """, (user_id,))

    conn.commit()

    conn.close()
def get_total_users():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tbl_user"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_admins():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tbl_user
        WHERE LOWER(TRIM(role))='admin'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_students():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tbl_user
        WHERE LOWER(TRIM(role))='student'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_resume_uploaded_count():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tbl_user
        WHERE resume_uploaded = 1
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_chatbot_usage():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(chatbot_usage)
        FROM tbl_user
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0


def get_total_recommendations():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(recommendation_count)
        FROM tbl_user
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0
def update_recommendation_count(user_id, count):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_user
        SET recommendation_count=%s
        WHERE id=%s
    """, (count, user_id))

    conn.commit()

    conn.close()
def get_user_by_id(user_id):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""

        SELECT *
        FROM tbl_user
        WHERE id = %s

    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user

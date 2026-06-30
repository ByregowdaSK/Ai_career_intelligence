from flask import Blueprint, render_template, session, redirect, request
import pandas as pd
import os
import tempfile

from flask import send_file

from models.user_model import (

    get_all_users,

    delete_user_by_id

)

# =====================================================
# BLUEPRINT
# =====================================================

admin = Blueprint(

    'admin',

    __name__,

    url_prefix='/admin'

)

# =====================================================
# ADMIN DASHBOARD
# =====================================================

@admin.route('/')
def admin_dashboard():

    # =================================================
    # LOGIN CHECK
    # =================================================

    if 'user_id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return redirect('/dashboard')

    # =================================================
    # FETCH USERS FROM DATABASE
    # =================================================

    users = get_all_users()

    # =================================================
    # TOTAL USERS
    # =================================================

    total_users = len(users)

    # =================================================
    # TOTAL ADMINS
    # =================================================

    admins = [

        u for u in users

        if str(
            u.get('role', '')
        ).strip().lower() == 'admin'

    ]

    # =================================================
    # TOTAL STUDENTS
    # =================================================

    students = [

        u for u in users

        if str(
            u.get('role', '')
        ).strip().lower() == 'student'

    ]

    # =================================================
    # RESUME UPLOAD COUNT
    # =================================================

    resume_uploaded = len([

        u for u in users

        if u.get('resume_uploaded')

    ])

    # =================================================
    # TOTAL CHATBOT USAGE
    # =================================================

    total_chatbot_usage = sum([

        int(
            u.get('chatbot_usage', 0) or 0
        )

        for u in users

    ])

    # =================================================
    # TOTAL RECOMMENDATIONS
    # =================================================

    total_recommendations = sum([

        int(
            u.get('recommendation_count', 0) or 0
        )

        for u in users

    ])

    # =================================================
    # AVERAGE RESUME SCORE
    # =================================================

    scores = [

        int(u.get('resume_score'))

        for u in users

        if u.get('resume_score')

    ]

    avg_resume_score = 0

    if scores:

        avg_resume_score = round(

            sum(scores) / len(scores)

        )

    # =================================================
    # RENDER TEMPLATE
    # =================================================

    return render_template(

        'admin.html',

        users=users,

        total_users=total_users,

        total_admins=len(admins),

        total_students=len(students),

        resume_uploaded=resume_uploaded,

        total_chatbot_usage=total_chatbot_usage,

        total_recommendations=total_recommendations,

        avg_resume_score=avg_resume_score

    )

# =====================================================
# MANAGE USERS
# =====================================================

@admin.route('/users')
def manage_users():

    # =================================================
    # LOGIN CHECK
    # =================================================

    if 'user_id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return redirect('/dashboard')

    # =================================================
    # PAGINATION
    # =================================================

    page = int(

        request.args.get('page', 1)

    )

    per_page = 5

    users = get_all_users()

    total_users = len(users)

    total_pages = (

        total_users + per_page - 1

    ) // per_page

    start = (page - 1) * per_page

    end = start + per_page

    paginated_users = users[start:end]

    # =================================================
    # RENDER TEMPLATE
    # =================================================

    return render_template(

        'admin_users.html',

        users=paginated_users,

        page=page,

        total_pages=total_pages

    )

# =====================================================
# DELETE USER
# =====================================================

@admin.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    # =================================================
    # LOGIN CHECK
    # =================================================

    if 'user_id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return redirect('/dashboard')

    # =================================================
    # DELETE USER
    # =================================================

    delete_user_by_id(user_id)

    return redirect('/admin/users')

# =====================================================
# EXPORT USERS PDF REPORT
# =====================================================

@admin.route('/export_users')
def export_users():

    # =================================================
    # LOGIN CHECK
    # =================================================

    if 'user_id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return redirect('/dashboard')

    # =================================================
    # REPORTLAB IMPORTS
    # =================================================

    from reportlab.platypus import (

        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer

    )

    from reportlab.lib import colors

    from reportlab.lib.styles import (

        getSampleStyleSheet,
        ParagraphStyle

    )

    from reportlab.lib.pagesizes import (

        landscape,
        letter

    )

    from reportlab.lib.enums import TA_CENTER

    # =================================================
    # FETCH USERS
    # =================================================

    users = get_all_users()

    # =================================================
    # TEMP FILE PATH
    # =================================================

    filepath = os.path.join(

        tempfile.gettempdir(),

        'users_report.pdf'

    )

    # =================================================
    # PDF DOCUMENT
    # =================================================

    doc = SimpleDocTemplate(

        filepath,

        pagesize=landscape(letter),

        rightMargin=15,
        leftMargin=15,
        topMargin=20,
        bottomMargin=20

    )

    styles = getSampleStyleSheet()

    elements = []

    # =================================================
    # TITLE STYLE
    # =================================================

    title_style = ParagraphStyle(

        'TitleStyle',

        parent=styles['Heading1'],

        alignment=TA_CENTER,

        fontSize=24,

        textColor=colors.HexColor('#1e3a8a'),

        spaceAfter=20

    )

    # =================================================
    # TITLE
    # =================================================

    title = Paragraph(

        "Career AI - Complete Users Report",

        title_style

    )

    elements.append(title)

    # =================================================
    # SUMMARY
    # =================================================

    total_users = len(users)

    total_students = len([

        u for u in users

        if str(
            u.get('role','')
        ).lower() == 'student'

    ])

    total_admins = len([

        u for u in users

        if str(
            u.get('role','')
        ).lower() == 'admin'

    ])

    summary = Paragraph(

        f"""

        <b>Total Users:</b> {total_users}
        &nbsp;&nbsp;&nbsp;&nbsp;

        <b>Students:</b> {total_students}
        &nbsp;&nbsp;&nbsp;&nbsp;

        <b>Admins:</b> {total_admins}

        """,

        styles['Normal']

    )

    elements.append(summary)

    elements.append(

        Spacer(1,20)

    )

    # =================================================
    # TABLE HEADERS
    # =================================================

    data = [[

        'ID',
        'Name',
        'Email',
        'Role',
        'Skills',
        'Resume',
        'Score',
        'AI Chats',
        'Recommendations',
        'Last Login'

    ]]

    # =================================================
    # TABLE ROWS
    # =================================================

    for user in users:

        skills = str(

            user.get('skills')
            or 'No Skills'

        )

        # LIMIT LONG TEXT

        if len(skills) > 120:

            skills = skills[:120] + " ..."

        data.append([

            str(
                user.get('id')
            ),

            Paragraph(

                str(
                    user.get('name')
                ),

                styles['BodyText']

            ),

            Paragraph(

                str(
                    user.get('email')
                ),

                styles['BodyText']

            ),

            str(
                user.get('role')
            ),

            Paragraph(

                skills,

                styles['BodyText']

            ),

            "Yes"

            if user.get(
                'resume_uploaded'
            )

            else "No",

            str(
                user.get('resume_score')
                or 0
            ),

            str(
                user.get('chatbot_usage')
                or 0
            ),

            str(
                user.get(
                    'recommendation_count'
                ) or 0
            ),

            str(
                user.get('last_login')
                or 'N/A'
            )

        ])

    # =================================================
    # TABLE
    # =================================================

    table = Table(

        data,

        repeatRows=1,

        colWidths=[

            35,     # ID
            85,     # Name
            145,    # Email
            55,     # Role
            180,    # Skills
            60,     # Resume
            55,     # Score
            55,     # AI Chats
            80,     # Recommendations
            100     # Last Login

        ]

    )

    # =================================================
    # TABLE STYLE
    # =================================================

    table.setStyle(

        TableStyle([

            # HEADER

            (
                'BACKGROUND',
                (0,0),
                (-1,0),
                colors.HexColor('#1e3a8a')
            ),

            (
                'TEXTCOLOR',
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                'FONTNAME',
                (0,0),
                (-1,0),
                'Helvetica-Bold'
            ),

            (
                'FONTSIZE',
                (0,0),
                (-1,-1),
                8
            ),

            (
                'BOTTOMPADDING',
                (0,0),
                (-1,0),
                10
            ),

            # BODY

            (
                'BACKGROUND',
                (0,1),
                (-1,-1),
                colors.beige
            ),

            (
                'GRID',
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),

            (
                'VALIGN',
                (0,0),
                (-1,-1),
                'TOP'
            ),

            (
                'WORDWRAP',
                (0,0),
                (-1,-1),
                'LTR'
            )

        ])

    )

    elements.append(table)

    # =================================================
    # BUILD PDF
    # =================================================

    doc.build(elements)

    # =================================================
    # DOWNLOAD PDF
    # =================================================

    return send_file(

        filepath,

        as_attachment=True

    )
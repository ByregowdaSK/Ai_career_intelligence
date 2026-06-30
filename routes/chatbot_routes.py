from flask import Blueprint, render_template, request

chatbot = Blueprint("chatbot", __name__)


@chatbot.route('/chatbot', methods=['GET', 'POST'])
def chatbot_page():

    answer = None
    question = ""

    if request.method == 'POST':

        question = request.form.get('question')

        answer = "This is AI test response showing successfully on page."

        print(answer)   

    return render_template(
        'chatbot.html',
        answer=answer,
        question=question
    )
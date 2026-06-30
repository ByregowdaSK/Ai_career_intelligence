from flask import Flask, redirect, session
import os
from datetime import timedelta
from extensions import mail
from routes.chatbot_routes import chatbot

from routes.auth_routes import auth
from routes.main_routes import main
from routes.admin import admin   # ✅ IMPORTANT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

app.secret_key = "1234567890"

# ✅ REGISTER BLUEPRINTS
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(chatbot)
app.config['MAIL_SERVER'] = 'sp.gmail.com'
app.config['MAIL_PORT'] = 123
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'asdfghjkl.project@gmail.com'
app.config['MAIL_PASSWORD'] = 'asdfghjkl'

mail.init_app(app)

# DEBUG ROUTES
print(app.url_map)

app.permanent_session_lifetime = timedelta(minutes=20)

@app.before_request
def make_session_permanent():

    session.permanent = True

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

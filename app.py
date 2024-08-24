from flask import Flask, render_template, request, jsonify, flash, make_response
from flask_mail import Mail, Message

import os

app = Flask(__name__)

USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')
KEY = os.environ.get('SECRET_KEY')

app.config['MAIL_SERVER'] = 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = USERNAME
app.config['MAIL_PASSWORD'] = PASSWORD
app.config['SECRET_KEY'] = KEY
mail = Mail(app)

@app.route('/')
def landing_page():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        req = request.get_json()
        name = req['name']
        email = req['email']
        subject = req['subject']
        message = req['message']

        msg = Message(subject, sender="info@yoshnee-raveendran.com", recipients=["yoshn91@gmail.com"])
        msg.body = "From: " + email + "\n\n" + message

        try:
            mail.send(msg)
            return make_response(jsonify({"response": "Your message has been sent. Thank you!"}), 200)
        except BaseException as e:
            return make_response(jsonify({"response": "Failed to send message, Please try again!"}), 500)


if __name__ == '__main__':
    app.run()
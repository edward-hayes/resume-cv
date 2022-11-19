from flask import Flask
from flask import render_template, redirect, url_for, request
from mailer import Email as Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

now = date.today()
year = now.year

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

mail = Mail()

class MyForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    subject = StringField(label="Subject", validators=[DataRequired()])
    message = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Send Message")

@app.route('/', methods=["GET","POST"])
def home():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            message = form.message.data
            mail.send_msg(
            to_address=os.getenv("TO_ADDRESS"),
            subject=f"WEBSITE: {name} sent you a message",
            message=f"Name: {name}\nEmail: {email}\n\nSubject:{subject}\n{message}"
            )
            return redirect(url_for('thanks',name=name))
        else:
            return render_template("index.html",form=form,error=True, year=year)
    else:
        return render_template("index.html",form=form, year=year)

@app.route('/thanks')
def thanks():
    name = request.args.get('name')
    return render_template('success.html',name=name, year=year)

if __name__ == "__main__":
    app.run()

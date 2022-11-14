from flask import Flask
from flask import render_template, redirect, url_for, request
from mailer import Email as Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = "yXEThxdFPfPWHtRwkWhy"

mail = Mail()
TO_ADDRESS = "hayesejh@gmail.com"

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
            print(f"form validated \nname: {name}\nemail: {email}\nsubject: {subject}\nmessage:{message}\n")
            return redirect(url_for('home'))
        else:
            return render_template("index.html",form=form,error=True)
    else:
        return render_template("index.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)
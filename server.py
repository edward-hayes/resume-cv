import json
import time
from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request
from flask_simple_captcha import CAPTCHA
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

## Captcha setup
secret_captcha_key = os.getenv("SECRET_CAPTCHA_KEY")
CAPTCHA_CONFIG = {
    'SECRET_CAPTCHA_KEY': secret_captcha_key,
    'METHOD': 'pbkdf2:sha256:100',
    'CAPTCHA_LENGTH': 5,
    'CAPTCHA_DIGITS': False,
    }

CAPTCHA = CAPTCHA(config=CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)


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
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if form.validate_on_submit():
            if CAPTCHA.verify(c_text, c_hash):
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
                captcha = CAPTCHA.create()
                return render_template("index.html",form=form, error=True, captcha_error=True, year=year, captcha=captcha)
        else:
            captcha = CAPTCHA.create()
            return render_template("index.html",form=form, error=True, year=year, captcha=captcha)
    else:
        captcha = CAPTCHA.create()
        return render_template("index.html",form=form, year=year, captcha=captcha)

@app.route('/thanks')
def thanks():
    name = request.args.get('name')
    return render_template('success.html',name=name, year=year)

########  EXTRA LSX ROUTES  ########

EXAMPLE_PRODUCT = "b76dc8f4-4e5d-40be-8a37-f09507bfb66d" ## testlspayexclusive "egg"
def receive_and_verify(request):
    try:
        json_data = request.get_json()

        if json_data and 'event_type' in json_data:
            print("request received:\n", json.dumps(json_data, indent=2))
            return True
        else:
            print("unknown request received:\n", request.args)
            return False
    except Exception as e:
        # Handle any exceptions and return an error response
        return False

@app.route('/lsx-1605/require_custom_fields_sale', methods=['POST'])
def require_custom_fields_sale():
    if receive_and_verify(request):
        data = request.json
        if "sale" in data and "custom_fields" in data["sale"] and len(data["sale"]['custom_fields']) > 0: # if custom fields are already set, don't require them again
            return {"actions": []}
        else:
            response_payload = {
                    "actions": [
                        {
                        "type": "require_custom_fields",
                        "title": "Require Custom Fields Example",
                        "message": "Which raffle would they like to enter today's purchase?",
                        "entity": "sale",
                        "entity_id": "cc0e2f8f-3c14-ac66-11ea-9e2e4fefb804",
                        "required_custom_fields": [
                            {
                            "name": "raffle-entry",
                            "values": [
                                {
                                "value": "free-album",
                                "title": "A free album - who doesn't love free music"
                                },
                                {
                                "value": "exclusive-merch",
                                "title": "Exclusive merch - a one of a kind item"
                                },
                                {
                                "value": "opt-out",
                                "title": "neither - opt out of the raffle"
                                }
                            ]
                            }
                        ]
                        }
                    ]
                    }
            return response_payload
    else:
        return {"error": "Invalid request"}, 400
    
@app.route('/lsx-1605/require_custom_fields_customer', methods=['POST'])
def require_custom_fields_customer():
    if receive_and_verify(request):
        data = request.json
        if "sale" in data and "custom_fields" in data["sale"] and len(data["sale"]['custom_fields']) > 0: # if custom fields are already set, don't require them again
            return {"actions": []}
        else:
            response_payload = {
                    "actions": [
                        {
                        "type": "require_custom_fields",
                        "title": "Require Custom Fields Example",
                        "message": "What is your favorite kind of pet?",
                        "entity": "customer",
                        "entity_id": "cc0e2f8f-3c14-ac66-11ea-9e2e4fefb804",
                        "required_custom_fields": [
                            {
                            "name": "favorite-pet",
                            "values": [
                                {
                                "value": "cat",
                                "title": "Cat - cats are the best"
                                },
                                {
                                "value": "cats",
                                "title": "Cats - why stop at just one"
                                },
                                {
                                "value": "none",
                                "title": "None - I don't like pets"
                                }
                            ]
                            }
                        ]
                        }
                    ]
                    }
            return response_payload
    else:
        return {"error": "Invalid request"}, 400

@app.route('/lsx-1605/set_custom_field_sale', methods=['POST'])
def set_custom_field_sale():
    if receive_and_verify(request):
        response_payload = {
                "actions": [
                    {
                    "type": "set_custom_field",
                    "entity": "sale",
                    "custom_field_name": "customer_changed_at",
                    "custom_field_value": time.time()
                    }
                ]
                }
        return response_payload
    else:
        return {"error": "Invalid request"}, 400
    
@app.route('/lsx-1605/set_custom_field_customer', methods=['POST'])
def set_custom_field_customer():
    if receive_and_verify(request):
        response_payload = {
                "actions": [
                    {
                    "type": "set_custom_field",
                    "entity": "customer",
                    "custom_field_name": "customer_changed_at",
                    "custom_field_value": time.time()
                    }
                ]
                }
        return response_payload
    else:
        return {"error": "Invalid request"}, 400

@app.route('/lsx-1605/add_line_item', methods=['POST'])
def add_line_item():
    if receive_and_verify(request):
        response_payload = {
                "actions": [
                    {
                    "type": "add_line_item",
                    "product_id": EXAMPLE_PRODUCT,
                    "quantity": 1,
                    "note": "here's an egg for this trying time",
                    }
                ]
                }
        return response_payload
    else:
        return {"error": "Invalid request"}, 400

@app.route('/lsx-1605/remove_line_item', methods=['POST'])
def remove_line_item():
    if receive_and_verify(request):
        response_payload = {
                "actions": [
                    {
                    "type": "remove_line_item",
                    "line_item_id": "b76dc8f4-4e5d-40be-8a37-f09507bfb66d"
                    }
                ]
                }
        return response_payload
    else:
        return {"error": "Invalid request"}, 400

@app.route('/lsx-1605/suggest_products', methods=['POST'])
def suggest_products():
    if receive_and_verify(request):
        data = request.json
        if "sale" in data and "line_items" in data["sale"]:
                line_items = data["sale"]["line_items"]
                for item in line_items:
                    if "product_id" in item and item["product_id"] == EXAMPLE_PRODUCT:
                        return {"actions": []}
        response_payload = {
                "actions": [
                    {
                    "type": "suggest_products",
                    "title": "Suggested Products",
                    "message": "Can I offer you an egg in this trying time?",
                    "suggested_products": [
                        {
                        "product_id": EXAMPLE_PRODUCT,
                        }
                    ]
                    }   
                ]
                }
        return response_payload
    else:  
        return {"error": "Invalid request"}, 400


########  EXTRA LSX ROUTES  ########

if __name__ == "__main__":
    app.run()

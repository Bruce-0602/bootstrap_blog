from flask import Flask, render_template, request
from flask_mail import Mail, Message
import requests
# import smtplib
import os

app = Flask(__name__)
# mail = Mail(app)
blog_api = "https://api.npoint.io/4780dc7ea12348799258"
posts = requests.get(blog_api).json()
OWN_EMAIL = os.environ['OWN_EMAIL']
OWN_PASSWORD = os.environ['OWN_PASSWORD']
APP_PASSWORD = os.environ['APP_PASSWORD']

# set up gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = OWN_EMAIL
app.config['MAIL_PASSWORD'] = APP_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == post_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    msg = Message('New Form', sender=OWN_EMAIL, recipients=[OWN_EMAIL])
    msg.body = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    mail.send(msg)
    # older version
    # with smtplib.SMTP("smtp.gmail.com") as connection:
    #     connection.starttls()
    #     connection.login(OWN_EMAIL, OWN_PASSWORD)
    #     connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)

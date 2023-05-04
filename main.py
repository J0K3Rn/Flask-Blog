from flask import Flask, render_template, request
from post import Post
import datetime
import requests
import smtplib

app = Flask(__name__)

CURRENT_YEAR = datetime.datetime.now().year

blog_url = "https://api.npoint.io/02b7b5790b38f8ac45b8"
response = requests.get(blog_url)
all_posts = response.json()
post_objects = []
for post in all_posts:
    post_obj = Post(post["id"], post["author"], post["date"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route('/home')
def home():
    return render_template("index.html", posts=all_posts, year=CURRENT_YEAR)


@app.route('/')
def root():
    return home()


@app.route('/about')
def about():
    return render_template("about.html", year=CURRENT_YEAR)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", msg_sent=False, year=CURRENT_YEAR)
    elif request.method == "POST":
        data = request.form
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        server_email = ""
        to_email = ""
        password = ""
        header = f"New message from {name} from Blogerrio!"
        body = message
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=server_email, password=password)
            connection.sendmail(
                from_addr=server_email,
                to_addrs=to_email,
                msg=f"{header}\n\nEmail: {email}\nPhone Number: {phone}\n{body}"
            )
        return render_template("contact.html", msg_sent=True, year=CURRENT_YEAR)


@app.route('/post/<int:index>')
def get_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post, year=CURRENT_YEAR)


if __name__ == "__main__":
    app.run(debug=True)

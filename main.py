from flask import Flask, render_template
from post import Post
import datetime
import requests

app = Flask(__name__)

CURRENT_YEAR = datetime.datetime.now().year

blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(blog_url)
all_posts = response.json()
post_objects = []
for post in all_posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts, year=CURRENT_YEAR)


@app.route('/post/<int:index>')
def get_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post, year=CURRENT_YEAR)


if __name__ == "__main__":
    app.run(debug=True)

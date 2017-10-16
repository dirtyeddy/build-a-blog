from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return render_template('blog.html')

@app.route('/blog', methods=['GET'])
def blog():

    blog_id = request.args.get('id')
    blogs = Blogs.query.all()

    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog.html', blog=blog)

    else:
        return render_template("blog.html", blogs=blogs, title="Main Page")

@app.route('/new-blog', methods=['GET', 'POST'])
def new_post():
    return render_template('new-blog.html', title="Build a Blog")

@app.route('/new-post', methods=['POST', 'GET'])
def new_blog():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        print(title,' ', body)

        if not title or not body:
            flash("Please fill out all the fields.")
            return redirect('/new-post')

        else:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id'== str(id))

    return render_template('new-post.html')

if __name__ == '__main__':
    app.run()

#Post Handler ---
#is this a new post?
#Assign form fields to variables
#verify form fields to variables, if they are empty show errors(flash)
#create blog post object
#feed in variables to object 
#put object into db 
#commit 
#redirect to main blog page 
#else: render the new blog template


from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'secret_key'



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    id = request.args.get("id")
    if not id:
        posts = Blog.query.all()
        return render_template('blog.html', title="Build a Blog", posts=posts)
    post = Blog.query.filter_by(id=id).first()
    return render_template('blog-entry.html', title="Blog", post=post)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ''
        body_error = ''
    
        if not title or not body:
            if not title:
                flash("Please fill out all the fields.")
            if not body:
                flash("Please fill out all the fields.")
            return render_template('/newpost.html', title=title, title_error=title_error, body=body, body_error=body_error)

        else:
            new_blog_entry = Blog(title, body)
            db.session.add(new_blog_entry)
            db.session.commit()
        
        return redirect('/blog?id='+ str(new_blog_entry.id))
   

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


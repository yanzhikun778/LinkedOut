from flask import (Flask, render_template, request, session, redirect, send_file)
from controller import constants
from controller.database import Database
from models import Student,Commuter,Blog,Comment,User


app = Flask(__name__)
app.secret_key = "NotSecure"

@app.before_first_request
def initialize_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('demo.html')

@app.route('/test')
def test():
    message=''
    return render_template('auth/login.html', prompt_error=message)

@app.route('/static/test')
def static_test():
    return send_file('static/detail01.html')

#----------------------------------  User  ----------------------------------
@app.route('/student/auth/login', methods=['POST'])
def login_student():
    email = request.form['email']
    password = request.form['password']
    students=Database.find_one(collection=constants.STUDENT_COLLECTION, query={"email": email})
    if students is not None:
        if students["password"]==password:
            session.__setitem__('email', email)
            session.__setitem__('name', students["name"])
        else:
            session.__setitem__('email', None)
            session.__setitem__('name', None)
            return render_template('auth/login.html', prompt_error="密码错误")
    else:
        session.__setitem__('email', None)
        session.__setitem__('name', None)
        return render_template('auth/login.html', prompt_error="该用户不存在  ")
    return redirect('/', code=302)


@app.route('/student/auth/register', methods=['POST'])
def register_student():
    # prompt_alert = ""
    email = request.form.get('email')
    password = request.form.get('password')
    sex = request.form.get('sex')
    name = request.form.get('name')

    school = request.form.get('school')
    if not len(email) or not len(password) or not len(name):
        prompt_alert = "Please enter valid email and password values."
    elif Student.register(email, password, sex, name, [], school):
        return redirect('/', code=302)
    else:
        prompt_alert = 'User with the same email already exists!'
    return render_template('auth/register.html', prompt_message=prompt_alert)

@app.route('/commuter/auth/login', methods=['POST'])
def login_commuter():
    email = request.form['email']
    password = request.form['password']
    commuters=Database.find_one(collection=constants.COMMUTER_COLLECTION, query={"email": email})
    if commuters is not None:
        if commuters["password"]==password:
            session.__setitem__('email', email)
            session.__setitem__('name', commuters["name"])
        else:
            session.__setitem__('email', None)
            session.__setitem__('name', None)
            return render_template('auth/login.html', prompt_error="密码错误")
    else:
        session.__setitem__('email', None)
        session.__setitem__('name', None)
        return render_template('auth/login.html', prompt_error="该用户不存在  ")
    return redirect('/', code=302)


@app.route('/commuter/auth/register', methods=['POST'])
def register_commuter():
    # prompt_alert = ""
    email = request.form.get('email')
    password = request.form.get('password')
    sex = request.form.get('sex')
    name = request.form.get('name')
    company = request.form.get('company')
    if not len(email) or not len(password) or not len(name):
        prompt_alert = "Please enter valid email and password values."
    elif Commuter.register(email, password, sex, name, company):
        return redirect('/', code=302)
    else:
        prompt_alert = 'User with the same email already exists!'
    return render_template('auth/register.html', prompt_message=prompt_alert)

@app.route('/logout')
def logout():
    User.logout()
    return redirect('/')


#----------------------------------  Blog  ----------------------------------
@app.route('/blogs/search/<title>')
def get_blog_search(title):
    blogs=Blog.get_by_title_re(title)
    user=User.get_by_email()
    return render_template('/templates/community/search.html', blogs=blogs, user=user)


@app.route('/blog/delete/<blog_id>')
def delete_blog(blog_id):

    blog = Blog.get_by_id(blog_id)
    user = User.get_by_id(blog.author_id)
    Blog.delete_all_from_mongo_viaQuery({'blog_id':blog_id})
    Blog.delete_from_mongo_viaId(blog_id)
    blogs = user.get_blogs()
    return render_template('blogs/doctorblogs.html', blogs=blogs, email=session.get('email'), c=0)


@app.route('/blog/<blog_id>')
def get_blog(blog_id=None):
    blog = Blog.get_by_id(blog_id)
    comments = blog.get_comments()
    user = User.get_by_id(blog.author_id)
    return render_template('blogs/single-blog.html', blog=blog, comments=comments, user=user)


@app.route('/myblogs')
def get_blogs(user_id=None):
    user = None
    if user_id:
        user = User.get_by_id(user_id)
    elif not user_id:
        user = User.get_by_email(session.get('email'))
    if not user:
        return render_template('error_404.html')

    user_blogs = user.get_blogs()
    return render_template('blogs/doctorblogs.html', blogs=user_blogs, email=session.get('email'), c=0)


@app.route('/pubblog')
def pubblog():
    return render_template('blogs/pubblog.html')


@app.route('/blog/create', methods=['POST'])
def create_new_blog():

    student = Student.get_by_email(session.get('email'))
    commuter = Commuter.get_by_email(session.get('email'))
    if student is None:
        user = commuter
    else:
        user = student

    title = request.form.get('blogTitle')
    description = request.form.get('blogDescription')
    blog = Blog(title=title, description=description, author=user.name, author_id=user._id)
    blog.save_to_mongo()
    return redirect('/myblogs')

# -----------------------------  Comments  ----------------------------------
@app.route('/comment/create/<blog_id>',methods=['POST'])
def create_new_comment(blog_id):
    student = Student.get_by_email(session.get('email'))
    commuter = Commuter.get_by_email(session.get('email'))
    if student is None:
        user = commuter
    else:
        user = student

    title = request.form.get('blogTitle')
    description = request.form.get('blogDescription')
    comment = Comment(blog_id, description, user.name)
    comment.save_to_mongo()
    return redirect('/')







if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

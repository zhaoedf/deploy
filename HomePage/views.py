import datetime

from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user

from HomePage import app,db
from HomePage.models import Message,Blog,User







@app.route('/',methods=['GET','POST'])
def hello_world():

    if request.method == 'POST':
        print(1)
        name = request.form.get('name')
        mail = request.form.get('mail')
        content = request.form.get('content')
        print(content)

        mes = Message(name=name,mail=mail,body=content)
        db.session.add(mes)
        db.session.commit()

        return redirect(url_for('prompt'))

    blogs = Blog.query.order_by(Blog.timestamp.desc()).limit(2)

    return render_template('index.html',blogs=blogs)



@app.route('/prompt')
def prompt():
    return render_template('prompt.html')


@app.route('/blogDisplay',methods=['GET','POST'])
def blogAllDisplay():
    page = request.args.get('page',1,type=int)

    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page,3,error_out=False)

    blogs = pagination.items

    return render_template('blogDisplay.html',blogs=blogs,paginate=pagination)


@app.route('/blogContent/<int:blog_id>')
def blogContentShow(blog_id):
   blog = Blog.query.get_or_404(blog_id)



   return render_template('blogContent.html',blog=blog,check=len(blog.text)<400)




@app.route('/login', methods=['GET','POST'])
def login():
    print(1)
    if request.method == 'POST':
        print(2)
        username = request.form['username']
        password = request.form['password']
        print(username,password)

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        print(username == user.username,user.validate_password(password))
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            print(1)
            return redirect(url_for('admin.index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))


    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'log out successfully!'
    return redirect(url_for('hello_world'))



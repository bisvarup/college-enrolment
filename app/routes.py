from flask import render_template, request, flash, redirect, url_for
from app import app
from app import db


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/register' , methods=['GET','POST'])
def register():
    print("request.method %s" % request.method)
    if request.method == 'GET':
        return render_template('register.html')
    user = db.User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = db.User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

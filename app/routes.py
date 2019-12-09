from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.database import Student, Teacher


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/registerStudent' , methods=['GET','POST'])
def registerStudent():
    print("request.method %s" % request.method)
    if request.method == 'GET':
        return render_template('registerStudent.html')
    student = Student(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(student)
    db.session.commit()
    flash('Student successfully registered')
    return redirect(url_for('loginStudent'))

@app.route('/loginStudent',methods=['GET','POST'])
def loginStudent():
    if request.method == 'GET':
        return render_template('loginStudent.html')
    username = request.form['username']
    password = request.form['password']
    registered_student = Student.query.filter_by(username=username,password=password).first()
    if registered_student is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('loginStudent'))
    login_user(registered_student)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/registerTeacher' , methods=['GET','POST'])
def registerTeacher():
    print("request.method %s" % request.method)
    if request.method == 'GET':
        return render_template('registerTeacher.html')
    teacher = Teacher(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(teacher)
    db.session.commit()
    flash('Teacher successfully registered')
    return redirect(url_for('loginTeacher'))

@app.route('/loginTeacher',methods=['GET','POST'])
def loginTeacher():
    if request.method == 'GET':
        return render_template('loginTeacher.html')
    username = request.form['username']
    password = request.form['password']
    registered_teacher = Teacher.query.filter_by(username=username,password=password).first()
    if registered_teacher is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('loginTeacher'))
    login_user(registered_teacher)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

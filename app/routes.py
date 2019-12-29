from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.database import Student, Teacher, Registration
from werkzeug.utils import secure_filename
from sqlalchemy import update
from fpdf import FPDF
import sys
import os

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/static/<path>')
def serve_static(path):
    return send_from_directory(app.static_folder,path)


@app.route('/register-student' , methods=['GET','POST'])
def registerStudent():
    print("request.method %s" % request.method)
    if request.method == 'GET':
        return render_template('register-student.html')
    student = Student(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(student)
    db.session.commit()
    flash('Student successfully registered')
    return redirect(url_for('loginStudent'))

@app.route('/login-student',methods=['GET','POST'])
def loginStudent():
    if request.method == 'GET':
        return render_template('login-student.html')
    username = request.form['username']
    password = request.form['password']
    registered_student = Student.query.filter_by(username=username,password=password).first()
    if registered_student is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('loginStudent'))
    login_user(registered_student)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('studentDashboard'))

@app.route('/student-dashboard')
def studentDashboard():
    if current_user.get_id() is None:
        return redirect('/')
    return render_template('student-dashboard.html')


@app.route('/register-teacher' , methods=['GET','POST'])
def registerTeacher():
    print("request.method %s" % request.method)
    if request.method == 'GET':
        return render_template('register-teacher.html')
    teacher = Teacher(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(teacher)
    db.session.commit()
    flash('Teacher successfully registered')
    return redirect(url_for('loginTeacher'))

@app.route('/login-teacher',methods=['GET','POST'])
def loginTeacher():
    if request.method == 'GET':
        return render_template('login-teacher.html')
    username = request.form['username']
    password = request.form['password']
    registered_teacher = Teacher.query.filter_by(username=username,password=password).first()
    if registered_teacher is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('loginTeacher'))
    login_user(registered_teacher)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('teacherDashboard'))

@app.route('/teacher-dashboard')
def teacherDashboard():
    if current_user.get_id() is None:
        return redirect('/')
    return render_template('teacher-dashboard.html')

@app.route('/teacher-dashboard/add-course')
def addCourse():
    if current_user.get_id() is None:
        return redirect('/')
    return render_template('add-course.html')

@app.route('/teacher-dashboard/list-courses')
def listCourses():
    if current_user.get_id() is None:
        return redirect('/')
    return render_template('list-courses.html')

@app.route('/teacher-dashboard/approved-students', methods=['GET', 'POST'])
def approvedStudents():
    if request.method == 'GET':
        if current_user.get_id() is None:
            return redirect('/')
        approved_students = Registration.query.filter_by(approved=True).all()
        return render_template('approved-students.html', data=approved_students)
    else:
        return "OK"

@app.route('/teacher-dashboard/applied-students', methods=['GET', 'POST'])
def appliedStudents():
    if request.method == 'GET':
        if current_user.get_id() is None:
            return redirect('/')
        applied_students = Registration.query.filter_by(approved=False).all()
        return render_template('applied-students.html', data=applied_students)
    else:
        id = request.form['id']
        registration = Registration.query.get(int(id))
        print(registration)
        registration.approved = True
        db.session.commit()
        return redirect('/teacher-dashboard/applied-students')

@app.route('/logout')
def logout():
    if current_user.get_id() is None:
        return redirect('/')
    logout_user()
    return redirect(url_for('index'))

@app.route('/student-enrolment', methods=['GET', 'POST'])
def studentEnrolment():
    if request.method == 'GET':
        return render_template('student-enrolment.html')
    else:
        pass

@app.route('/submit-course', methods=['POST'])
def submitCourse():
    guardian_name = request.form['guardian_name']
    class_10_percentage = request.form['class_10_percentage']

    class_10_certificate = request.files['class_10_certificate']
    class_10_certificate_filename = secure_filename(class_10_certificate.filename)

    class_12_percentage=request.form['class_12_percentage']

    class_12_certificate = request.files['class_12_certificate']
    class_12_certificate_filename = secure_filename(class_12_certificate.filename)

    prevRegistration = Registration.query.filter_by(student_id=current_user.id).first()
    if prevRegistration is not None:
        flash('You already applied for course')
        return redirect(url_for('studentDashboard'))

    registration = Registration(
        current_user.id,
        current_user.username,
        guardian_name,
        class_10_percentage,
        class_12_percentage,
        class_10_certificate_filename,
        class_12_certificate_filename)


    class_10_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], class_10_certificate_filename))
    class_12_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], class_12_certificate_filename))


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Username "+current_user.username, ln=1, align="L")
    pdf.cell(200, 15, txt="Guardian Name " + guardian_name, ln=1, align="L")
    pdf.cell(200, 20, txt="Class 10 percentage " + class_10_percentage, ln=1, align="L")
    pdf.cell(200, 25, txt="Class 12 percentage" + class_12_percentage, ln=1, align="L")

    pdf.output(os.path.join(app.static_folder,"Student_" + current_user.username +"_.pdf"))

    db.session.add(registration)
    db.session.commit()

    flash('You registered for course')
    return redirect(url_for('studentDashboard'))

@app.errorhandler(404)
def handle404(e):
    return render_template("404.html")

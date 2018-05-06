import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash


DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = "key"
USERNAME = "admin"
PASSWORD = "p@ssw0rd"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'The system does not recognize that username.'
            return render_template('login.html', error=error)
        elif request.form['password'] != PASSWORD:
            error = 'The password is incorrect; please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')


def newgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    elif request.method == 'POST':
        g.db.execute('insert into grades (student_id, quiz_id, score) values (?, ?, ?)',
                     [request.form['student_id'], request.form['quiz_id'], request.form['score']])
        g.db.commit()
    return redirect(url_for('dashboard'))
    if username == 'admin' and password == 'password':
        session = request.form['username']
        return render_template('dashboard.html', username=username, password=password)
    else:
        print 'Invalid login'
        return render_template('index.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    conns = g.db.execute('select studentid, firstname, lastname from students')
    students = [dict(studentid=row[0], firstname=row[1], lastname=row[2])
                for row in conns.fetchall()]
    connq = g.db.execute('select quizid, subject, questions, date from quizzes')
    quizzes = [dict(quizid=row[0], subject=row[1], questions=row[2], date=row[3])
               for row in connq.fetchall()]
    conng = g.db.execute('select student_id, quiz_id, score from grades')
    grades = [dict(student_id=row[0], quiz_id=row[1], score=row[2])
              for row in conng.fetchall()]
    return render_template("dashboard.html", students=students, quizzes=quizzes, grades=grades)


@app.route('/student/add', methods=['GET', 'POST'])
def newstudent():
    if request.method == 'POST':
        g.db.execute('insert into students (firstname, lastname) values (?, ?)',
                     [request.form['firstname'], request.form['lastname']])
        g.db.commit()
        return redirect(url_for('dashboard'))
    return render_template("addstudent.html")


@app.route('/quiz/add', methods=['GET', 'POST'])
def newquiz():
    if request.method == 'POST':
        g.db.execute('insert into quizzes (subject, questions, date) values (?, ?, ?)',
                     [request.form['subject'], request.form['questions'], request.form['date']])
        g.db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addquiz.html')


@app.route('/results/add', methods=['GET', 'POST'])
def newgrade():
    if request.method == 'POST':
        g.db.execute('insert into grades (student_id, quiz_id, score) values (?, ?, ?)',
                     [request.form['student_id'], request.form['quiz_id'], request.form['score']])
        g.db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addgrade.html')


if __name__ == "__main__":
    app.run()
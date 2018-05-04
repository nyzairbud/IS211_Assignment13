import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('hw13.db')

    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS students;")
    c.execute("CREATE TABLE students (studentid INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "firstname text not null,lastname text not null);")
    c.execute("INSERT INTO students VALUES(1, 'John', 'Smith');")

    c.execute("DROP TABLE IF EXISTS quizzes;")
    c.execute("CREATE TABLE quizzes(quizid INTEGER PRIMARY KEY,"
                   "subject text not null,questions INTEGER not null,date text not null)")
    c.execute("INSERT INTO quizzes VALUES(1, 'Python Basics', 5, 'Feb. 5, 2015');")

    c.execute("DROP TABLE IF EXISTS grades;")
    c.execute("CREATE TABLE grades(student_id INTEGER not null,"
                   "quiz_id INTEGER not null,score INTEGER not null)")
    c.execute("INSERT INTO grades VALUES(1, 1, 85);")

    con.commit()

except lite.Error, e:

    if con:
        con.rollback()

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()
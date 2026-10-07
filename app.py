from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Flask application
app = Flask(__name__)
# ==================== OTHER USER DATABASE ====================

def init_database():
    conn = sqlite3.connect('campus.db')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            dob TEXT,
            address TEXT,
            user_type TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


init_database()
# ==================== OTHER USER REGISTRATION ====================

@app.route('/register')
def register():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Other User Registration</title>

    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
            margin: 0;
        }

        header {
            background: #059669;
            color: white;
            padding: 25px;
            text-align: center;
        }

        .container {
            max-width: 650px;
            margin: 30px auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,.12);
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0 15px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 7px;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #059669;
            color: white;
            border: none;
            border-radius: 7px;
            font-size: 16px;
        }

        label {
            font-weight: bold;
        }

        .login {
            display: block;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>

<body>

<header>
    <h1>👤 Other User Registration</h1>
    <p>AI Campus Operating System</p>
</header>

<div class="container">

<div class="card">

    <h2>Create Account</h2>

    <form method="POST" action="/register">

        <label>Full Name</label>
        <input type="text" name="name" required>

        <label>Email</label>
        <input type="email" name="email" required>

        <label>Mobile Number</label>
        <input type="tel" name="mobile" required>

        <label>Date of Birth</label>
        <input type="date" name="dob">

        <label>Address</label>
        <textarea name="address" rows="3"></textarea>

        <label>User Type</label>
        <select name="user_type">
            <option value="Other User">Other User</option>
            <option value="Parent">Parent</option>
            <option value="Visitor">Visitor</option>
            <option value="Staff">Staff</option>
        </select>

        <label>Username</label>
        <input type="text" name="username" required>

        <label>Password</label>
        <input type="password" name="password" required>

        <button type="submit">
            Create Account
        </button>

    </form>

    <a class="login" href="/">
        Already registered? Go to Login
    </a>

</div>

</div>

</body>
</html>
'''
@app.route('/register', methods=['POST'])
def save_registration():

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    mobile = request.form.get('mobile', '').strip()
    dob = request.form.get('dob', '').strip()
    address = request.form.get('address', '').strip()
    user_type = request.form.get('user_type', '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '')

    if not name or not email or not mobile or not username or not password:
        return '''
        <h2>Please fill all required fields.</h2>
        <a href="/register">Back to Registration</a>
        '''

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect('campus.db')

        conn.execute('''
            INSERT INTO users
            (name, email, mobile, dob, address, user_type, username, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            email,
            mobile,
            dob,
            address,
            user_type,
            username,
            hashed_password
        ))

        conn.commit()
        conn.close()

        return '''
        <h2>Registration Successful! ✅</h2>
        <p>Your account has been created.</p>
        <a href="/">Go to Login</a>
        '''

    except sqlite3.IntegrityError:

        return '''
        <h2>Username already exists ❌</h2>
        <p>Please choose another username.</p>
        <a href="/register">Try Again</a>
        '''

# ==================================================
# LOGIN
# ==================================================

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def check_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "student" and password == "1234":
        return render_template("student.html")
    # OTHER USER LOGIN
    conn = sqlite3.connect('campus.db')

    user = conn.execute(
        'SELECT name, password FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):
        return f'''
        <html>
        <head>
            <title>Other User Dashboard</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #f4f6f9;
                    margin: 0;
                }}

                header {{
                    background: #059669;
                    color: white;
                    padding: 25px;
                }}

                .box {{
                    max-width: 800px;
                    margin: 40px auto;
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                }}
            </style>
        </head>

        <body>

        <header>
            <h1>👤 Other User Dashboard</h1>
            <p>Welcome, {user[0]}</p>
        </header>

        <div class="box">

    <h2>Welcome {user[0]} 👋</h2>

    <p>You are successfully logged in to AI Campus Operating System.</p>

    <hr>

    <h3>👤 Your Account</h3>

    <p><b>Name:</b> {user[0]}</p>

    <br>

    <a class="button" href="/user-profile">
        👤 My Profile
    </a>

    <a class="button" href="/">
        🚪 Logout
    </a>

</div>

        </body>
        </html>
        '''

    elif username == "teacher" and password == "1234":
        return render_template("teacher.html")
    else:
        return """
        <h2>Invalid Username or Password</h2>
        <a href="/">Back to Login</a>
        """

    from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Flask application
app = Flask(__name__)
# ==================== OTHER USER DATABASE ====================

def init_database():
    conn = sqlite3.connect('campus.db')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            dob TEXT,
            address TEXT,
            user_type TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


init_database()
# ==================== OTHER USER REGISTRATION ====================

@app.route('/register')
def register():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Other User Registration</title>

    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
            margin: 0;
        }

        header {
            background: #059669;
            color: white;
            padding: 25px;
            text-align: center;
        }

        .container {
            max-width: 650px;
            margin: 30px auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,.12);
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0 15px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 7px;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #059669;
            color: white;
            border: none;
            border-radius: 7px;
            font-size: 16px;
        }

        label {
            font-weight: bold;
        }

        .login {
            display: block;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>

<body>

<header>
    <h1>👤 Other User Registration</h1>
    <p>AI Campus Operating System</p>
</header>

<div class="container">

<div class="card">

    <h2>Create Account</h2>

    <form method="POST" action="/register">

        <label>Full Name</label>
        <input type="text" name="name" required>

        <label>Email</label>
        <input type="email" name="email" required>

        <label>Mobile Number</label>
        <input type="tel" name="mobile" required>

        <label>Date of Birth</label>
        <input type="date" name="dob">

        <label>Address</label>
        <textarea name="address" rows="3"></textarea>

        <label>User Type</label>
        <select name="user_type">
            <option value="Other User">Other User</option>
            <option value="Parent">Parent</option>
            <option value="Visitor">Visitor</option>
            <option value="Staff">Staff</option>
        </select>

        <label>Username</label>
        <input type="text" name="username" required>

        <label>Password</label>
        <input type="password" name="password" required>

        <button type="submit">
            Create Account
        </button>

    </form>

    <a class="login" href="/">
        Already registered? Go to Login
    </a>

</div>

</div>

</body>
</html>
'''
@app.route('/register', methods=['POST'])
def save_registration():

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    mobile = request.form.get('mobile', '').strip()
    dob = request.form.get('dob', '').strip()
    address = request.form.get('address', '').strip()
    user_type = request.form.get('user_type', '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '')

    if not name or not email or not mobile or not username or not password:
        return '''
        <h2>Please fill all required fields.</h2>
        <a href="/register">Back to Registration</a>
        '''

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect('campus.db')

        conn.execute('''
            INSERT INTO users
            (name, email, mobile, dob, address, user_type, username, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            email,
            mobile,
            dob,
            address,
            user_type,
            username,
            hashed_password
        ))

        conn.commit()
        conn.close()

        return '''
        <h2>Registration Successful! ✅</h2>
        <p>Your account has been created.</p>
        <a href="/">Go to Login</a>
        '''

    except sqlite3.IntegrityError:

        return '''
        <h2>Username already exists ❌</h2>
        <p>Please choose another username.</p>
        <a href="/register">Try Again</a>
        '''

# ==================================================
# LOGIN
# ==================================================

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def check_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "student" and password == "1234":
        return render_template("student.html")
    # OTHER USER LOGIN
    conn = sqlite3.connect('campus.db')

    user = conn.execute(
        'SELECT name, password FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):
        return f'''
        <html>
        <head>
            <title>Other User Dashboard</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #f4f6f9;
                    margin: 0;
                }}

                header {{
                    background: #059669;
                    color: white;
                    padding: 25px;
                }}

                .box {{
                    max-width: 800px;
                    margin: 40px auto;
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                }}
            </style>
        </head>

        <body>

        <header>
            <h1>👤 Other User Dashboard</h1>
            <p>Welcome, {user[0]}</p>
        </header>

        <div class="box">

    <h2>Welcome {user[0]} 👋</h2>

    <p>You are successfully logged in to AI Campus Operating System.</p>

    <hr>

    <h3>👤 Your Account</h3>

    <p><b>Name:</b> {user[0]}</p>

    <br>

    <a class="button" href="/user-profile">
        👤 My Profile
    </a>

    <a class="button" href="/">
        🚪 Logout
    </a>

</div>

        </body>
        </html>
        '''

    elif username == "teacher" and password == "1234":
        return render_template("teacher.html")

    elif username == "admin" and password == "1234":
        return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>

        <style>
            body {
                font-family: Arial;
                background: #f4f6f9;
                margin: 0;
                text-align: center;
            }

            header {
                background: #111827;
                color: white;
                padding: 25px;
            }

            .box {
                background: white;
                max-width: 600px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.12);
            }

            .button {
                display: inline-block;
                padding: 14px 22px;
                margin: 10px;
                background: #059669;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
            }

            .logout {
                background: #555;
            }
        </style>
    </head>

    <body>

        <header>
            <h1>👨‍💼 Admin Dashboard</h1>
            <p>AI Campus Operating System</p>
        </header>

        <div class="box">

            <h2>Welcome Admin 👋</h2>

            <p>Manage campus system information.</p>

            <a class="button" href="/registered-users">
                👥 Registered Users
            </a>

            <br>

            <a class="button logout" href="/">
                🚪 Logout
            </a>

        </div>

    </body>
    </html>
    """
    else:
        return """
        <h2>Invalid Username or Password</h2>
        <a href="/">Back to Login</a>
        """
# ==================================================
# STUDENT
# ==================================================

@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/attendance")
def attendance():
    return render_template("attendance.html")


@app.route("/marks")
def marks():
    return render_template("marks.html")


@app.route("/assignments")
def assignments():
    return render_template("assignments.html")


@app.route("/teacher-notes")
def teacher_notes():
    return render_template("upload_notes.html")


@app.route("/notices")
def notices():
    return render_template("notices.html")


@app.route("/timetable")
def timetable():
    return render_template("timetable.html")


# # ==================== AI ASSISTANT ====================

# ==================== AI ASSISTANT ====================

@app.route('/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():

    answer = ""

    if request.method == 'POST':

        question = request.form.get('question', '').lower().strip()

        if 'attendance' in question:
            answer = "Your current attendance is 85%."

        elif 'marks' in question or 'mark' in question:
            answer = "Your current average marks are 81%. Your DSA score is 78/100."

        elif 'assignment' in question:
            answer = "You currently have 4 pending assignments."

        elif 'timetable' in question or 'time table' in question:
            answer = "Please open the Timetable section to check your weekly classes."

        elif 'notice' in question:
            answer = "Please open the Notices section to check the latest college notices."

        elif 'performance' in question or 'report' in question:
            answer = "Open Performance Report to view your attendance, marks and assignments."

        elif 'profile' in question:
            answer = "Open Student Profile to view your academic information."

        elif 'python' in question:
            answer = "Python is a programming language used in software development, AI, automation and data analysis."

        elif 'java' in question:
            answer = "Java is an object-oriented programming language commonly used for software and application development."

        elif 'dsa' in question or 'data structure' in question:
            answer = "DSA stands for Data Structures and Algorithms. It is used to store, manage and process data efficiently."

        elif 'oops' in question or 'oop' in question:
            answer = "OOPS means Object-Oriented Programming. Its main concepts are Class, Object, Inheritance, Polymorphism, Encapsulation and Abstraction."

        elif 'dbms' in question:
            answer = "DBMS stands for Database Management System. It is used to store, manage and retrieve data."

        elif 'project' in question:
            answer = "Your project is an AI Campus Operating System developed using Flask and Python."

        elif 'hello' in question or 'hi' in question:
            answer = "Hello! 👋 I am your AI Campus Assistant. How can I help you?"

        else:
            answer = "I can help you with Attendance, Marks, Assignments, Timetable, Notices, Performance, Profile, Python, Java, DSA, OOPS and DBMS."

    return render_template('ai_assistant.html', 
    answer=answer)

# ==================================================
# TEACHER DASHBOARD
# ==================================================

@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


# ==================================================
# TEACHER - STUDENTS
# ==================================================

@app.route("/teacher-students")
def teacher_students():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Student Information</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #16a34a;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}
.button {
        display: inline-block;
        padding: 12px 20px;
        background: #059669;
        color: white;
        text-decoration: none;
        border-radius: 7px;
        margin: 5px;
    }
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #16a34a;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Information</h1>
<p>AI Campus Operating System</p>

</header>

<div class="container">

<div class="box">

<h2>Student List</h2>

<table>

<tr>
<th>Name</th>
<th>Roll Number</th>
<th>Course</th>
<th>Attendance</th>
<th>Marks</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>B.Tech CSE</td>
<td>85%</td>
<td>78%</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>B.Tech CSE</td>
<td>90%</td>
<td>82%</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>B.Tech CSE</td>
<td>88%</td>
<td>91%</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>B.Tech CSE</td>
<td>76%</td>
<td>74%</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>B.Tech CSE</td>
<td>82%</td>
<td>79%</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - ATTENDANCE
# ==================================================

@app.route("/teacher-attendance")
def teacher_attendance():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Attendance</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #2563eb;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #2563eb;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.present {
    color: green;
    font-weight: bold;
}

.absent {
    color: red;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Attendance</h1>
<p>Teacher Attendance Management</p>

</header>

<div class="container">

<div class="box">

<h2>Today's Attendance</h2>

<table>

<tr>
<th>Student Name</th>
<th>Roll Number</th>
<th>Status</th>
<th>Attendance</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td class="present">Present</td>
<td>85%</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td class="present">Present</td>
<td>90%</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td class="present">Present</td>
<td>88%</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td class="absent">Absent</td>
<td>76%</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td class="present">Present</td>
<td>82%</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - MARKS
# ==================================================

@app.route("/teacher-marks")
def teacher_marks():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Marks</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #7c3aed;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #7c3aed;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.marks {
    font-weight: bold;
}

.pass {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Marks</h1>
<p>Teacher Marks Management</p>

</header>

<div class="container">

<div class="box">

<h2>Academic Performance</h2>

<table>

<tr>
<th>Name</th>
<th>Roll Number</th>
<th>Subject</th>
<th>Marks</th>
<th>Status</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>Data Structures</td>
<td class="marks">78 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>Data Structures</td>
<td class="marks">82 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>Data Structures</td>
<td class="marks">91 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>Data Structures</td>
<td class="marks">74 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>Data Structures</td>
<td class="marks">79 / 100</td>
<td class="pass">Passed</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - ASSIGNMENTS
# ==================================================

@app.route("/teacher-assignments")
def teacher_assignments():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Assignments</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #ea580c;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #ea580c;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.pending {
    color: red;
    font-weight: bold;
}

.submitted {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Assignments</h1>
<p>Teacher Assignment Management</p>

</header>

<div class="container">

<div class="box">

<h2>Assignment List</h2>

<table>

<tr>
<th>Assignment</th>
<th>Subject</th>
<th>Due Date</th>
<th>Status</th>
</tr>

<tr>
<td>DSA Assignment 1</td>
<td>Data Structures</td>
<td>05 October 2026</td>
<td class="pending">Pending</td>
</tr>

<tr>
<td>Python Assignment</td>
<td>Python</td>
<td>08 October 2026</td>
<td class="submitted">Submitted</td>
</tr>

<tr>
<td>DBMS Assignment</td>
<td>Database</td>
<td>10 October 2026</td>
<td class="pending">Pending</td>
</tr>

<tr>
<td>OOPS Assignment</td>
<td>OOPS</td>
<td>12 October 2026</td>
<td class="submitted">Submitted</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - REPORTS
# ==================================================

@app.route("/teacher-reports")
def teacher_reports():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Student Reports</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f9;
}

header {
    background: #0891b2;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #0891b2;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.good {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Reports</h1>
<p>Student Performance Report</p>

</header>

<div class="container">

<div class="box">

<h2>📊 Academic Performance</h2>

<table>

<tr>
<th>Student Name</th>
<th>Roll Number</th>
<th>Attendance</th>
<th>Marks</th>
<th>Performance</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>85%</td>
<td>78%</td>
<td class="good">Good</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>90%</td>
<td>82%</td>
<td class="good">Very Good</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>88%</td>
<td>91%</td>
<td class="good">Excellent</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>76%</td>
<td>74%</td>
<td class="good">Good</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>82%</td>
<td>79%</td>
<td class="good">Good</td>
</tr>

</table>

<a href="/teacher" class="back">
← Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""

# ==================================================
# TEACHER - PROFILE
# ==================================================
@app.route("/teacher-profile")
def teacher_profile():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Profile - AI Campus</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f9;
}

header {
    background: #4f46e5;
    color: white;
    padding: 25px 30px;
}

header h1 {
    margin: 0;
}

header p {
    margin-top: 8px;
}

.container {
    max-width: 900px;
    margin: 30px auto;
    padding: 20px;
}

.profile-card {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.12);
}

.profile-top {
    text-align: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 25px;
}

.profile-icon {
    font-size: 70px;
}

.profile-top h2 {
    margin: 10px 0 5px;
}

.profile-top p {
    color: #666;
}

.info {
    margin-top: 25px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 16px;
    border-bottom: 1px solid #eee;
}

.label {
    font-weight: bold;
    color: #444;
}

.value {
    color: #222;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 22px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 7px;
}

.back:hover {
    background: #333;
}

</style>

</head>

<body>

<header>

<h1>👨‍🏫 Teacher Profile</h1>

<p>AI Campus Operating System</p>

</header>


<div class="container">

<div class="profile-card">


<div class="profile-top">

<div class="profile-icon">
👨‍🏫
</div>

<h2>Dr. Rajesh Kumar</h2>

<p>Computer Science Faculty</p>

</div>


<div class="info">


<div class="info-row">

<span class="label">
👤 Name
</span>

<span class="value">
Dr. Rajesh Kumar
</span>

</div>


<div class="info-row">

<span class="label">
🏫 Department
</span>

<span class="value">
Computer Science & Engineering
</span>

</div>


<div class="info-row">

<span class="label">
💼 Role
</span>

<span class="value">
Assistant Professor
</span>

</div>


<div class="info-row">

<span class="label">
📧 Email
</span>

<span class="value">
rajesh.kumar@aicampus.edu
</span>

</div>


<div class="info-row">

<span class="label">
📱 Contact
</span>

<span class="value">
+91 98765 43210
</span>

</div>


<div class="info-row">

<span class="label">
📚 Subjects
</span>

<span class="value">
Python, DSA, DBMS, OOPS
</span>

</div>


<div class="info-row">

<span class="label">
🎓 Qualification
</span>

<span class="value">
M.Tech in Computer Science
</span>

</div>


<div class="info-row">

<span class="label">
📅 Experience
</span>

<span class="value">
5 Years
</span>

</div>


</div>


<a href="/teacher" class="back">
← Back to Teacher Dashboard
</a>


</div>

</div>

</body>

</html>
"""



# ==================================================
# RUN APPLICATION
# ==================================================
# ==================================================
# STUDENT PERFORMANCE REPORT
# ==================================================

@app.route('/performance-report')
def performance_report():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Performance Report</title>

    <style>
        body {
            font-family: Arial;
            margin: 0;
            background: #f4f6f9;
            color: #222;
        }

        header {
            background: #0f766e;
            color: white;
            padding: 25px 30px;
        }

        .container {
            max-width: 1100px;
            margin: 30px auto;
            padding: 20px;
        }

        .cards {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .card {
            background: white;
            padding: 22px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 180px;
        }

        .num {
            font-size: 30px;
            font-weight: bold;
            color: #0f766e;
        }

        .box {
            background: white;
            padding: 22px;
            margin-top: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #0f766e;
            color: white;
            padding: 12px;
            text-align: left;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        .good {
            color: green;
            font-weight: bold;
        }

        .pending {
            color: red;
            font-weight: bold;
        }

        .submitted {
            color: green;
            font-weight: bold;
        }

        .bar {
            height: 18px;
            background: #ddd;
            border-radius: 10px;
        }

        .fill {
            height: 18px;
            width: 85%;
            background: #0f766e;
            border-radius: 10px;
        }

        .back {
            display: inline-block;
            margin-top: 25px;
            padding: 12px 20px;
            background: #555;
            color: white;
            text-decoration: none;
            border-radius: 7px;
        }
    </style>
</head>

<body>

<header>
    <h1>📊 Student Performance Report</h1>
    <p>AI Campus Operating System</p>
</header>

<div class="container">

    <!-- SUMMARY CARDS -->
    <div class="cards">

        <div class="card">
            <h3>Attendance</h3>
            <div class="num">85%</div>
            <p>85 Present / 100 Classes</p>
        </div>

        <div class="card">
            <h3>Average Marks</h3>
            <div class="num">81%</div>
            <p>Overall Academic Score</p>
        </div>

        <div class="card">
            <h3>Assignments</h3>
            <div class="num">4</div>
            <p>Total Assignments</p>
        </div>

        <div class="card">
            <h3>Overall Performance</h3>
            <div class="num">Good</div>
            <p>Academic Performance</p>
        </div>

    </div>


    <!-- ATTENDANCE -->
    <div class="box">

        <h2>📅 Attendance Performance</h2>

        <p>
            Current Attendance:
            <b>85%</b>
        </p>

        <div class="bar">
            <div class="fill"></div>
        </div>

        <p>85 Present / 15 Absent / 100 Total Classes</p>

    </div>


    <!-- SUBJECT PERFORMANCE -->
    <div class="box">

        <h2>📚 Subject Performance</h2>

        <table>

            <tr>
                <th>Subject</th>
                <th>Marks</th>
                <th>Grade</th>
                <th>Performance</th>
            </tr>

            <tr>
                <td>Data Structures</td>
                <td>78 / 100</td>
                <td>B+</td>
                <td class="good">Good</td>
            </tr>

            <tr>
                <td>Python Programming</td>
                <td>82 / 100</td>
                <td>A</td>
                <td class="good">Very Good</td>
            </tr>

            <tr>
                <td>DBMS</td>
                <td>75 / 100</td>
                <td>B+</td>
                <td class="good">Good</td>
            </tr>

            <tr>
                <td>OOPS</td>
                <td>80 / 100</td>
                <td>A</td>
                <td class="good">Very Good</td>
            </tr>

        </table>

    </div>


    <!-- ASSIGNMENT PERFORMANCE -->
    <div class="box">

        <h2>📝 Assignment Performance</h2>

        <table>

            <tr>
                <th>Assignment</th>
                <th>Subject</th>
                <th>Due Date</th>
                <th>Status</th>
            </tr>

            <tr>
                <td>DSA Assignment 1</td>
                <td>Data Structures</td>
                <td>05 October 2026</td>
                <td class="pending">Pending</td>
            </tr>

            <tr>
                <td>Python Assignment</td>
                <td>Python</td>
                <td>08 October 2026</td>
                <td class="submitted">Submitted</td>
            </tr>

            <tr>
                <td>DBMS Assignment</td>
                <td>DBMS</td>
                <td>10 October 2026</td>
                <td class="pending">Pending</td>
            </tr>

            <tr>
                <td>OOPS Assignment</td>
                <td>OOPS</td>
                <td>12 October 2026</td>
                <td class="submitted">Submitted</td>
            </tr>

        </table>

    </div>


    <!-- BACK BUTTON -->
    <a class="back" href="/student">
        ← Back to Student Dashboard
    </a>

</div>

</body>
</html>
'''
# ==================== REGISTERED USERS ====================

@app.route('/registered-users')
def registered_users():

    conn = sqlite3.connect('campus.db')

    users = conn.execute('''
        SELECT id, name, email, mobile, dob, address, user_type, username
        FROM users
        ORDER BY id DESC
    ''').fetchall()

    conn.close()

    html = '''
    <!DOCTYPE html>
    <html>

    <head>
        <title>Registered Users</title>

        <style>
            body {
                font-family: Arial;
                background: #f4f6f9;
                margin: 0;
            }

            h1 {
                background: #111827;
                color: white;
                padding: 25px;
                margin: 0;
            }

            .container {
                padding: 25px;
                overflow-x: auto;
            }

            table {
                width: 100%;
                background: white;
                border-collapse: collapse;
            }

            th {
                background: #111827;
                color: white;
                padding: 12px;
            }

            td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
        </style>

    </head>

    <body>

    <h1>👥 Registered Other Users</h1>

    <div class="container">

    <table>

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Email</th>
        <th>Mobile</th>
        <th>DOB</th>
        <th>Address</th>
        <th>User Type</th>
        <th>Username</th>
    </tr>
    '''

    for user in users:

        html += f'''
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
            <td>{user[3]}</td>
            <td>{user[4]}</td>
            <td>{user[5]}</td>
            <td>{user[6]}</td>
            <td>{user[7]}</td>
        </tr>
        '''

    html += '''
    </table>

    </div>

    </body>
    </html>
    '''

    return html

@app.route('/user-profile')
def user_profile():
    return """
    <h1>👤 My Profile</h1>
    <p>Your account is successfully active.</p>
    <br>
    <a href="/">🚪 Logout</a>
    """
if __name__ == '__main__':
    app.run(debug=True)

# ==================================================
# STUDENT
# ==================================================

@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/attendance")
def attendance():
    return render_template("attendance.html")


@app.route("/marks")
def marks():
    return render_template("marks.html")


@app.route("/assignments")
def assignments():
    return render_template("assignments.html")


@app.route("/notices")
def notices():
    return render_template("notices.html")


@app.route("/timetable")
def timetable():
    return render_template("timetable.html")


# # ==================== AI ASSISTANT ====================

# ==================== AI ASSISTANT ====================

@app.route('/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():

    answer = ""

    if request.method == 'POST':

        question = request.form.get('question', '').lower().strip()

        if 'attendance' in question:
            answer = "Your current attendance is 85%."

        elif 'marks' in question or 'mark' in question:
            answer = "Your current average marks are 81%. Your DSA score is 78/100."

        elif 'assignment' in question:
            answer = "You currently have 4 pending assignments."

        elif 'timetable' in question or 'time table' in question:
            answer = "Please open the Timetable section to check your weekly classes."

        elif 'notice' in question:
            answer = "Please open the Notices section to check the latest college notices."

        elif 'performance' in question or 'report' in question:
            answer = "Open Performance Report to view your attendance, marks and assignments."

        elif 'profile' in question:
            answer = "Open Student Profile to view your academic information."

        elif 'python' in question:
            answer = "Python is a programming language used in software development, AI, automation and data analysis."

        elif 'java' in question:
            answer = "Java is an object-oriented programming language commonly used for software and application development."

        elif 'dsa' in question or 'data structure' in question:
            answer = "DSA stands for Data Structures and Algorithms. It is used to store, manage and process data efficiently."

        elif 'oops' in question or 'oop' in question:
            answer = "OOPS means Object-Oriented Programming. Its main concepts are Class, Object, Inheritance, Polymorphism, Encapsulation and Abstraction."

        elif 'dbms' in question:
            answer = "DBMS stands for Database Management System. It is used to store, manage and retrieve data."

        elif 'project' in question:
            answer = "Your project is an AI Campus Operating System developed using Flask and Python."

        elif 'hello' in question or 'hi' in question:
            answer = "Hello! 👋 I am your AI Campus Assistant. How can I help you?"

        else:
            answer = "I can help you with Attendance, Marks, Assignments, Timetable, Notices, Performance, Profile, Python, Java, DSA, OOPS and DBMS."

    return render_template('ai_assistant.html', 
    answer=answer)

# ==================================================
# TEACHER DASHBOARD
# ==================================================

@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


# ==================================================
# TEACHER - STUDENTS
# ==================================================

@app.route("/teacher-students")
def teacher_students():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Student Information</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #16a34a;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}
.button {
        display: inline-block;
        padding: 12px 20px;
        background: #059669;
        color: white;
        text-decoration: none;
        border-radius: 7px;
        margin: 5px;
    }
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #16a34a;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Information</h1>
<p>AI Campus Operating System</p>

</header>

<div class="container">

<div class="box">

<h2>Student List</h2>

<table>

<tr>
<th>Name</th>
<th>Roll Number</th>
<th>Course</th>
<th>Attendance</th>
<th>Marks</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>B.Tech CSE</td>
<td>85%</td>
<td>78%</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>B.Tech CSE</td>
<td>90%</td>
<td>82%</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>B.Tech CSE</td>
<td>88%</td>
<td>91%</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>B.Tech CSE</td>
<td>76%</td>
<td>74%</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>B.Tech CSE</td>
<td>82%</td>
<td>79%</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - ATTENDANCE
# ==================================================

@app.route("/teacher-attendance")
def teacher_attendance():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Attendance</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #2563eb;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #2563eb;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.present {
    color: green;
    font-weight: bold;
}

.absent {
    color: red;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Attendance</h1>
<p>Teacher Attendance Management</p>

</header>

<div class="container">

<div class="box">

<h2>Today's Attendance</h2>

<table>

<tr>
<th>Student Name</th>
<th>Roll Number</th>
<th>Status</th>
<th>Attendance</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td class="present">Present</td>
<td>85%</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td class="present">Present</td>
<td>90%</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td class="present">Present</td>
<td>88%</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td class="absent">Absent</td>
<td>76%</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td class="present">Present</td>
<td>82%</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - MARKS
# ==================================================

@app.route("/teacher-marks")
def teacher_marks():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Marks</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #7c3aed;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #7c3aed;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.marks {
    font-weight: bold;
}

.pass {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Marks</h1>
<p>Teacher Marks Management</p>

</header>

<div class="container">

<div class="box">

<h2>Academic Performance</h2>

<table>

<tr>
<th>Name</th>
<th>Roll Number</th>
<th>Subject</th>
<th>Marks</th>
<th>Status</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>Data Structures</td>
<td class="marks">78 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>Data Structures</td>
<td class="marks">82 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>Data Structures</td>
<td class="marks">91 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>Data Structures</td>
<td class="marks">74 / 100</td>
<td class="pass">Passed</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>Data Structures</td>
<td class="marks">79 / 100</td>
<td class="pass">Passed</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - ASSIGNMENTS
# ==================================================

@app.route("/teacher-assignments")
def teacher_assignments():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Assignments</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #f4f6f9;
}

header {
    background: #ea580c;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #ea580c;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.pending {
    color: red;
    font-weight: bold;
}

.submitted {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Assignments</h1>
<p>Teacher Assignment Management</p>

</header>

<div class="container">

<div class="box">

<h2>Assignment List</h2>

<table>

<tr>
<th>Assignment</th>
<th>Subject</th>
<th>Due Date</th>
<th>Status</th>
</tr>

<tr>
<td>DSA Assignment 1</td>
<td>Data Structures</td>
<td>05 October 2026</td>
<td class="pending">Pending</td>
</tr>

<tr>
<td>Python Assignment</td>
<td>Python</td>
<td>08 October 2026</td>
<td class="submitted">Submitted</td>
</tr>

<tr>
<td>DBMS Assignment</td>
<td>Database</td>
<td>10 October 2026</td>
<td class="pending">Pending</td>
</tr>

<tr>
<td>OOPS Assignment</td>
<td>OOPS</td>
<td>12 October 2026</td>
<td class="submitted">Submitted</td>
</tr>

</table>

<a href="/teacher" class="back">
Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""


# ==================================================
# TEACHER - REPORTS
# ==================================================

@app.route("/teacher-reports")
def teacher_reports():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Student Reports</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f9;
}

header {
    background: #0891b2;
    color: white;
    padding: 25px;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #0891b2;
    color: white;
    padding: 14px;
}

td {
    padding: 14px;
    border-bottom: 1px solid #ddd;
}

.good {
    color: green;
    font-weight: bold;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 20px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

</style>

</head>

<body>

<header>

<h1>Student Reports</h1>
<p>Student Performance Report</p>

</header>

<div class="container">

<div class="box">

<h2>📊 Academic Performance</h2>

<table>

<tr>
<th>Student Name</th>
<th>Roll Number</th>
<th>Attendance</th>
<th>Marks</th>
<th>Performance</th>
</tr>

<tr>
<td>Rahul Kumar</td>
<td>101</td>
<td>85%</td>
<td>78%</td>
<td class="good">Good</td>
</tr>

<tr>
<td>Amit Sharma</td>
<td>102</td>
<td>90%</td>
<td>82%</td>
<td class="good">Very Good</td>
</tr>

<tr>
<td>Priya Singh</td>
<td>103</td>
<td>88%</td>
<td>91%</td>
<td class="good">Excellent</td>
</tr>

<tr>
<td>Neha Verma</td>
<td>104</td>
<td>76%</td>
<td>74%</td>
<td class="good">Good</td>
</tr>

<tr>
<td>Rohit Kumar</td>
<td>105</td>
<td>82%</td>
<td>79%</td>
<td class="good">Good</td>
</tr>

</table>

<a href="/teacher" class="back">
← Back to Teacher Dashboard
</a>

</div>

</div>

</body>

</html>
"""

# ==================================================
# TEACHER - PROFILE
# ==================================================
@app.route("/teacher-profile")
def teacher_profile():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Teacher Profile - AI Campus</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f9;
}

header {
    background: #4f46e5;
    color: white;
    padding: 25px 30px;
}

header h1 {
    margin: 0;
}

header p {
    margin-top: 8px;
}

.container {
    max-width: 900px;
    margin: 30px auto;
    padding: 20px;
}

.profile-card {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.12);
}

.profile-top {
    text-align: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 25px;
}

.profile-icon {
    font-size: 70px;
}

.profile-top h2 {
    margin: 10px 0 5px;
}

.profile-top p {
    color: #666;
}

.info {
    margin-top: 25px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 16px;
    border-bottom: 1px solid #eee;
}

.label {
    font-weight: bold;
    color: #444;
}

.value {
    color: #222;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 12px 22px;
    background: #555;
    color: white;
    text-decoration: none;
    border-radius: 7px;
}

.back:hover {
    background: #333;
}

</style>

</head>

<body>

<header>

<h1>👨‍🏫 Teacher Profile</h1>

<p>AI Campus Operating System</p>

</header>


<div class="container">

<div class="profile-card">


<div class="profile-top">

<div class="profile-icon">
👨‍🏫
</div>

<h2>Dr. Rajesh Kumar</h2>

<p>Computer Science Faculty</p>

</div>


<div class="info">


<div class="info-row">

<span class="label">
👤 Name
</span>

<span class="value">
Dr. Rajesh Kumar
</span>

</div>


<div class="info-row">

<span class="label">
🏫 Department
</span>

<span class="value">
Computer Science & Engineering
</span>

</div>


<div class="info-row">

<span class="label">
💼 Role
</span>

<span class="value">
Assistant Professor
</span>

</div>


<div class="info-row">

<span class="label">
📧 Email
</span>

<span class="value">
rajesh.kumar@aicampus.edu
</span>

</div>


<div class="info-row">

<span class="label">
📱 Contact
</span>

<span class="value">
+91 98765 43210
</span>

</div>


<div class="info-row">

<span class="label">
📚 Subjects
</span>

<span class="value">
Python, DSA, DBMS, OOPS
</span>

</div>


<div class="info-row">

<span class="label">
🎓 Qualification
</span>

<span class="value">
M.Tech in Computer Science
</span>

</div>


<div class="info-row">

<span class="label">
📅 Experience
</span>

<span class="value">
5 Years
</span>

</div>


</div>


<a href="/teacher" class="back">
← Back to Teacher Dashboard
</a>


</div>

</div>

</body>

</html>
"""



# ==================================================
# RUN APPLICATION
# ==================================================
# ==================================================
# STUDENT PERFORMANCE REPORT
# ==================================================

@app.route('/performance-report')
def performance_report():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Performance Report</title>

    <style>
        body {
            font-family: Arial;
            margin: 0;
            background: #f4f6f9;
            color: #222;
        }

        header {
            background: #0f766e;
            color: white;
            padding: 25px 30px;
        }

        .container {
            max-width: 1100px;
            margin: 30px auto;
            padding: 20px;
        }

        .cards {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .card {
            background: white;
            padding: 22px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 180px;
        }

        .num {
            font-size: 30px;
            font-weight: bold;
            color: #0f766e;
        }

        .box {
            background: white;
            padding: 22px;
            margin-top: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #0f766e;
            color: white;
            padding: 12px;
            text-align: left;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        .good {
            color: green;
            font-weight: bold;
        }

        .pending {
            color: red;
            font-weight: bold;
        }

        .submitted {
            color: green;
            font-weight: bold;
        }

        .bar {
            height: 18px;
            background: #ddd;
            border-radius: 10px;
        }

        .fill {
            height: 18px;
            width: 85%;
            background: #0f766e;
            border-radius: 10px;
        }

        .back {
            display: inline-block;
            margin-top: 25px;
            padding: 12px 20px;
            background: #555;
            color: white;
            text-decoration: none;
            border-radius: 7px;
        }
    </style>
</head>

<body>

<header>
    <h1>📊 Student Performance Report</h1>
    <p>AI Campus Operating System</p>
</header>

<div class="container">

    <!-- SUMMARY CARDS -->
    <div class="cards">

        <div class="card">
            <h3>Attendance</h3>
            <div class="num">85%</div>
            <p>85 Present / 100 Classes</p>
        </div>

        <div class="card">
            <h3>Average Marks</h3>
            <div class="num">81%</div>
            <p>Overall Academic Score</p>
        </div>

        <div class="card">
            <h3>Assignments</h3>
            <div class="num">4</div>
            <p>Total Assignments</p>
        </div>

        <div class="card">
            <h3>Overall Performance</h3>
            <div class="num">Good</div>
            <p>Academic Performance</p>
        </div>

    </div>


    <!-- ATTENDANCE -->
    <div class="box">

        <h2>📅 Attendance Performance</h2>

        <p>
            Current Attendance:
            <b>85%</b>
        </p>

        <div class="bar">
            <div class="fill"></div>
        </div>

        <p>85 Present / 15 Absent / 100 Total Classes</p>

    </div>


    <!-- SUBJECT PERFORMANCE -->
    <div class="box">

        <h2>📚 Subject Performance</h2>

        <table>

            <tr>
                <th>Subject</th>
                <th>Marks</th>
                <th>Grade</th>
                <th>Performance</th>
            </tr>

            <tr>
                <td>Data Structures</td>
                <td>78 / 100</td>
                <td>B+</td>
                <td class="good">Good</td>
            </tr>

            <tr>
                <td>Python Programming</td>
                <td>82 / 100</td>
                <td>A</td>
                <td class="good">Very Good</td>
            </tr>

            <tr>
                <td>DBMS</td>
                <td>75 / 100</td>
                <td>B+</td>
                <td class="good">Good</td>
            </tr>

            <tr>
                <td>OOPS</td>
                <td>80 / 100</td>
                <td>A</td>
                <td class="good">Very Good</td>
            </tr>

        </table>

    </div>


    <!-- ASSIGNMENT PERFORMANCE -->
    <div class="box">

        <h2>📝 Assignment Performance</h2>

        <table>

            <tr>
                <th>Assignment</th>
                <th>Subject</th>
                <th>Due Date</th>
                <th>Status</th>
            </tr>

            <tr>
                <td>DSA Assignment 1</td>
                <td>Data Structures</td>
                <td>05 October 2026</td>
                <td class="pending">Pending</td>
            </tr>

            <tr>
                <td>Python Assignment</td>
                <td>Python</td>
                <td>08 October 2026</td>
                <td class="submitted">Submitted</td>
            </tr>

            <tr>
                <td>DBMS Assignment</td>
                <td>DBMS</td>
                <td>10 October 2026</td>
                <td class="pending">Pending</td>
            </tr>

            <tr>
                <td>OOPS Assignment</td>
                <td>OOPS</td>
                <td>12 October 2026</td>
                <td class="submitted">Submitted</td>
            </tr>

        </table>

    </div>


    <!-- BACK BUTTON -->
    <a class="back" href="/student">
        ← Back to Student Dashboard
    </a>

</div>

</body>
</html>
'''
# ==================== REGISTERED USERS ====================

@app.route('/registered-users')
def registered_users():

    conn = sqlite3.connect('campus.db')

    users = conn.execute('''
        SELECT id, name, email, mobile, dob, address, user_type, username
        FROM users
        ORDER BY id DESC
    ''').fetchall()

    conn.close()

    html = '''
    <!DOCTYPE html>
    <html>

    <head>
        <title>Registered Users</title>

        <style>
            body {
                font-family: Arial;
                background: #f4f6f9;
                margin: 0;
            }

            h1 {
                background: #111827;
                color: white;
                padding: 25px;
                margin: 0;
            }

            .container {
                padding: 25px;
                overflow-x: auto;
            }

            table {
                width: 100%;
                background: white;
                border-collapse: collapse;
            }

            th {
                background: #111827;
                color: white;
                padding: 12px;
            }

            td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
        </style>

    </head>

    <body>

    <h1>👥 Registered Other Users</h1>

    <div class="container">

    <table>

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Email</th>
        <th>Mobile</th>
        <th>DOB</th>
        <th>Address</th>
        <th>User Type</th>
        <th>Username</th>
    </tr>
    '''

    for user in users:

        html += f'''
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
            <td>{user[3]}</td>
            <td>{user[4]}</td>
            <td>{user[5]}</td>
            <td>{user[6]}</td>
            <td>{user[7]}</td>
        </tr>
        '''

    html += '''
    </table>

    </div>

    </body>
    </html>
    '''

    return html
if __name__ == '__main__':
    app.run(debug=True)
   
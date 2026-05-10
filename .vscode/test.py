from flask import Flask, render_template, request, redirect, url_for, session
import logging
import datetime
import sqlite3
import os

# ----------------------------------------------------
# APPLICATION INITIALIZATION
# ----------------------------------------------------

app = Flask(__name__)

app.secret_key = "research_project_secret_key"

# ----------------------------------------------------
# LOGGING CONFIGURATION
# ----------------------------------------------------

logging.basicConfig(

    filename="application.log",

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

# ----------------------------------------------------
# DATABASE CREATION
# ----------------------------------------------------

DATABASE_NAME = "users.db"

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            password TEXT NOT NULL,

            email TEXT,

            mobile TEXT

        )

    """)

    connection.commit()

    connection.close()

create_database()

# ----------------------------------------------------
# DEFAULT USERS
# ----------------------------------------------------

default_users = {

    "admin": "1234",

    "tester": "test123",

    "developer": "dev123"

}

# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------

@app.route("/")
def home():

    logging.info("Home page visited")

    return render_template("index.html")

# ----------------------------------------------------
# LOGIN FUNCTION
# ----------------------------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")

    password = request.form.get("password")

    email = request.form.get("email")

    mobile = request.form.get("mobile")

    logging.info(f"Login attempt by user: {username}")

    # --------------------------------------------
    # EMPTY FIELD VALIDATION
    # --------------------------------------------

    if username == "" or password == "":

        logging.warning("Empty fields detected")

        return """

        <h2>Validation Error</h2>

        <p>Username and Password cannot be empty.</p>

        <a href="/">Go Back</a>

        """

    # --------------------------------------------
    # SQL INJECTION BASIC CHECK
    # --------------------------------------------

    dangerous_keywords = [

        "' OR '1'='1",

        "DROP TABLE",

        "--",

        ";"

    ]

    for word in dangerous_keywords:

        if word in username or word in password:

            logging.warning("Possible SQL Injection Attempt")

            return """

            <h2>Security Alert</h2>

            <p>Malicious Input Detected.</p>

            <a href="/">Go Back</a>

            """

    # --------------------------------------------
    # USER AUTHENTICATION
    # --------------------------------------------

    if username in default_users and default_users[username] == password:

        session["username"] = username

        logging.info("Login Successful")

        # ----------------------------------------
        # STORE LOGIN RECORD IN DATABASE
        # ----------------------------------------

        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        cursor.execute("""

            INSERT INTO users(

                username,
                password,
                email,
                mobile

            )

            VALUES(?,?,?,?)

        """, (

            username,
            password,
            email,
            mobile

        ))

        connection.commit()

        connection.close()

        return f"""

        <html>

        <head>

            <title>Dashboard</title>

            <style>

                body{{
                    font-family: Arial;
                    background:#f4f7fc;
                    padding:40px;
                }}

                .dashboard{{
                    background:white;
                    padding:30px;
                    border-radius:10px;
                    box-shadow:0px 0px 10px rgba(0,0,0,0.2);
                }}

            </style>

        </head>

        <body>

            <div class="dashboard">

                <h1>Login Successful</h1>

                <h2>Welcome {username}</h2>

                <p>
                    This dashboard demonstrates
                    successful authentication testing.
                </p>

                <h3>User Information</h3>

                <ul>

                    <li>Email: {email}</li>

                    <li>Mobile: {mobile}</li>

                    <li>Login Time:
                        {datetime.datetime.now()}
                    </li>

                </ul>

                <a href="/logout">
                    Logout
                </a>

            </div>

        </body>

        </html>

        """

    else:

        logging.error("Invalid Credentials")

        return """

        <html>

        <body>

            <h1>Invalid Credentials</h1>

            <p>
                Username or password is incorrect.
            </p>

            <a href="/">
                Try Again
            </a>

        </body>

        </html>

        """

# ----------------------------------------------------
# LOGOUT FUNCTION
# ----------------------------------------------------

@app.route("/logout")
def logout():

    user = session.get("username")

    logging.info(f"{user} logged out")

    session.pop("username", None)

    return redirect(url_for("home"))

# ----------------------------------------------------
# API STATUS CHECK
# ----------------------------------------------------

@app.route("/api/status")
def api_status():

    logging.info("API status checked")

    return {

        "status": "running",

        "project": "Software Quality Assurance Research",

        "testing": [

            "Manual Testing",

            "Automation Testing",

            "Performance Testing",

            "Security Testing"

        ]

    }

# ----------------------------------------------------
# VIEW ALL USERS
# ----------------------------------------------------

@app.route("/users")
def view_users():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    connection.close()

    output = """

    <html>

    <head>

        <title>Users</title>

    </head>

    <body>

        <h1>Registered Login Records</h1>

        <table border="1" cellpadding="10">

            <tr>

                <th>ID</th>

                <th>Username</th>

                <th>Password</th>

                <th>Email</th>

                <th>Mobile</th>

            </tr>

    """

    for user in users:

        output += f"""

        <tr>

            <td>{user[0]}</td>

            <td>{user[1]}</td>

            <td>{user[2]}</td>

            <td>{user[3]}</td>

            <td>{user[4]}</td>

        </tr>

        """

    output += """

        </table>

    </body>

    </html>

    """

    return output

# ----------------------------------------------------
# ERROR HANDLING
# ----------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    logging.error("404 Error Occurred")

    return """

    <h1>404 Error</h1>

    <p>Page Not Found</p>

    """, 404

# ----------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------

if __name__ == "__main__":

    logging.info("Application Started")

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
import Database

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-in-production"

db = Database.DataBase()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access that page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    
    if not db.loginUserExists():
        flash("No accounts found. Please create the first account.", "info")
        return redirect(url_for("register"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user_info = db.validateLogin(username, password)
        if user_info:
            session["user_id"] = user_info["id"]
            session["username"] = user_info["username"]
            session["role"] = user_info["role"]
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    first_run = not db.loginUserExists()

    error = None
    success = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")
        role     = request.form.get("role", "user")

        if not username or not password:
            error = "Username and password are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            effective_role = "admin" if first_run else role
            ok = db.createLoginUser(username, password, effective_role)
            if ok:
                if first_run:
                    flash("Account created. Please log in.", "success")
                    return redirect(url_for("login"))
                success = f"Account '{username}' ({effective_role}) created successfully."
            else:
                error = f"Username '{username}' is already taken."

    return render_template("register.html", error=error, success=success,
                           first_run=first_run)

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    db_success = None

    if request.method == "POST":
        user_input_1 = request.form.get("user_input_1")
        user_input_2 = request.form.get("user_input_2")
        db_success = db.addAction(user_input_1, user_input_2)

    return render_template("index.html", db_success=db_success)

@app.route("/data", methods=["GET"])
@login_required
def data():
    data_list = db.fetch()
    return render_template("data.html", data_list=data_list)

@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    user_success = None
    form_type = None

    if request.method == "POST":
        if "add_user_btn" in request.form:
            form_type = "add_user"
            user_success = db.addUser(
                request.form.get("stud_id_create_input"),
                request.form.get("name_create_input"),
            )
        elif "upload_file_btn" in request.form:
            form_type = "upload_file"
            file = request.files["file_input"]
            user_success = db.replaceUsers(file)

    return render_template("user.html", user_success=user_success, form_type=form_type)


if __name__ == "__main__":
    app.run(debug=True)

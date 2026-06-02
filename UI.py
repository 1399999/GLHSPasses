from flask import Flask, render_template, request
import Database

start_btn = None
end_btn = None
t0 = None
t1 = None
combust_nun = None

app = Flask(__name__, template_folder='Templates')
db = Database.DataBase()

@app.route("/", methods=["GET", "POST"])
def home():

    global submit_btn
    global t0
    global t1
    global combust_nun

    submit_btn = None
    user_input_1 = None
    user_input_2 = None
    db_success = None
    
    if request.method == "POST":
        submit_btn = request.form.get("submit_btn")
        user_input_1 = request.form.get("user_input_1")
        user_input_2 = request.form.get("user_input_2")

        db_success = db.addAction(user_input_1, user_input_2)

    output = render_template("index.html", db_success=db_success)

    if submit_btn != None:
        submit_btn = None

    return output

@app.route("/data", methods=["GET"])
def data():
    data_list = db.fetch()

    return render_template("data.html", data_list=data_list)

@app.route("/user", methods=["GET", "POST"])
def user():
    global add_user_btn
    global upload_file_btn
    global name_create_input
    global stud_id_create_input

    add_user_btn = None
    upload_file_btn = None
    name_create_input = None
    stud_id_create_input = None
    user_success = None
    form_type = None

    if request.method == "POST":
        add_user_btn = request.form.get("add_user_btn")
        name_create_input = request.form.get("name_create_input")
        stud_id_create_input = request.form.get("stud_id_create_input")
        upload_file_btn = request.form.get("upload_file_btn")

        if request.method == 'POST':
            if 'add_user_btn' in request.form:
                form_type = 'add_user'
                user_success = db.addUser(stud_id_create_input, name_create_input)
                
            elif 'upload_file_btn' in request.form:
                form_type = 'upload_file'
                file = request.files['file_input']
                user_success = db.replaceUsers(file)

    output = render_template("user.html", user_success=user_success, form_type=form_type)

    if add_user_btn != None:
        add_user_btn = None

    if upload_file_btn != None:
        upload_file_btn = None

    return output


if __name__ == "__main__":
    app.run(debug=True)

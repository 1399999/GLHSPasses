from flask import Flask, render_template, request
import time

start_btn = None
end_btn = None
t0 = None
t1 = None
combust_nun = None

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    global start_btn
    global end_btn
    global t0
    global t1
    global combust_nun

    user_input_1 = None
    user_input_2 = None
    
    if request.method == "POST":
        start_btn = request.form.get("start")
        end_btn = request.form.get("end")
        if start_btn != None:
            t0 = time.time()
        if end_btn != None:
            t1 = time.time()
            combust_nun = t1 - t0
        user_input_1 = request.form.get("user_input_1")
        user_input_2 = request.form.get("user_input_2")
    
    output = render_template("index.html", stud_id=user_input_1, place=user_input_2, start_btn=start_btn, end_btn=end_btn, time_a=combust_nun)

    if start_btn != None and end_btn != None:
        start_btn = None
        end_btn = None

    return output

if __name__ == "__main__":
    app.run(debug=True)

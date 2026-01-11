from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "microservices-devops-secret"

# Demo users
USERS = ["admin1", "admin2", "admin3"]


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and password == username:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- AGE CALCULATOR ----------------
@app.route("/age", methods=["GET", "POST"])
def age():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            payload = {
                "day": request.form.get("day"),
                "month": request.form.get("month"),
                "year": request.form.get("year")
            }

            response = requests.post(
                "http://age-service:5000/age",
                json=payload,
                timeout=3
            )

            if response.status_code == 200:
                return render_template("age_result.html", result=response.json())
            else:
                return render_template("age.html", error="Age service error")

        except Exception:
            return render_template("age.html", error="Age service unavailable")

    return render_template("age.html")


# ---------------- SIMPLE CALCULATOR ----------------
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            payload = {
                "a": request.form.get("a"),
                "b": request.form.get("b"),
                "operation": request.form.get("operation")
            }

            response = requests.post(
                "http://calc-service:5000/api/calc",
                json=payload,
                timeout=3
            )

            if response.status_code == 200:
                return render_template(
                    "calc_result.html",
                    result=response.json().get("result")
                )
            else:
                return render_template("calc.html", error="Calculation failed")

        except Exception:
            return render_template("calc.html", error="Calculator service unavailable")

    return render_template("calc.html")


# ---------------- INTEREST CALCULATOR ----------------
@app.route("/interest", methods=["GET", "POST"])
def interest():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            payload = {
                "principal": request.form.get("principal"),
                "rate": request.form.get("rate"),
                "time": request.form.get("time")
            }

            response = requests.post(
                "http://interest-service:5000/api/interest",
                json=payload,
                timeout=3
            )

            if response.status_code == 200:
                return render_template(
                    "interest_result.html",
                    result=response.json()
                )
            else:
                return render_template("interest.html", error="Interest calculation failed")

        except Exception:
            return render_template("interest.html", error="Interest service unavailable")

    return render_template("interest.html")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

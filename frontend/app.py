from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "microservices-devops-secret"

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
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])


# ---------------- AGE CALCULATOR ----------------
@app.route("/age", methods=["GET", "POST"])
def age():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    error = None

    if request.method == "POST":
        try:
            response = requests.post(
                "http://age-service:5000/calculate",
                json={
                    "day": request.form.get("day"),
                    "month": request.form.get("month"),
                    "year": request.form.get("year")
                },
                timeout=3
            )

            if response.status_code == 200:
                data = response.json()
                result = f"{data['years']} years, {data['months']} months, {data['days']} days"
            else:
                error = "Age service returned an error"

        except requests.exceptions.RequestException:
            error = "Age service is unavailable"

    return render_template("age.html", result=result, error=error)


# ---------------- SIMPLE CALCULATOR ----------------
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    error = None

    if request.method == "POST":
        try:
            response = requests.post(
                "http://calc-service:5000/calculate",
                json={
                    "a": request.form.get("a"),
                    "b": request.form.get("b"),
                    "operation": request.form.get("operation")
                },
                timeout=3
            )

            if response.status_code == 200:
                result = response.json().get("result")
            else:
                error = "Calculator service returned an error"

        except requests.exceptions.RequestException:
            error = "Calculator service is unavailable"

    return render_template("calculator.html", result=result, error=error)


# ---------------- INTEREST CALCULATOR ----------------
@app.route("/interest", methods=["GET", "POST"])
def interest():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    error = None

    if request.method == "POST":
        try:
            response = requests.post(
                "http://interest-service:5000/calculate",
                json={
                    "principal": request.form.get("principal"),
                    "rate": request.form.get("rate"),
                    "time": request.form.get("time")
                },
                timeout=3
            )

            if response.status_code == 200:
                data = response.json()
                result = f"Interest: {data['interest']} | Total: {data['total_amount']}"
            else:
                error = "Interest service returned an error"

        except requests.exceptions.RequestException:
            error = "Interest service is unavailable"

    return render_template("interest.html", result=result, error=error)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

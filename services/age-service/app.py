from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

@app.route("/age", methods=["POST"])
def calculate_age():
    data = request.get_json()

    day = int(data.get("day"))
    month = int(data.get("month"))
    year = int(data.get("year"))

    today = date.today()
    dob = date(year, month, day)

    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        months -= 1
        days += 30

    if months < 0:
        years -= 1
        months += 12

    return jsonify({
        "years": years,
        "months": months,
        "days": days
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


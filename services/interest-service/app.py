from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/calculate", methods=["POST"])
def calculate_interest():
    data = request.get_json()

    try:
        p = float(data.get("principal"))
        r = float(data.get("rate"))
        t = float(data.get("time"))

        if p < 0 or r < 0 or t < 0:
            return jsonify({"error": "Values must be positive"}), 400

        interest = (p * r * t) / 100
        total = p + interest

        return jsonify({
            "interest": round(interest, 2),
            "total_amount": round(total, 2)
        }), 200

    except Exception:
        return jsonify({"error": "Invalid input"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

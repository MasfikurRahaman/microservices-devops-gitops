from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/api/calc", methods=["POST"])
def calculate():
    data = request.get_json()

    try:
        a = float(data.get("a"))
        b = float(data.get("b"))
        op = data.get("operation")

        if op == "add":
            result = a + b
        elif op == "sub":
            result = a - b
        elif op == "mul":
            result = a * b
        elif op == "div":
            if b == 0:
                return jsonify({"error": "Division by zero"}), 400
            result = a / b
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({"result": result})

    except Exception:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


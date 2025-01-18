from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from math import factorial

app = Flask(__name__)

# Fungsi untuk menghitung kombinasi (nCx)
def kombinasi(n, x):
    return factorial(n) // (factorial(x) * factorial(n - x))

# Fungsi untuk menghitung probabilitas binomial
def probabilitas_binomial(n, x, p):
    nCx = kombinasi(n, x)
    prob = nCx * (p ** x) * ((1 - p) ** (n - x))
    return prob

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        n = int(data["n"])
        p = float(data["p"])
        x = int(data["x"])

        # Perhitungan probabilitas
        probability = probabilitas_binomial(n, x, p)
        steps = [
            f"Rumus: P(X = x) = (nCx) * p^x * (1-p)^(n-x)",
            f"nCx = {n}! / ({x}! * ({n}-{x})!) = {kombinasi(n, x)}",
            f"P(X = {x}) = ({kombinasi(n, x)}) * {p}^{x} * (1-{p})^{n-x}",
            f"P(X = {x}) = {probability:.4f}",
        ]

        # Membuat grafik distribusi binomial
        x_vals = np.arange(0, n + 1)
        y_vals = [probabilitas_binomial(n, i, p) for i in x_vals]

        plt.figure(figsize=(8, 6))
        plt.bar(x_vals, y_vals, color="skyblue", edgecolor="black")
        plt.title("Distribusi Binomial", fontsize=14)
        plt.xlabel("Jumlah Keberhasilan (x)", fontsize=12)
        plt.ylabel("Probabilitas", fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Simpan grafik ke stream byte
        img_stream = BytesIO()
        plt.savefig(img_stream, format="png")
        plt.close()
        img_stream.seek(0)

        # Encode stream ke base64
        graph_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "probability": probability,
            "steps": steps,
            "graph_base64": graph_base64,
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

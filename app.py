from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import binom

app = Flask(__name__)

# Endpoint utama untuk menampilkan form
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint untuk menghitung probabilitas binomial
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        n = int(data["n"])
        p = float(data["p"])
        x = int(data["x"])

        # Perhitungan probabilitas
        probability = binom.pmf(x, n, p)
        steps = [
            f"Rumus: P(X = x) = (nCx) * p^x * (1-p)^(n-x)",
            f"nCx = {n}! / ({x}! * ({n}-{x})!)",
            f"P(X = {x}) = ({n}C{x}) * {p}^{x} * (1-{p})^{n-x}",
            f"P(X = {x}) = {probability:.4f}",
        ]

        # Membuat grafik
        x_vals = np.arange(0, n + 1)
        y_vals = binom.pmf(x_vals, n, p)

        plt.figure(figsize=(8, 6))
        plt.bar(x_vals, y_vals, color="skyblue", edgecolor="black")
        plt.title("Distribusi Binomial", fontsize=14)
        plt.xlabel("Jumlah Keberhasilan (x)", fontsize=12)
        plt.ylabel("Probabilitas", fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        graph_path = os.path.join("static", "graph.png")
        plt.savefig(graph_path)
        plt.close()

        return jsonify({
            "success": True,
            "probability": probability,
            "steps": steps,
            "graph_url": f"/{graph_path}",
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

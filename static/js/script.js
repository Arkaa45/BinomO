document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("binomialForm");
    const resetButton = document.getElementById("resetButton");
    const resultContainer = document.getElementById("result-container");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const n = document.getElementById("n").value;
        const p = document.getElementById("p").value;
        const x = document.getElementById("x").value;

        try {
            const response = await axios.post("/calculate", { n, p, x });
            const result = response.data;

            if (result.success) {
                document.getElementById("result").innerText =
                    `Probabilitas: ${result.probability.toFixed(4)}`;
                const stepsList = document.getElementById("steps");
                stepsList.innerHTML = "";

                result.steps.forEach(step => {
                    const li = document.createElement("li");
                    li.innerText = step;
                    stepsList.appendChild(li);
                });

                const graphImg = document.getElementById("graph");
                graphImg.src = `data:image/png;base64,${result.graph_base64}`;
                graphImg.style.display = "block";

                resultContainer.style.display = "block";
            } else {
                document.getElementById("result").innerText =
                    "Error: " + result.message;
                resultContainer.style.display = "block";
            }
        } catch (error) {
            console.error(error);
            document.getElementById("result").innerText =
                "Terjadi kesalahan pada server.";
            resultContainer.style.display = "block";
        }
    });

    resetButton.addEventListener("click", () => {
        document.getElementById("n").value = "";
        document.getElementById("p").value = "";
        document.getElementById("x").value = "";
        resultContainer.style.display = "none";
    });
});

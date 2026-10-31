const cropEmojis = {
    rice: "🌾", wheat: "🌿", maize: "🌽", chickpea: "🫘",
    kidneybeans: "🫘", pigeonpeas: "🫘", mothbeans: "🫘", mungbean: "🌱",
    blackgram: "🌿", lentil: "🟤", pomegranate: "🍎", banana: "🍌",
    mango: "🥭", grapes: "🍇", watermelon: "🍉", muskmelon: "🍈",
    apple: "🍎", orange: "🍊", papaya: "🍐", coconut: "🥥",
    cotton: "🌸", jute: "🪢", coffee: "☕"
};

function predict() {
    const fields = ["n", "p", "k", "temp", "humidity", "ph", "rainfall"];
    const labels = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH", "Rainfall"];

    const btn = document.getElementById("predict-btn");
    const resultCard = document.getElementById("result-card");
    const resultCrop = document.getElementById("result-crop");
    const resultNote = document.getElementById("result-note");
    const errorMsg = document.getElementById("error-msg");

    // Hide previous results/errors
    resultCard.classList.remove("show");
    errorMsg.classList.remove("show");

    // Validate all fields
    for (let i = 0; i < fields.length; i++) {
        const val = document.getElementById(fields[i]).value;
        if (val === "" || isNaN(val)) {
            errorMsg.textContent = `⚠️ Please enter a valid value for ${labels[i]}.`;
            errorMsg.classList.add("show");
            return;
        }
    }

    const data = {
        N:           parseFloat(document.getElementById("n").value),
        P:           parseFloat(document.getElementById("p").value),
        K:           parseFloat(document.getElementById("k").value),
        temperature: parseFloat(document.getElementById("temp").value),
        humidity:    parseFloat(document.getElementById("humidity").value),
        ph:          parseFloat(document.getElementById("ph").value),
        rainfall:    parseFloat(document.getElementById("rainfall").value)
    };

    // Loading state
    btn.classList.add("loading");
    btn.querySelector(".btn-text").textContent = "Analyzing...";

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => {
        if (!res.ok) throw new Error("Server error: " + res.status);
        return res.json();
    })
    .then(result => {
        const crop = result.prediction;
        const emoji = cropEmojis[crop.toLowerCase()] || "🌱";

        resultCrop.textContent = emoji + " " + crop.charAt(0).toUpperCase() + crop.slice(1);
        resultNote.textContent = "Based on your soil nutrients and climate conditions";
        resultCard.classList.add("show");
    })
    .catch(err => {
        errorMsg.textContent = "❌ Could not connect to the server. Make sure app.py is running on port 5000.";
        errorMsg.classList.add("show");
        console.error(err);
    })
    .finally(() => {
        btn.classList.remove("loading");
        btn.querySelector(".btn-text").textContent = "Analyze & Recommend";
    });
}

// Allow Enter key to submit
document.addEventListener("keydown", e => {
    if (e.key === "Enter") predict();
});
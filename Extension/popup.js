async function loadData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/crypto");

        console.log("Status:", response.status);

        const text = await response.text();
        console.log("Raw response:", text);

        const data = JSON.parse(text);

        console.log("Parsed data:", data);

        displayData(data);

    } catch (error) {
        console.error("Error:", error);
    }
}

function displayData(data) {
    const container = document.getElementById("crypto-container");
    container.innerHTML = "";

    data.forEach(coin => {
        const div = document.createElement("div");
        div.classList.add("crypto-card");

        div.innerHTML = `
            <div>
                <div class="coin-name">${coin.name}</div>
                <div style="font-size:12px; color:gray;">${coin.symbol.toUpperCase()}</div>
            </div>
            <div class="coin-price">
                $${Number(coin.current_price).toLocaleString()}
            </div>
        `;

        container.appendChild(div);
    });
}

loadData();
setInterval(loadData, 15000);
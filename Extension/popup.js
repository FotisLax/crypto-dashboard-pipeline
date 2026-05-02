async function loadData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/crypto");
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error("Error loading top coins:", error);
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
                <div style="font-size:12px; color:gray;">
                    ${coin.symbol.toUpperCase()}
                </div>
            </div>
            <div class="coin-price">
                $${Number(coin.current_price).toLocaleString()}
            </div>
        `;

        container.appendChild(div);
    });
}


async function searchCoin() {
    const coin = document.getElementById("searchInput").value.trim();
    const resultDiv = document.getElementById("searchResult");

    if (!coin) return;

    resultDiv.innerHTML = `<p>Loading...</p>`;

    try {
        const response = await fetch(`http://127.0.0.1:5000/search/${coin}`);
        const data = await response.json();

        if (!response.ok || data.error) {
            resultDiv.innerHTML = `<p style="color:red;">Coin not found</p>`;
            return;
        }

        resultDiv.innerHTML = `
            <div class="crypto-card">
                <div>
                    <div class="coin-name">${data.name}</div>
                    <div style="font-size:12px; color:gray;">
                        ${data.symbol.toUpperCase()}
                    </div>
                </div>
                <div class="coin-price">
                    $${Number(data.current_price).toLocaleString()}
                </div>
            </div>
        `;
    } catch (error) {
        resultDiv.innerHTML = `<p style="color:red;">Server error</p>`;
    }
}


document.getElementById("searchBtn").addEventListener("click", searchCoin);

document.getElementById("searchInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        searchCoin();
    }
});


loadData();
setInterval(loadData, 15000);
// ==============================
// CREATE MAP
// ==============================

const map = L.map("map").setView(
    [31.7, 77.2],
    8
);

// ==============================
// MAP TILES
// ==============================

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "&copy; OpenStreetMap contributors"
    }
).addTo(map);

// ==============================
// DEFAULT LOCATION MARKER
// ==============================

const marker = L.marker(
    [31.7, 77.2]
).addTo(map);

marker.bindPopup(
    "<b>Himachal Pradesh</b><br>Flood monitoring region"
).openPopup();


// ==============================
// FLOOD PREDICTION
// ==============================

const predictButton = document.getElementById("predict-button");

predictButton.addEventListener("click", async () => {

    // Get rainfall values from inputs
    const rainfall_mm_hr = parseFloat(
        document.getElementById("rainfall_mm_hr").value
    );

    const rainfall_mm = parseFloat(
        document.getElementById("rainfall_mm").value
    );

    const rainfall_1hr = parseFloat(
        document.getElementById("rainfall_1hr").value
    );

    const rainfall_3hr = parseFloat(
        document.getElementById("rainfall_3hr").value
    );

    const rainfall_6hr = parseFloat(
        document.getElementById("rainfall_6hr").value
    );

    const rainfall_24hr = parseFloat(
        document.getElementById("rainfall_24hr").value
    );


    // Check if all values are entered
    if (
        isNaN(rainfall_mm_hr) ||
        isNaN(rainfall_mm) ||
        isNaN(rainfall_1hr) ||
        isNaN(rainfall_3hr) ||
        isNaN(rainfall_6hr) ||
        isNaN(rainfall_24hr)
    ) {
        alert("Please enter all rainfall values.");
        return;
    }


    // Change button while processing
    predictButton.innerText = "ANALYZING...";
    predictButton.disabled = true;


    try {

        // Send data to Flask API
        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    rainfall_mm_hr: rainfall_mm_hr,
                    rainfall_mm: rainfall_mm,
                    rainfall_1hr: rainfall_1hr,
                    rainfall_3hr: rainfall_3hr,
                    rainfall_6hr: rainfall_6hr,
                    rainfall_24hr: rainfall_24hr
                })
            }
        );


        // Convert response to JSON
        const result = await response.json();


        // Display probability
        document.getElementById("probability").innerText =
            result.flood_probability;


        // Display risk level
        document.getElementById("risk-level").innerText =
            result.risk_level + " FLOOD RISK";


        // Update message
        document.getElementById("result-message").innerText =
            "Prediction generated using rainfall data and the trained flood risk model.";


    } catch (error) {

        console.error(error);

        document.getElementById("risk-level").innerText =
            "CONNECTION ERROR";

        document.getElementById("result-message").innerText =
            "Could not connect to the prediction server.";

    }


    // Restore button
    predictButton.innerText = "ANALYZE FLOOD RISK";
    predictButton.disabled = false;

});
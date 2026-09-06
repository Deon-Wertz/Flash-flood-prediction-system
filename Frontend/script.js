/* =========================================================
   FLASH FLOOD PREDICTION SYSTEM
   FINAL JAVASCRIPT
========================================================= */


/* =========================================================
   1. DEMONSTRATION DATA
========================================================= */

const scenarios = {

    normal: {
        rainfall_mm_hr: 0.2,
        rainfall_mm: 0.1,
        rainfall_1hr: 0.5,
        rainfall_3hr: 1.2,
        rainfall_6hr: 2.5,
        rainfall_24hr: 8
    },

    moderate: {
        rainfall_mm_hr: 4,
        rainfall_mm: 2,
        rainfall_1hr: 5,
        rainfall_3hr: 12,
        rainfall_6hr: 25,
        rainfall_24hr: 50
    },

    heavy: {
        rainfall_mm_hr: 15,
        rainfall_mm: 7.5,
        rainfall_1hr: 18,
        rainfall_3hr: 45,
        rainfall_6hr: 85,
        rainfall_24hr: 150
    },

    extreme: {
        rainfall_mm_hr: 40,
        rainfall_mm: 20,
        rainfall_1hr: 50,
        rainfall_3hr: 120,
        rainfall_6hr: 220,
        rainfall_24hr: 350
    }

};


/* =========================================================
   2. LOCATIONS
========================================================= */

const locations = [

    {
        name: "Kangra",
        district: "Kangra, Himachal Pradesh",
        lat: 32.099,
        lng: 76.269
    },

    {
        name: "Manali",
        district: "Kullu, Himachal Pradesh",
        lat: 32.2396,
        lng: 77.1887
    },

    {
        name: "Kullu",
        district: "Kullu, Himachal Pradesh",
        lat: 31.9579,
        lng: 77.1095
    },

    {
        name: "Mandi",
        district: "Mandi, Himachal Pradesh",
        lat: 31.708,
        lng: 76.931
    },

    {
        name: "Chamba",
        district: "Chamba, Himachal Pradesh",
        lat: 32.5534,
        lng: 76.1258
    }

];


/* =========================================================
   3. GLOBAL STATE
========================================================= */

let currentLocation = locations[0];

let currentScenario = "normal";

let simulationRunning = false;

let simulationInterval = null;


/* =========================================================
   4. DOM ELEMENTS
========================================================= */

const rainfallInputs = {

    rainfall_mm_hr:
        document.getElementById("rainfall_mm_hr"),

    rainfall_mm:
        document.getElementById("rainfall_mm"),

    rainfall_1hr:
        document.getElementById("rainfall_1hr"),

    rainfall_3hr:
        document.getElementById("rainfall_3hr"),

    rainfall_6hr:
        document.getElementById("rainfall_6hr"),

    rainfall_24hr:
        document.getElementById("rainfall_24hr")

};


const predictButton =
    document.getElementById("predict-button");

const probabilityElement =
    document.getElementById("probability");

const riskLevelElement =
    document.getElementById("risk-level");

const resultMessageElement =
    document.getElementById("result-message");

const predictionStatus =
    document.getElementById("prediction-status");

const riskIndicator =
    document.getElementById("risk-indicator");

const coordinatesElement =
    document.getElementById("coordinates");

const locationSelect =
    document.getElementById("location-select");


/* =========================================================
   5. MAP
========================================================= */

const map = L.map("map").setView(
    [
        currentLocation.lat,
        currentLocation.lng
    ],
    10
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


const marker = L.marker([
    currentLocation.lat,
    currentLocation.lng
]).addTo(map);


marker.bindPopup(
    `<b>${currentLocation.name}</b><br>
     ${currentLocation.district}<br>
     Flash flood monitoring location`
);


/* =========================================================
   6. MAP MARKER
========================================================= */

function updateMarker(color) {

    const colors = {

        green: "#22c55e",
        orange: "#f59e0b",
        red: "#ef4444",
        darkred: "#991b1b",
        blue: "#38bdf8"

    };


    const selectedColor =
        colors[color] || colors.blue;


    const icon = L.divIcon({

        className: "",

        html: `
            <div style="
                width:24px;
                height:24px;
                background:${selectedColor};
                border-radius:50%;
                border:4px solid white;
                box-shadow:0 0 18px ${selectedColor};
            "></div>
        `,

        iconSize: [24, 24],

        iconAnchor: [12, 12]

    });


    marker.setIcon(icon);


    marker.setPopupContent(
        `<b>${currentLocation.name}</b><br>
        ${currentLocation.district}<br>
        <b>Risk:</b> ${color.toUpperCase()}`
    );

}


/* =========================================================
   7. UPDATE LOCATION
========================================================= */

function updateLocation(location) {

    currentLocation = location;


    map.setView(
        [
            location.lat,
            location.lng
        ],
        11
    );


    marker.setLatLng([
        location.lat,
        location.lng
    ]);


    marker.setPopupContent(
        `<b>${location.name}</b><br>
        ${location.district}<br>
        Flash flood monitoring location`
    );


    coordinatesElement.innerText =
        `${location.lat.toFixed(4)}° N, ${location.lng.toFixed(4)}° E`;

}


/* =========================================================
   8. INPUT FUNCTIONS
========================================================= */

function updateInputs(data) {

    Object.keys(rainfallInputs).forEach(key => {

        if (rainfallInputs[key]) {

            rainfallInputs[key].value =
                data[key];

        }

    });

}


function getInputData() {

    const data = {};


    Object.keys(rainfallInputs).forEach(key => {

        data[key] =
            parseFloat(
                rainfallInputs[key].value
            );

    });


    return data;

}


/* =========================================================
   9. TELEMETRY
========================================================= */

function updateTelemetry(data) {

    const rainfall =
        Number(data.rainfall_mm_hr) || 0;


    const rainfallElement =
        document.getElementById(
            "telemetry-rainfall"
        );


    const rainfallBar =
        document.getElementById(
            "rainfall-indicator"
        );


    const soilElement =
        document.getElementById(
            "soil-saturation"
        );


    const soilBar =
        document.getElementById(
            "soil-indicator"
        );


    const riverElement =
        document.getElementById(
            "river-level"
        );


    const slopeElement =
        document.getElementById(
            "slope-tilt"
        );


    const riverStatus =
        document.getElementById(
            "river-status"
        );


    const slopeStatus =
        document.getElementById(
            "slope-status"
        );


    /*
       Convert rainfall into realistic
       demonstration sensor values.
    */

    const soil =
        Math.min(
            98,
            25 + rainfall * 2
        );


    const river =
        Math.max(
            0,
            rainfall * 0.012
        );


    const slope =
        Math.max(
            0.4,
            rainfall * 0.08
        );


    if (rainfallElement) {

        rainfallElement.innerText =
            rainfall.toFixed(1);

    }


    if (rainfallBar) {

        rainfallBar.style.width =
            Math.min(
                100,
                (rainfall / 50) * 100
            ) + "%";

    }


    if (soilElement) {

        soilElement.innerText =
            Math.round(soil);

    }


    if (soilBar) {

        soilBar.style.width =
            soil + "%";

    }


    if (riverElement) {

        riverElement.innerText =
            "+" + river.toFixed(2);

    }


    if (slopeElement) {

        slopeElement.innerText =
            slope.toFixed(1);

    }


    if (riverStatus) {

        riverStatus.innerText =
            rainfall >= 15
                ? "Elevated"
                : rainfall >= 5
                    ? "Rising"
                    : "Normal";

    }


    if (slopeStatus) {

        slopeStatus.innerText =
            slope >= 2
                ? "Unstable"
                : slope >= 1
                    ? "Watch"
                    : "Stable";

    }

}


/* =========================================================
   10. ML CONFIDENCE
========================================================= */

function updateMLConfidence(probability) {

    probability =
        Number(probability) || 0;


    const xgb =
        Math.min(
            99,
            Math.max(
                20,
                probability + 8
            )
        );


    const lstm =
        Math.min(
            99,
            Math.max(
                15,
                probability - 3
            )
        );


    const xgbElement =
        document.getElementById(
            "xgb-confidence"
        );


    const lstmElement =
        document.getElementById(
            "lstm-confidence"
        );


    if (xgbElement) {

        xgbElement.innerText =
            Math.round(xgb) + "%";

    }


    if (lstmElement) {

        lstmElement.innerText =
            Math.round(lstm) + "%";

    }

}


/* =========================================================
   11. RISK UI
========================================================= */

function updateRiskUI(probability, risk) {

    probability =
        Number(probability) || 0;


    let position =
        Math.min(
            100,
            Math.max(0, probability)
        );


    riskIndicator.style.left =
        position + "%";


    let color = "blue";


    if (risk === "LOW") {

        color = "green";

    }

    else if (risk === "MODERATE") {

        color = "orange";

    }

    else if (risk === "HIGH") {

        color = "red";

    }

    else if (
        risk === "SEVERE" ||
        risk === "EXTREME"
    ) {

        color = "darkred";

    }


    updateMarker(color);

}


/* =========================================================
   12. ALERT SYSTEM
========================================================= */

function updateAlert(risk) {

    const alertCard =
        document.getElementById(
            "alert-card"
        );

    const alertTitle =
        document.getElementById(
            "alert-title"
        );

    const alertMessage =
        document.getElementById(
            "alert-message"
        );

    const alertStatus =
        document.getElementById(
            "alert-status"
        );


    if (!alertCard) return;


    /*
       Reset classes.
    */

    alertCard.style.borderColor =
        "rgba(56, 189, 248, 0.18)";


    alertStatus.style.background =
        "rgba(34, 197, 94, 0.1)";


    alertStatus.style.color =
        "#86efac";


    if (risk === "LOW") {

        alertTitle.innerText =
            "Monitoring Conditions";

        alertMessage.innerText =
            "Environmental conditions are currently stable.";

        alertStatus.innerText =
            "NORMAL";

    }


    else if (risk === "MODERATE") {

        alertTitle.innerText =
            "Elevated Monitoring";

        alertMessage.innerText =
            "Rainfall conditions are increasing. Continue monitoring the region.";

        alertStatus.innerText =
            "WATCH";

        alertCard.style.borderColor =
            "rgba(245, 158, 11, 0.35)";

        alertStatus.style.background =
            "rgba(245, 158, 11, 0.12)";

        alertStatus.style.color =
            "#fbbf24";

    }


    else if (risk === "HIGH") {

        alertTitle.innerText =
            "High Flood Risk";

        alertMessage.innerText =
            "Heavy rainfall detected. Local response teams should remain prepared.";

        alertStatus.innerText =
            "ALERT";

        alertCard.style.borderColor =
            "rgba(239, 68, 68, 0.4)";

        alertStatus.style.background =
            "rgba(239, 68, 68, 0.12)";

        alertStatus.style.color =
            "#f87171";

    }


    else {

        alertTitle.innerText =
            "Emergency Flood Warning";

        alertMessage.innerText =
            "Extreme rainfall conditions detected. Emergency response may be required.";

        alertStatus.innerText =
            "EMERGENCY";

        alertCard.style.borderColor =
            "rgba(239, 68, 68, 0.65)";

        alertStatus.style.background =
            "rgba(239, 68, 68, 0.18)";

        alertStatus.style.color =
            "#fca5a5";

    }

}


/* =========================================================
   13. UPDATE PREDICTION DISPLAY
========================================================= */

function updatePrediction(result) {

    let probability =
        Number(
            result.flood_probability
        );


    if (isNaN(probability)) {

        probability = 0;

    }


    /*
       Some Flask APIs return 0.86
       instead of 86.
    */

    if (probability <= 1) {

        probability *= 100;

    }


    probability =
        Math.min(
            100,
            Math.max(
                0,
                probability
            )
        );


    probability =
        Number(
            probability.toFixed(1)
        );


    let risk =
        String(
            result.risk_level || "LOW"
        ).toUpperCase();


    probabilityElement.innerText =
        probability.toFixed(1);


    riskLevelElement.innerText =
        risk + " FLOOD RISK";


    predictionStatus.innerText =
        risk === "LOW"
            ? "MONITORING"
            : risk === "MODERATE"
                ? "WATCH"
                : risk === "HIGH"
                    ? "ALERT"
                    : "EMERGENCY";


    let message = "";


    if (risk === "LOW") {

        message =
            "Rainfall conditions are currently within the low flood-risk range.";

    }

    else if (risk === "MODERATE") {

        message =
            "Moderate rainfall conditions detected. Continued monitoring is recommended.";

    }

    else if (risk === "HIGH") {

        message =
            "Heavy rainfall detected. Flood risk is high. Remain alert.";

    }

    else {

        message =
            "Extreme rainfall conditions detected. Severe flood risk warning.";

    }


    resultMessageElement.innerText =
        message;


    updateRiskUI(
        probability,
        risk
    );


    updateMLConfidence(
        probability
    );


    updateAlert(
        risk
    );


    const now =
        new Date();


    const time =
        now.toLocaleTimeString();


    const lastUpdated =
        document.getElementById(
            "last-updated"
        );


    const statusLastUpdate =
        document.getElementById(
            "status-last-update"
        );


    if (lastUpdated) {

        lastUpdated.innerText =
            time;

    }


    if (statusLastUpdate) {

        statusLastUpdate.innerText =
            time;

    }

}


/* =========================================================
   14. BACKEND PREDICTION
========================================================= */

async function predictFlood(data) {

    try {

        predictionStatus.innerText =
            "ANALYZING";


        const response =
            await fetch(
    "https://flash-flood-prediction-system.onrender.com/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const result =
            await response.json();


        console.log(
            "ML Prediction:",
            result
        );


        updatePrediction(
            result
        );


    }

    catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        predictionStatus.innerText =
            "OFFLINE";


        riskLevelElement.innerText =
            "BACKEND ERROR";


        resultMessageElement.innerText =
            "Could not connect to the Flask prediction server.";


        /*
           We still update the telemetry so
           the dashboard doesn't look dead.
        */

        updateTelemetry(data);

    }

}


/* =========================================================
   15. SCENARIO SELECTION
========================================================= */

function selectScenario(name) {

    if (!scenarios[name]) {

        return;

    }


    currentScenario =
        name;


    /*
       Stop live simulation when
       selecting a scenario.
    */

    if (simulationRunning) {

        stopSimulation();

    }


    const data =
        scenarios[name];


    /*
       Fill rainfall inputs.
    */

    updateInputs(
        data
    );


    /*
       Update telemetry immediately.
    */

    updateTelemetry(
        data
    );


    /*
       Highlight selected card.
    */

    document
        .querySelectorAll(
            ".scenario-card"
        )
        .forEach(card => {

            card.classList.remove(
                "active-scenario"
            );

        });


    const card =
        document.getElementById(
            name + "-scenario"
        );


    if (card) {

        card.classList.add(
            "active-scenario"
        );

    }


    /*
       Ask Flask for actual prediction.
    */

    predictFlood(
        data
    );

}


/* =========================================================
   16. SCENARIO BUTTONS
========================================================= */

document
    .getElementById("normal-scenario")
    ?.addEventListener(
        "click",
        () => selectScenario("normal")
    );


document
    .getElementById("moderate-scenario")
    ?.addEventListener(
        "click",
        () => selectScenario("moderate")
    );


document
    .getElementById("heavy-scenario")
    ?.addEventListener(
        "click",
        () => selectScenario("heavy")
    );


document
    .getElementById("extreme-scenario")
    ?.addEventListener(
        "click",
        () => selectScenario("extreme")
    );


/* =========================================================
   17. MANUAL ANALYSIS
========================================================= */

predictButton?.addEventListener(
    "click",
    async () => {

        const data =
            getInputData();


        const invalid =
            Object.values(data)
                .some(
                    value =>
                        Number.isNaN(value)
                );


        if (invalid) {

            alert(
                "Please enter all rainfall values."
            );

            return;

        }


        predictButton.innerText =
            "⚡ ANALYZING...";


        predictButton.disabled =
            true;


        updateTelemetry(
            data
        );


        await predictFlood(
            data
        );


        predictButton.innerText =
            "⚡ ANALYZE FLOOD RISK";


        predictButton.disabled =
            false;

    }
);

/*
===============
   18. LIVE SIMULATION DATA
========================================================= */

function generateLiveData() {

    const base =
        scenarios[currentScenario];


    const variation =
        (Math.random() * 2) - 1;


    const intensity =
        Math.max(
            0,
            base.rainfall_mm_hr +
            variation * 2
        );


    const amount =
        Math.max(
            0,
            base.rainfall_mm +
            variation
        );


    const oneHour =
        Math.max(
            0,
            base.rainfall_1hr +
            variation * 2
        );


    const threeHour =
        Math.max(
            oneHour,
            base.rainfall_3hr +
            variation * 4
        );


    const sixHour =
        Math.max(
            threeHour,
            base.rainfall_6hr +
            variation * 6
        );


    const twentyFourHour =
        Math.max(
            sixHour,
            base.rainfall_24hr +
            variation * 10
        );


    return {

        rainfall_mm_hr:
            Number(
                intensity.toFixed(2)
            ),

        rainfall_mm:
            Number(
                amount.toFixed(2)
            ),

        rainfall_1hr:
            Number(
                oneHour.toFixed(2)
            ),

        rainfall_3hr:
            Number(
                threeHour.toFixed(2)
            ),

        rainfall_6hr:
            Number(
                sixHour.toFixed(2)
            ),

        rainfall_24hr:
            Number(
                twentyFourHour.toFixed(2)
            )

    };

}


/* =========================================================
   19. RUN LIVE SIMULATION
========================================================= */

function runSimulation() {

    const data =
        generateLiveData();


    updateInputs(
        data
    );


    updateTelemetry(
        data
    );


    predictFlood(
        data
    );

}


/* =========================================================
   20. STOP SIMULATION
========================================================= */

function stopSimulation() {

    simulationRunning =
        false;


    clearInterval(
        simulationInterval
    );


    simulationInterval =
        null;


    const button =
        document.getElementById(
            "simulation-button"
        );


    if (button) {

        button.innerText =
            "▶ START LIVE SIMULATION";

    }

}


/* =========================================================
   21. START / STOP SIMULATION
========================================================= */

function toggleSimulation() {

    const button =
        document.getElementById(
            "simulation-button"
        );


    if (!button) {

        return;

    }


    if (!simulationRunning) {

        simulationRunning =
            true;


        button.innerText =
            "⏸ STOP LIVE SIMULATION";


        runSimulation();


        simulationInterval =
            setInterval(
                runSimulation,
                4000
            );

    }

    else {

        stopSimulation();

    }

}


document
    .getElementById(
        "simulation-button"
    )
    ?.addEventListener(
        "click",
        toggleSimulation
    );


/* =========================================================
   22. LOCATION SELECTOR
========================================================= */

locationSelect?.addEventListener(
    "change",
    function () {

        const selected =
            locations.find(
                location =>
                    location.name ===
                    this.value
            );


        if (!selected) {

            return;

        }


        updateLocation(
            selected
        );

    }
);


/* =========================================================
   23. INITIALIZE DASHBOARD
========================================================= */

updateLocation(
    currentLocation
);


updateInputs(
    scenarios.normal
);


updateTelemetry(
    scenarios.normal
);


selectScenario(
    "normal"
);


console.log(
    "Flash Flood Prediction System initialized."
);
// ==========================================================
// Medingo AI Dashboard
// ==========================================================

const API = "https://medingo.onrender.com/";

const phcSelect = document.getElementById("phcSelect");
const predictBtn = document.getElementById("predictBtn");

const patients = document.getElementById("patients");
const stock = document.getElementById("stock");
const doctor = document.getElementById("doctor");

const paracetamol = document.getElementById("paracetamol");
const amoxicillin = document.getElementById("amoxicillin");

const riskFill = document.getElementById("riskFill");
const riskText = document.getElementById("riskText");

const alerts = document.getElementById("alerts");

const aiExplanation = document.getElementById("aiExplanation");


// ==========================================================
// Load PHCs
// ==========================================================

async function loadPHCs() {

    try {

        const response = await fetch(`${API}/phcs`);

        const data = await response.json();

        phcSelect.innerHTML = "";

        data.phcs.forEach(phc => {

            const option = document.createElement("option");

            option.value = phc;

            option.textContent = phc;

            phcSelect.appendChild(option);

        });

    }

    catch (err) {

        console.error(err);

        alert("Cannot connect to backend.");

    }

}


// ==========================================================
// Calculate Risk Score
// ==========================================================

function calculateRisk(data){

    let risk = 0;

    risk += Math.min(50, data.doctor_utilization * 0.5);

    if(data.remaining_stock < 1000)
        risk += 15;

    if(data.remaining_stock < 600)
        risk += 15;

    risk += Math.min(20, data.alerts.length * 5);

    return Math.min(100, Math.round(risk));

}


// ==========================================================
// Generate Forecast
// ==========================================================

async function generateForecast(){

    try{

        predictBtn.disabled = true;

        predictBtn.innerText = "Generating...";

        const phc = phcSelect.value;

        const response = await fetch(

            `${API}/forecast/${phc}`

        );

        const data = await response.json();

        const p = data.prediction;

        patients.innerText = p.predicted_patients;

        stock.innerText = p.remaining_stock;

        doctor.innerText = p.doctor_utilization + "%";

        paracetamol.innerText = p.paracetamol_needed;

        amoxicillin.innerText = p.amoxicillin_needed;

        // =============================
        // Risk Score
        // =============================

        const risk = p.risk_score ?? calculateRisk(p);

        riskFill.style.width = risk + "%";

        riskText.innerText = risk + " / 100";

        // =============================
        // Alerts
        // =============================

        alerts.innerHTML = "";

        p.alerts.forEach(alert => {

            const li = document.createElement("li");

            li.innerHTML = "⚠ " + alert;

            alerts.appendChild(li);

        });

        // =============================
        // AI
        // =============================

        aiExplanation.innerText = data.ai_explanation;

    }

    catch(err){

        console.error(err);

        alert("Unable to generate forecast.");

    }

    finally{

        predictBtn.disabled = false;

        predictBtn.innerText = "Generate Forecast";

    }

}


// ==========================================================
// Events
// ==========================================================

predictBtn.addEventListener(

    "click",

    generateForecast

);


// ==========================================================
// Start
// ==========================================================

loadPHCs();
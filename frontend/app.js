// ==========================================================
// Medingo AI v0.2
// Frontend Controller
// ==========================================================

// ===============================
// Backend URL
// ===============================

const API = "https://medingo.onrender.com";


// ===============================
// DOM Elements
// ===============================

const phcSelect = document.getElementById("phcSelect");
const generateBtn = document.getElementById("generateBtn");

const reportSection = document.getElementById("reportSection");

const patients = document.getElementById("patients");
const stock = document.getElementById("stock");
const doctor = document.getElementById("doctor");

const para = document.getElementById("para");
const amox = document.getElementById("amox");

const riskScore = document.getElementById("riskScore");

const summaryText = document.getElementById("summaryText");
const aiExplanation = document.getElementById("aiExplanation");

const alerts = document.getElementById("alerts");


// ===============================
// Pipeline
// ===============================

const pipeline = [

    {
        id: "hospital",
        waiting: "Waiting...",
        processing: "Collecting Hospital Records...",
        completed: "Hospital Records Loaded"
    },

    {
        id: "weather",
        waiting: "Waiting...",
        processing: "Loading Weather Intelligence...",
        completed: "Weather Processed"
    },

    {
        id: "disease",
        waiting: "Waiting...",
        processing: "Reading Disease Trends...",
        completed: "Disease Trends Ready"
    },

    {
        id: "calendar",
        waiting: "Waiting...",
        processing: "Analyzing Calendar...",
        completed: "Calendar Processed"
    },

    {
        id: "simulation",
        waiting: "Waiting...",
        processing: "Generating Synthetic Dataset...",
        completed: "27,375 Records Generated"
    },

    {
        id: "features",
        waiting: "Waiting...",
        processing: "Preparing ML Features...",
        completed: "41 Features Ready"
    },

    {
        id: "xgboost",
        waiting: "Waiting...",
        processing: "Running XGBoost...",
        completed: "Forecast Generated"
    },

    {
        id: "risk",
        waiting: "Waiting...",
        processing: "Calculating Operational Risk...",
        completed: "Risk Score Generated"
    },

    {
        id: "gemini",
        waiting: "Waiting...",
        processing: "Writing Executive Summary...",
        completed: "Executive Summary Ready"
    }

];

// ==========================================================
// Utility Functions
// ==========================================================

function sleep(ms){

    return new Promise(resolve => setTimeout(resolve, ms));

}

function getStatus(node){

    return node.querySelector(".status");

}

function resetPipeline(){

    reportSection.classList.remove("show");

    pipeline.forEach(step=>{

        const node = document.getElementById(step.id);

        console.log("Checking:", step.id, node);

        if(!node){
            console.error("Missing node:", step.id);
            return;
        }

        const status = node.querySelector(".status");

        node.classList.remove("active","done");

        if(status){
            status.classList.remove("active","done");
            status.innerText = step.waiting;
        }

    });

}

// ==========================================================
// Count Animation
// ==========================================================

async function animateCounter(element, endValue, duration = 800){

    let start = 0;

    const increment = Math.ceil(endValue / 50);

    while(start < endValue){

        start += increment;

        if(start > endValue){

            start = endValue;

        }

        element.innerText = start.toLocaleString();

        await sleep(duration / 50);

    }

}



// ==========================================================
// AI Pipeline Animation
// ==========================================================

async function animatePipeline(){

    resetPipeline();

    for(const step of pipeline){

        const node = document.getElementById(step.id);

        const status = getStatus(node);

        node.scrollIntoView({

            behavior:"smooth",

            block:"center"

        });

        node.classList.add("active");

        status.classList.add("active");

        status.innerText = step.processing;

        // ==========================================
        // Simulation Engine Animation
        // ==========================================

        if(step.id === "simulation"){

            const stats = node.querySelectorAll("strong");

            await animateCounter(stats[0],27375);

            await animateCounter(stats[1],41,400);

            await animateCounter(stats[2],25,400);

        }

        // ==========================================
        // XGBoost Animation
        // ==========================================

        if(step.id === "xgboost"){

            for(let i=0;i<=10;i++){

                status.innerHTML =

                "Running Model " +

                "█".repeat(i) +

                "░".repeat(10-i);

                await sleep(120);

            }

        }

        // ==========================================
        // Gemini Animation
        // ==========================================

        if(step.id === "gemini"){

            for(let i=0;i<6;i++){

                status.innerHTML =

                "Generating Executive Summary" +

                ".".repeat((i%3)+1);

                await sleep(250);

            }

        }

        status.classList.remove("active");

        status.classList.add("done");

        status.innerHTML =

        "✔ " + step.completed;

        node.classList.remove("active");

        node.classList.add("done");

        await sleep(250);

    }

}

// ==========================================================
// Load PHCs
// ==========================================================

async function loadPHCs(){

    try{

        const response = await fetch(`${API}/phcs`);

        if(!response.ok){

            throw new Error("Unable to load PHCs");

        }

        const data = await response.json();

        phcSelect.innerHTML = "";

        data.phcs.forEach(phc=>{

            const option = document.createElement("option");

            option.value = phc;

            option.textContent = phc;

            phcSelect.appendChild(option);

        });

    }

    catch(error){

        console.error(error);

        alert("Cannot connect to backend.");

    }

}

// ==========================================================
// Calculate Risk
// ==========================================================

function calculateRisk(data){

    let risk = 0;

    risk += Math.min(50,data.doctor_utilization*0.5);

    if(data.remaining_stock<1000){

        risk += 15;

    }

    if(data.remaining_stock<600){

        risk += 15;

    }

    risk += Math.min(20,data.alerts.length*5);

    return Math.min(100,Math.round(risk));

}

// ==========================================================
// Type Writer
// ==========================================================

async function typeWriter(element,text,speed=12){

    element.innerHTML="";

    for(const letter of text){

        element.innerHTML += letter;

        await sleep(speed);

    }

}

// ==========================================================
// Populate Report
// ==========================================================

async function populateReport(data){

    const p = data.prediction;

    const risk = p.risk_score ?? calculateRisk(p);

    await animateCounter(

        patients,

        p.predicted_patients,

        700

    );

    await animateCounter(

        stock,

        p.remaining_stock,

        700

    );

    doctor.innerText =

    p.doctor_utilization + "%";

    para.innerText =

    p.paracetamol_needed;

    amox.innerText =

    p.amoxicillin_needed;

    riskScore.innerText = risk;

    alerts.innerHTML = "";

    p.alerts.forEach(item=>{

        const li = document.createElement("li");

        li.innerHTML = "⚠ " + item;

        alerts.appendChild(li);

    });

    summaryText.innerText =

    `PHC ${p.phc_id} is expected to handle ${p.predicted_patients} patients tomorrow with an operational risk score of ${risk}/100.`;

    await typeWriter(

        aiExplanation,

        data.ai_explanation,

        8

    );

}

// ==========================================================
// Generate Forecast
// ==========================================================

async function generateForecast(){

    try{

        generateBtn.disabled = true;

        generateBtn.innerText = "Generating...";

        // Start Animation + Backend Together

        const animationPromise = animatePipeline();

        const apiPromise = fetch(

            `${API}/forecast/${phcSelect.value}`

        );

        const [_, response] = await Promise.all([

            animationPromise,

            apiPromise

        ]);

        if(!response.ok){

            throw new Error("Forecast Failed");

        }

        const data = await response.json();

        reportSection.classList.add("show");

        await populateReport(data);

        reportSection.scrollIntoView({

            behavior:"smooth",

            block:"start"

        });

    }

    catch(error){

        console.error(error);

        alert("Unable to generate forecast.");

    }

    finally{

        generateBtn.disabled = false;

        generateBtn.innerText =

        "Generate Tomorrow's Report";

    }

}

// ==========================================================
// Events
// ==========================================================

generateBtn.addEventListener(

    "click",

    generateForecast

);

// ==========================================================
// Start Application
// ==========================================================

loadPHCs();

resetPipeline();

lucide.createIcons();
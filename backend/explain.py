"""
===========================================================
Medingo AI Explainer
===========================================================

Uses Gemini to explain the prediction
in simple natural language.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# ==========================================================
# Configure Gemini
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise Exception(
        "GOOGLE_API_KEY not found in environment variables."
    )

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ==========================================================
# AI Explanation
# ==========================================================

def generate_explanation(prediction):

    prompt = f"""

You are Medingo AI, an intelligent healthcare planning assistant for Primary Health Centres.

Based on the prediction below, generate a professional operational report.

Prediction:
- PHC ID: {prediction["phc_id"]}
- Predicted Patients: {prediction["predicted_patients"]}
- Paracetamol Required: {prediction["paracetamol_needed"]}
- Amoxicillin Required: {prediction["amoxicillin_needed"]}
- Remaining Medicine Stock: {prediction["remaining_stock"]}
- Doctor Utilization: {prediction["doctor_utilization"]}%
- Overall Risk Score: {prediction["risk_score"]}/100
- Alerts: {", ".join(prediction["alerts"])}

Generate the response in EXACTLY this format:

Executive Summary:
(2 concise sentences)

Operational Risks:
• Bullet points only

Recommended Actions:
• Bullet points only

Overall Risk Score:
Explain why the operational risk score is {prediction["risk_score"]}/100.

Do NOT change the score.
Do NOT recalculate it.
Only explain the factors that contributed to it.

Keep the response under 180 words.
Use professional healthcare language.
Never exaggerate.
Base every recommendation only on the provided prediction.
Do not invent new risks.
Do not use Markdown.
"""

    response = model.generate_content(prompt)

    return response.text.strip()




# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = {

        "phc_id": "PHC_01",

        "predicted_patients": 88,

        "paracetamol_needed": 61,

        "amoxicillin_needed": 15,

        "remaining_stock": 1364,

        "doctor_utilization": 97.8,

        "risk_score": 54,

        "alerts": [

            "Operations Normal"

        ]

    }

    explanation = generate_explanation(sample)

    print()

    print(explanation)
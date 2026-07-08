"""
===========================================================
Medingo Backend API
===========================================================

FastAPI Backend

Endpoints

GET /
GET /forecast/{phc_id}
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_tomorrow
from explain import generate_explanation


# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(

    title="Medingo AI",

    version="1.0"

)


# ==========================================================
# Enable CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==========================================================
# Home
# ==========================================================

@app.get("/")

def home():

    return {

        "message": "Medingo AI Backend Running",

        "status": "success"

    }


# ==========================================================
# Forecast Endpoint
# ==========================================================

@app.get("/forecast/{phc_id}")

def forecast(phc_id: str):

    prediction = predict_tomorrow(phc_id)

    explanation = generate_explanation(prediction)

    return {

        "prediction": prediction,

        "ai_explanation": explanation

    }


@app.get("/phcs")
def get_phcs():

    return {

        "phcs": [

            f"PHC_{i:02d}"

            for i in range(1,26)

        ]

    }

# ==========================================================
# Run Server
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )
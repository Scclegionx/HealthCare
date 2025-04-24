from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import HealthcareChatbot
import numpy as np
import uvicorn

app = FastAPI(title="Healthcare Chatbot API")

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các method
    allow_headers=["*"],  # Cho phép tất cả các header
)

class SymptomRequest(BaseModel):
    symptoms: list[int]

class DiagnosisResponse(BaseModel):
    diagnosis: str
    probability: float
    diseases: list[str]
    probabilities: list[float]
    uncertainties: list[float]
    test: str
    medicine: str

chatbot = HealthcareChatbot()
chatbot.load_model()

@app.get("/symptoms")
async def get_symptoms():
    try:
        return chatbot.symptom_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=DiagnosisResponse)
async def predict_diagnosis(request: SymptomRequest):
    try:
        # Chuyển đổi symptoms thành vector nhị phân
        symptom_vector = np.zeros(len(chatbot.symptom_names))
        for idx in request.symptoms:
            symptom_vector[idx] = 1
        
        # Dự đoán
        diagnosis, mean_probs, std_probs = chatbot.get_diagnosis(symptom_vector)
        test, medicine = chatbot.get_recommendations(diagnosis)
        
        return DiagnosisResponse(
            diagnosis=diagnosis,
            probability=float(mean_probs[chatbot.diseases.index(diagnosis)]),
            diseases=chatbot.diseases,
            probabilities=mean_probs.tolist(),
            uncertainties=std_probs.tolist(),
            test=test,
            medicine=medicine
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081) 
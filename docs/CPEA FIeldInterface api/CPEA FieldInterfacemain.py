from fastapi import FastAPI

app = FastAPI(
    title="CPEA-FieldInterface",
    version="0.1"
)

@app.get("/")
def root():
    return {
        "status": "active",
        "framework": "CPEA-FieldInterface"
    }

@app.get("/coherence")
def coherence():
    return {
        "coherence_score": 0.82,
        "collapse_risk": 0.31
    }

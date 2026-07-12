from fastapi import FastAPI

app = FastAPI(
    title="Gold AI Market Intelligence Platform",
    description="AI-powered financial intelligence platform for gold market analysis",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "gold-ai-backend"
    }
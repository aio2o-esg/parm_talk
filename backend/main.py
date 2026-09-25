from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, merchants, esg, coupons, dashboard, analytics

app = FastAPI(
    title="SME-TALK API",
    description="Algorand 기반 ESG-Gold 플랫폼 백엔드",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sme-talk.vercel.app",
        "http://localhost:19006",
        "exp://",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(merchants.router)
app.include_router(esg.router)
app.include_router(coupons.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "SME-TALK API 서버 정상 작동 중", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

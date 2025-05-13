from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import knowledge_base, chatbot, post_call

app = FastAPI(
    title="BBQ Nation",
    description="Chatbot for BBQ Nation",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(knowledge_base.router, prefix="/api/knowledge-based", tags=["Knowledge Base"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(post_call.router, prefix="/api/analyze", tags=["Post-Call Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to BBQ Nation"} 
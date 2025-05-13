from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import json
import tiktoken
from app.utils.token_manager import TokenManager

router = APIRouter()
token_manager = TokenManager()

# Request models
class Query(BaseModel):
    city: str
    branch: str

class KnowledgeBaseQuery(BaseModel):
    text: str
    property: Optional[str] = None
    category: Optional[str] = None

# Response model
class KnowledgeResponse(BaseModel):
    content: str
    source: str
    confidence: float
    tokens: int

# GET endpoint to list available cities
@router.get("/properties")
async def get_properties():
    """Get list of available properties"""
    return {
        "properties": [
            {"id": "Delhi", "name": "BBQ Nation Delhi"},
            {"id": "Bangalore", "name": "BBQ Nation Bangalore"}
        ]
    }

# GET endpoint to list knowledge categories
@router.get("/categories")
async def get_categories():
    """Get list of available knowledge base categories"""
    return {
        "categories": [
            "menu",
            "pricing",
            "location",
            "hours",
            "booking",
            "faq"
        ]
    }

# POST endpoint to simulate querying the knowledge base
@router.post("/query")
async def query_knowledge_base(query: KnowledgeBaseQuery) -> KnowledgeResponse:
    """
    Query the knowledge base with a text query
    Returns information in chunks of max 800 tokens
    """
    try:
        # Sample dummy response
        response = {
            "content": "Sample response about Barbeque Nation",
            "source": "knowledge_base",
            "confidence": 0.95,
            "tokens": 100
        }

        # Check token limit
        if response["tokens"] > 800:
            response = token_manager.truncate_response(response)

        return KnowledgeResponse(**response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/branch-info")
async def get_branch_info(query: Query):
    try:
        city = query.city.strip().replace(" ", "")
        branch = query.branch.strip().replace(" ", "")

        filename = f"{branch}_{city}.json"
        filepath = os.path.join("data", "knowledge_base", filename)

        if not os.path.isfile(filepath):
            raise HTTPException(
                status_code=404,
                detail=f"Branch data not found for '{query.branch}' in '{query.city}'"
            )

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
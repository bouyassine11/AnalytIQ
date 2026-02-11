from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from openai import OpenAI
from app.api.dependencies import get_current_user
from app.core.database import get_database
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/dataset/{dataset_id}", response_model=ChatResponse)
async def chat_with_dataset(
    dataset_id: str,
    chat_message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    db = await get_database()
    dataset = await db.datasets.find_one({"_id": ObjectId(dataset_id), "user_id": str(current_user["_id"])})
    
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    
    if dataset.get("status") != "completed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dataset analysis not completed")
    
    # Get analysis context
    analysis = dataset.get("analysis_result", {})
    eda = analysis.get("eda_results", {})
    cleaning = analysis.get("cleaning_report", {})
    
    # Build context for AI
    context = f"""Dataset: {dataset['filename']}
Rows: {eda.get('overview', {}).get('rows', 'N/A')}
Columns: {eda.get('overview', {}).get('columns', 'N/A')}
Data Quality: {eda.get('data_quality', {}).get('completeness', 0):.1f}% complete
Missing Values: {len(cleaning.get('missing_values', {}))} columns
Duplicates Removed: {cleaning.get('duplicates_removed', 0)}
Outliers: {len(cleaning.get('outliers_detected', {}))} columns detected

Column Analysis: {list(eda.get('column_analysis', {}).keys())}

User Question: {chat_message.message}"""
    
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=settings.HUGGINGFACE_API_KEY,
        )
        
        completion = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-Next:novita",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data analyst assistant. Answer questions about the dataset based on the provided context. Be concise and helpful."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            max_tokens=500,
            temperature=0.7,
        )
        
        response_text = completion.choices[0].message.content
        return ChatResponse(response=response_text)
        
    except Exception as e:
        # Fallback response
        return ChatResponse(
            response=f"I can help you understand your dataset '{dataset['filename']}' with {eda.get('overview', {}).get('rows', 'N/A')} rows and {eda.get('overview', {}).get('columns', 'N/A')} columns. The data is {eda.get('data_quality', {}).get('completeness', 0):.1f}% complete. What specific aspect would you like to know more about?"
        )

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
    overview = eda.get("overview", {})
    quality = eda.get("data_quality", {})
    column_analysis = eda.get("column_analysis", {})
    
    # Build detailed context
    columns_info = "\n".join([f"- {col}: {info.get('dtype', 'unknown')} ({info.get('unique_values', 0)} unique values)" 
                              for col, info in list(column_analysis.items())[:10]])
    
    context = f"""You are analyzing the dataset '{dataset['filename']}'.

Dataset Overview:
- Total Rows: {overview.get('rows', 'N/A'):,}
- Total Columns: {overview.get('columns', 'N/A')}
- Data Completeness: {quality.get('completeness', 0):.1f}%
- Memory Usage: {overview.get('memory_usage', 'N/A')}

Data Quality:
- Missing Values: {len(cleaning.get('missing_values', {}))} columns affected
- Duplicates Removed: {cleaning.get('duplicates_removed', 0)}
- Outliers Detected: {len(cleaning.get('outliers_detected', {}))} columns
- Numeric Columns: {quality.get('numeric_columns', 0)}
- Categorical Columns: {quality.get('categorical_columns', 0)}

Column Details:
{columns_info}

User Question: {chat_message.message}

Provide a clear, concise answer based on the data above. If asked about specific columns, trends, or recommendations, use the context provided."""
    
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
                    "content": "You are an expert data analyst. Provide clear, actionable insights about datasets. Be specific and reference actual numbers from the data."
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
        # Smart fallback based on question
        question_lower = chat_message.message.lower()
        
        if "column" in question_lower or "field" in question_lower:
            cols = list(column_analysis.keys())[:5]
            return ChatResponse(response=f"Your dataset has {len(column_analysis)} columns. The main ones are: {', '.join(cols)}. Each column has been analyzed for data types, missing values, and distributions.")
        
        elif "quality" in question_lower or "clean" in question_lower:
            return ChatResponse(response=f"Your data quality is {quality.get('completeness', 0):.1f}% complete. We removed {cleaning.get('duplicates_removed', 0)} duplicates and handled missing values in {len(cleaning.get('missing_values', {}))} columns.")
        
        elif "row" in question_lower or "size" in question_lower:
            return ChatResponse(response=f"Your dataset contains {overview.get('rows', 0):,} rows and {overview.get('columns', 0)} columns, using approximately {overview.get('memory_usage', 'N/A')} of memory.")
        
        else:
            return ChatResponse(response=f"I can help you understand your dataset '{dataset['filename']}' with {overview.get('rows', 0):,} rows and {overview.get('columns', 0)} columns. Ask me about specific columns, data quality, or recommendations!")

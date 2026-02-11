from datetime import datetime
from bson import ObjectId
from typing import Optional, Dict, Any
from app.core.database import get_database
from app.agents.orchestrator import OrchestratorAgent

class DatasetService:
    @staticmethod
    async def create_dataset(user_id: str, filename: str, file_path: str) -> Dict[str, Any]:
        db = await get_database()
        
        dataset_doc = {
            "user_id": user_id,
            "filename": filename,
            "file_path": file_path,
            "upload_date": datetime.utcnow(),
            "status": "processing",
            "analysis_result": None
        }
        
        result = await db.datasets.insert_one(dataset_doc)
        dataset_doc["_id"] = result.inserted_id
        return dataset_doc
    
    @staticmethod
    async def process_dataset(dataset_id: str):
        db = await get_database()
        
        dataset = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
        if not dataset:
            return
        
        try:
            orchestrator = OrchestratorAgent(dataset["file_path"])
            analysis_result = await orchestrator.run_analysis()
            
            await db.datasets.update_one(
                {"_id": ObjectId(dataset_id)},
                {
                    "$set": {
                        "status": "completed",
                        "analysis_result": analysis_result,
                        "completed_at": datetime.utcnow()
                    }
                }
            )
        except Exception as e:
            await db.datasets.update_one(
                {"_id": ObjectId(dataset_id)},
                {
                    "$set": {
                        "status": "failed",
                        "error": str(e)
                    }
                }
            )
    
    @staticmethod
    async def get_dataset(dataset_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        db = await get_database()
        return await db.datasets.find_one({"_id": ObjectId(dataset_id), "user_id": user_id})
    
    @staticmethod
    async def get_user_datasets(user_id: str):
        db = await get_database()
        cursor = db.datasets.find({"user_id": user_id}).sort("upload_date", -1)
        return await cursor.to_list(length=100)

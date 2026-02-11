from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, status
from typing import List
import os
import shutil
from bson import ObjectId
from app.api.dependencies import get_current_user
from app.services.dataset_service import DatasetService
from app.models.schemas import DatasetUploadResponse, AnalysisResponse

router = APIRouter(prefix="/datasets", tags=["Datasets"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    dataset = await DatasetService.create_dataset(
        user_id=str(current_user["_id"]),
        filename=file.filename,
        file_path=file_path
    )
    
    background_tasks.add_task(DatasetService.process_dataset, str(dataset["_id"]))
    
    return DatasetUploadResponse(
        dataset_id=str(dataset["_id"]),
        filename=dataset["filename"],
        status=dataset["status"],
        message="File uploaded successfully. Analysis in progress."
    )

@router.get("/analysis/{dataset_id}", response_model=AnalysisResponse)
async def get_analysis(
    dataset_id: str,
    current_user: dict = Depends(get_current_user)
):
    dataset = await DatasetService.get_dataset(dataset_id, str(current_user["_id"]))
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    analysis_result = dataset.get("analysis_result") or {}
    
    return AnalysisResponse(
        dataset_id=str(dataset["_id"]),
        filename=dataset["filename"],
        status=dataset["status"],
        cleaning_report=analysis_result.get("cleaning_report"),
        eda_results=analysis_result.get("eda_results"),
        visualizations=analysis_result.get("visualizations"),
        ai_insights=analysis_result.get("ai_insights"),
        created_at=dataset["upload_date"]
    )

@router.get("/list")
async def list_datasets(current_user: dict = Depends(get_current_user)):
    datasets = await DatasetService.get_user_datasets(str(current_user["_id"]))
    
    return [
        {
            "dataset_id": str(ds["_id"]),
            "filename": ds["filename"],
            "status": ds["status"],
            "upload_date": ds["upload_date"]
        }
        for ds in datasets
    ]

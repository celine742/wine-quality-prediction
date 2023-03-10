"""API module for model-related things.

This module contains API endpoints for serializing a model, add data to the datasource, retrain the model and get a description of its hyperparameters and its performance.
"""

from fastapi import APIRouter
import os
from app.model import model_xgboost

router = APIRouter()

@router.get("/api/model")
async def get_model() -> dict:
    """Saves model to disk.

    Returns:
        A dictionary of the message to confirm the model has been successfully saved.
    """
    # If model is not yet serialized, train it then save it
    if not os.path.isfile("app/model/model.p"):
        model_xgboost.save_model()
    return {"message" : "Le modele est serialise"}


@router.get("/api/model/description")
async def get_description() -> dict:
    """Description of the model hyperparameters and performance.

    Returns:
        A dictionary of the hyperparameters and their values and the mean squared error.
    """
    desc = model_xgboost.description()
    return desc

@router.put("/api/model")
async def add_data(fixed_acidity:float, volatile_acidity:float, citric_acid:float, 
                residual_sugar:float, chlorides:float, free_sulfur_dioxide:int,
                total_sulfur_dioxide:int, density:float, pH:float, sulphates:float, 
                alcohol:float, quality:int):
    model_xgboost.add_data_csv(fixed_acidity, volatile_acidity, citric_acid, 
                residual_sugar, chlorides, free_sulfur_dioxide,
                total_sulfur_dioxide, density, pH, sulphates, 
                alcohol, quality)
    return {"message": "La donnée a été ajoutée"}
    

@router.post("/api/model/retrain")
async def retrain_model() -> dict:
    """Retraining of the model.

    Returns:
        A dictionary of the message to confirm that it has successfuly been retrained.
    """
    model_xgboost.save_model()
    return {"message" : "Le modele est reentraine"}
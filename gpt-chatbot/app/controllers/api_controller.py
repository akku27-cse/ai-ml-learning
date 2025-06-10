from fastapi import APIRouter, HTTPException
from app.models.gpt2_model import gpt2_generator
from app.schemas.request_models import TextGenerationRequest
from app.config import settings

router = APIRouter()

@router.post("/generate")
async def generate_text(request: TextGenerationRequest):
    try:
        # Use request parameters if provided, otherwise use defaults from config
        max_length = request.max_length if request.max_length else settings.max_length
        num_sequences = request.num_return_sequences if request.num_return_sequences else settings.num_return_sequences
        
        # Temporary override of settings for this request
        original_max_length = settings.max_length
        original_num_sequences = settings.num_return_sequences
        
        settings.max_length = max_length
        settings.num_return_sequences = num_sequences
        
        result = gpt2_generator.generate_text(request.prompt)
        
        # Restore original settings
        settings.max_length = original_max_length
        settings.num_return_sequences = original_num_sequences
        
        return {"generated_text": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
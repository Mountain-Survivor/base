from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/models")

models = ["bert", "resnet"]

@router.get("/{model_name}")
def get_model(model_name: str, version: int = 1):
	if model_name not in models:
		raise HTTPException(
			status_code=404,
			detail="Model not found"
		)
	return {
		"model": model_name,
		"version": version
		}

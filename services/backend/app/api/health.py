from fastapi import APIRouter

router = APIRouter()


@router.get("/health", operation_id="health")
def health():
    return {"status": "ok"}

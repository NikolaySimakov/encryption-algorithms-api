from fastapi import APIRouter, status

router = APIRouter()


@router.post('/')
def process_metrics_data(data):
    pass
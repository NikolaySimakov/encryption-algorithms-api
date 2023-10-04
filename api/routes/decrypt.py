from fastapi import APIRouter, status

router = APIRouter()


@router.post('/')
def process_decrypt_data(data):
    pass
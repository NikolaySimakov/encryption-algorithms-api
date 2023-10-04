from fastapi import APIRouter, status

router = APIRouter()


@router.post('/')
def process_encrypt_data(data):
    pass
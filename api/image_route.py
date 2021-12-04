from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from api import image_svc

import database, schemas, models

router = APIRouter(prefix='/image', tags=['Image'])

@router.get('/get')
def get_image_by_tour_id(tour_id: str, db: Session = Depends(database.get_db)):
    return image_svc.get_image_by_tour_id(db, tour_id)

@router.post('/create')
def create_image(img: schemas.Images, db: Session = Depends(database.get_db)):
    image_svc.create_image(db, img)

@router.delete('/delete')
def delete_image_by_id(id: int, db: Session = Depends(database.get_db)):
    if not image_svc.delete_image(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'image with id {id} not found'
        )
    return 'success'

@router.delete('/delete-by-tour-id')
def delete_image_by_tour_id(tour_id: str, db: Session = Depends(database.get_db)):
    if not image_svc.delete_image_by_tour_id(db, tour_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Something go wrong'
        )
    return 'success'
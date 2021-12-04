from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import schemas, models
from fastapi import status, HTTPException, Depends

def get_image_by_tour_id(db: Session, tour_id: str):
    return db.query(models.Images).filter(models.Images.tour_id == tour_id).all()

def create_image(db: Session, image: schemas.Images):
    new_image = models.Images(**image.dict())

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

def delete_image(db: Session, id: int):
    image = db.query(models.Images).filter(models.Images.id == id)

    if (image.first() == None):
        return False
    
    image.delete(synchronize_session=False)
    db.commit()

    return True

def delete_image_by_tour_id(db: Session, id: str):
    images = db.query(models.Images).filter(models.Images.tour_id == id)

    if (images.all() == None):
        return False 

    images.delete(synchronize_session=False)
    db.commit()
    return True
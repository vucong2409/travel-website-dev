import fastapi
from pydantic.errors import StrRegexError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import schemas, models
from fastapi import status, HTTPException 

def get_route_by_tour_id(db: Session, tour_id: str):
    return db.query(models.Routes).filter(models.Routes.tour_id == tour_id).all()

def get_route_by_route_id(db: Session, route_id: int):
    return db.query(models.Routes).filter(models.Routes.route_id == route_id).first()

def create_route(db: Session, route: schemas.Routes):
    new_route = models.Routes(**route.dict()) 

    db.add(new_route)
    db.commit()
    db.refresh(new_route)

def delete_route_by_id(db: Session, route_id: int):
    route = db.query(models.Routes).filter(models.Routes.route_id == route_id)

    if (route.first() == None):
        return False
    
    route.delete(synchronize_session=False)
    db.commit()
    return True

def delete_route_by_tour_id(db: Session, tour_id: str):
    routes = db.query(models.Routes).filter(models.Routes.tour_id == tour_id)

    if (routes.all() == None):
        return False
    
    routes.delete(synchronize_session=False)
    db.commit()
    return True
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import schemas, models
from fastapi import status, HTTPException, Depends
from sqlalchemy.sql.expression import and_


def get_all_tour(db: Session):
    return db.query(models.Tour).all()


def get_tours(db: Session, limit: int, skip: int):
    return db.query(models.Tour).limit(limit).offset(skip).all()


def create_new_tour(db: Session, tour: schemas.TourOut):
    new_tour = models.Tour(**tour.dict())

    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)

    return new_tour


def tour_query_by_id(db: Session, tour_id: str):
    return db.query(models.Tour).filter(models.Tour.tour_id == tour_id)


def get_tour_by_id(db: Session, tour_id: str):
    tour = tour_query_by_id(db, tour_id).first()
    if not tour:
        return False
    return tour


def delete_tour_by_id(db: Session, tour_id: str):
    tour_query = tour_query_by_id(db, tour_id)

    if tour_query.first() == None:
        return False

    tour_query.delete(synchronize_session=False)
    db.commit()
    return True


def update_tour_by_id(db: Session, tour: schemas.TourToChange, tour_id: str):
    tour_query = tour_query_by_id(db, tour_id)

    if tour_query.first() == None:
        return False
    print(tour.dict())
    tour_query.update(tour.dict(), synchronize_session=False)
    db.commit()

    return tour_query.first()

def query_tour_by_place(db: Session, place_id: str, query: str):
    if (query == ''):
        return db.query(models.Tour).filter(models.Tour.place_id == place_id).all()
    else:
        return (
            db.query(models.Tour)
            .filter(and_(models.Tour.place_id == place_id, models.Tour.tour_title.contains(query)))
            .all()
        )

def query_tour_by_type(db: Session, type_id: str, query: str):
    if (query == ''):
        return db.query(models.Tour).filter(models.Tour.type_id == type_id).all()
    else:
        return (
            db.query(models.Tour)
            .filter(and_(models.Tour.type_id == type_id, models.Tour.tour_title.contains(query)))
            .all()
        )

def query_tour_global(db: Session, query: str):
    if (query == ''):
        return db.query(models.Tour).all()
    else:
        return (
            db.query(models.Tour)
            .filter(models.Tour.tour_title.contains(query))
            .all()
        )
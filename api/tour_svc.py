from sqlalchemy.orm import Session
import schemas, models
from fastapi import status, HTTPException, Depends


def get_all_tour(db: Session):
    return db.query(models.Tour).all()


def get_tours(db: Session, limit: int, skip: int):
    return db.query(models.Tour).limit(limit).offset(skip).all()


def create_new_tour(db: Session, tour: schemas.TourOut):
    print(tour.dict())
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

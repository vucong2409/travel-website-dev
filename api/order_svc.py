import fastapi
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends
from sqlalchemy.sql.expression import and_, false
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.roles import UsesInspection
import schemas, models

def get_your_order(user: models.Login, db: Session):
    orders = (db.query(models.Order)
        .filter(and_(models.Order.user_id == user.login_id, models.Order.confirmed == 1)) 
        .all()
    )
    return orders

def get_order_by_id(user: models.Login, db: Session, id: int):
    order = (db.query(models.Orderdetail)
        .filter(and_(models.Orderdetail.order_id == id, models.Orderdetail.customer_id == user.login_id)) 
        .first()
    )
    return order

def get_your_unconfirmed_order(user: models.Login, db: Session):
    orders = (db.query(models.Order)
        .filter(and_(models.Order.user_id == user.login_id, models.Order.confirmed == 0)) 
        .all()
    )
    return orders

def get_all_unconfirmed_order(user: models.Login, db: Session):
    if user.login_role_id == '1':
        return false

    orders = (db.query(models.Order)
        .filter(models.Order.confirmed == 0) 
        .all()
    )
    return orders

def confirm_order(user: models.Login, db: Session, id: int):
    if user.login_role_id == '1':
        return false

    order = (db.query(models.Order)
        .filter(models.Order.order_id == id) 
    )

    if (order.first() == None):
        return False

    order.confirmed = 1
    db.add(order)
    db.commit()
    db.refresh(order)

def create_your_order(user: models.Login, order_form: schemas.OrderForm, db: Session):
    order = models.Order(
        order_date = order_form.order_date,
        order_detail = order_form.order_detail,
        user_id = user.login_id,
        confirmed = 0
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    order_detail = models.Orderdetail(
        order_id = order.order_id,
        tour_id = order_form.tour_id,
        adult_number = order_form.adult_number,
        adult_price = order_form.adult_price,
        kid_number = order_form.kid_number,
        kid_price = order_form.kid_price,
        customer_id = user.login_id
    )
    
    db.add(order_detail)
    db.commit()
    db.refresh(order_detail)

    return "success"

def delete_order(login: models.Login, db: Session, id: int):
    orderdetail = (db.query(models.Orderdetail)
        .filter(and_(models.Orderdetail.order_id == id, models.Orderdetail.customer_id == login.login_id))
    )

    order = (db.query(models.Order)
        .filter(and_(models.Order.order_id == id, models.Order.user_id == login.login_id))
    )

    if (order.first() == None):
        return False
    
    if (orderdetail.first() == None):
        return False

    order.delete(synchronize_session=False)
    db.commit()

    orderdetail.delete(synchronize_session=False)
    db.commit()

    return True


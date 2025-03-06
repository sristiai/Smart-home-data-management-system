# src/controllers/resident_controller.py
print("Entering resident controller")
from src.models.db import db
from src.models.residents_model import Resident
from src.models.user_model import User
from src.models.houses_model import House
from src.controllers.house_controller import get_house_by_id

def get_all_residents():
    return (
        db.session.query(Resident, User, House)
        .join(User, Resident.user_id == User.user_id)
        .join(House, Resident.house_id == House.house_id)
        .all()
    )

def get_resident_by_id(resident_id):
    result = (
        db.session.query(Resident, User, House)
        .join(User, Resident.user_id == User.user_id)
        .join(House, Resident.house_id == House.house_id)
        .filter(Resident.resident_id == resident_id)
        .first()
    )
    if not result:
        return None
    resident, user, house = result
    return {
        "resident": resident,
        "user": user,
        "house": house
    }

def create_resident(data):
    house = get_house_by_id(data['house_id'])
    if not house:
        raise ValueError(f"House with id {data['house_id']} does not exist.")
    
    resident = Resident(
        user_id=data['user_id'],
        house_id=data['house_id'],
        move_in_date=data.get('move_in_date'),
        move_out_date=data.get('move_out_date')
    )
    db.session.add(resident)
    db.session.commit()
    return resident

def update_resident(resident, data):
    for field in ['move_in_date', 'move_out_date']:
        if field in data:
            setattr(resident, field, data[field])
    db.session.commit()
    return resident

def delete_resident(resident):
    db.session.delete(resident)
    db.session.commit()
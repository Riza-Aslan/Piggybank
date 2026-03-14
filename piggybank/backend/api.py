from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from datetime import datetime
import json
import io

import models
import schemas
from database import get_db

router = APIRouter()

# --- Accounts ---
@router.post("/accounts/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = db.query(models.Person).filter(models.Person.name == person.name).first()
    if db_person:
        raise HTTPException(status_code=400, detail="Person already exists")
    new_person = models.Person(name=person.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    new_person.balance = 0.0
    return new_person

@router.get("/accounts/", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = db.query(models.Person).offset(skip).limit(limit).all()
    # Calculate balance for each person
    for p in persons:
        balance = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.person_id == p.id).scalar()
        p.balance = balance if balance is not None else 0.0
    return persons

@router.delete("/accounts/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(db_person)
    db.commit()
    return {"ok": True}

@router.get("/accounts/{person_id}", response_model=schemas.PersonWithTransactions)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    balance = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.person_id == db_person.id).scalar()
    db_person.balance = balance if balance is not None else 0.0
    return db_person

# --- Transactions ---

@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_person = db.query(models.Person).filter(models.Person.id == transaction.person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    tx_data = transaction.model_dump()
    if not tx_data.get('date'):
        tx_data['date'] = datetime.utcnow()

    db_transaction = models.Transaction(**tx_data)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"ok": True}

@router.get("/transactions/", response_model=List[schemas.Transaction])
def read_all_transactions(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return db.query(models.Transaction).order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()

# --- HACS Integration Sensors ---

@router.get("/sensors")
def get_hacs_sensors(db: Session = Depends(get_db)):
    """
    Returns a simple JSON dict mapping person names to their current balance.
    This is consumed by the Home Assistant REST sensor / HACS.
    """
    persons = db.query(models.Person).all()
    sensors = {}
    for p in persons:
        balance = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.person_id == p.id).scalar()
        safe_name = p.name.lower().replace(" ", "_")
        sensors[safe_name] = round(balance if balance is not None else 0.0, 2)
    return sensors

# --- Import / Export ---

@router.get("/export")
def export_data_json(db: Session = Depends(get_db)):
    persons = db.query(models.Person).all()
    data = []
    for p in persons:
        transactions = db.query(models.Transaction).filter(models.Transaction.person_id == p.id).all()
        data.append({
            "name": p.name,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "transactions": [
                {
                    "amount": t.amount,
                    "note": t.note,
                    "date": t.date.isoformat() if t.date else None
                } for t in transactions
            ]
        })
    
    json_data = json.dumps({"export": data}, indent=2)
    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=piggybank_backup.json"
        }
    )

@router.post("/import")
async def import_data_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        payload = json.loads(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")

    if "export" not in payload:
        raise HTTPException(status_code=400, detail="Invalid import format: 'export' key missing")
    
    # CLEAR EVERYTHING
    db.query(models.Transaction).delete()
    db.query(models.Person).delete()
    db.commit()
    
    for p_data in payload["export"]:
        name = p_data.get("name")
        if not name:
            continue
            
        created_at = datetime.fromisoformat(p_data["created_at"]) if p_data.get("created_at") else datetime.utcnow()
        person = models.Person(name=name, created_at=created_at)
        db.add(person)
        db.commit()
        db.refresh(person)
            
        # Add transactions
        for t_data in p_data.get("transactions", []):
            try:
                dt = datetime.fromisoformat(t_data["date"]) if t_data.get("date") else datetime.utcnow()
            except ValueError:
                dt = datetime.utcnow()
                
            tx = models.Transaction(
                person_id=person.id,
                amount=t_data.get("amount", 0.0),
                note=t_data.get("note", ""),
                date=dt
            )
            db.add(tx)
        
        db.commit()
    
    return {"ok": True, "message": "Import successful. All old data was replaced."}
